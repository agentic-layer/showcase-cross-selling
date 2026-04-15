-- Enable RLS on all public tables
ALTER TABLE public.claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.decision_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sentiment_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.call_transcripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.call_speaker_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.raw_webhook_events ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for claims table
CREATE POLICY "Users can view their own claims" ON public.claims
  FOR SELECT USING (auth.uid() = customer_id);

CREATE POLICY "Users can insert their own claims" ON public.claims
  FOR INSERT WITH CHECK (auth.uid() = customer_id);

CREATE POLICY "Users can update their own claims" ON public.claims
  FOR UPDATE USING (auth.uid() = customer_id);

CREATE POLICY "Service role can access all claims" ON public.claims
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for customers table
CREATE POLICY "Users can view their own customer data" ON public.customers
  FOR SELECT USING (auth.uid() = customer_id);

CREATE POLICY "Users can insert their own customer data" ON public.customers
  FOR INSERT WITH CHECK (auth.uid() = customer_id);

CREATE POLICY "Users can update their own customer data" ON public.customers
  FOR UPDATE USING (auth.uid() = customer_id);

CREATE POLICY "Service role can access all customers" ON public.customers
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for conversations table
CREATE POLICY "Users can view their own conversations" ON public.conversations
  FOR SELECT USING (auth.uid() = customer_id);

CREATE POLICY "Users can insert their own conversations" ON public.conversations
  FOR INSERT WITH CHECK (auth.uid() = customer_id);

CREATE POLICY "Users can update their own conversations" ON public.conversations
  FOR UPDATE USING (auth.uid() = customer_id);

CREATE POLICY "Service role can access all conversations" ON public.conversations
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for vehicles table
CREATE POLICY "Users can view their own vehicles" ON public.vehicles
  FOR SELECT USING (auth.uid() = customer_id);

CREATE POLICY "Users can insert their own vehicles" ON public.vehicles
  FOR INSERT WITH CHECK (auth.uid() = customer_id);

CREATE POLICY "Users can update their own vehicles" ON public.vehicles
  FOR UPDATE USING (auth.uid() = customer_id);

CREATE POLICY "Service role can access all vehicles" ON public.vehicles
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for decisions table
CREATE POLICY "Users can view decisions for their claims" ON public.decisions
  FOR SELECT USING (
    claim_id IN (
      SELECT id FROM public.claims WHERE customer_id = auth.uid()
    )
  );

CREATE POLICY "Service role can access all decisions" ON public.decisions
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for decision_logs table
CREATE POLICY "Users can view decision logs for their data" ON public.decision_logs
  FOR SELECT USING (
    customer_id = auth.uid() OR
    claim_id IN (
      SELECT id FROM public.claims WHERE customer_id = auth.uid()
    )
  );

CREATE POLICY "Service role can access all decision logs" ON public.decision_logs
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for sentiment_analysis table
CREATE POLICY "Users can view sentiment analysis for their claims" ON public.sentiment_analysis
  FOR SELECT USING (
    claim_id IN (
      SELECT id FROM public.claims WHERE customer_id = auth.uid()
    )
  );

CREATE POLICY "Service role can access all sentiment analysis" ON public.sentiment_analysis
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for call_transcripts table
CREATE POLICY "Service role can access all call transcripts" ON public.call_transcripts
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for call_speaker_segments table
CREATE POLICY "Service role can access all call speaker segments" ON public.call_speaker_segments
  FOR ALL USING (auth.role() = 'service_role');

-- Create RLS policies for raw_webhook_events table
CREATE POLICY "Service role can access all webhook events" ON public.raw_webhook_events
  FOR ALL USING (auth.role() = 'service_role');

-- Fix database functions with proper search_path
CREATE OR REPLACE FUNCTION public.update_modified_column()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.generate_claim_number()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    NEW.claim_number := 'CLM-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || UPPER(SUBSTRING(NEW.id::text, 1, 4));
    RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.populate_claims_sentiment()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    UPDATE claims c
    SET overall_sentiment = (
        SELECT overall_sentiment
        FROM sentiment_analysis sa
        WHERE sa.conversation_id = c.conversation_id
    )
    WHERE EXISTS (
        SELECT 1
        FROM sentiment_analysis sa
        WHERE sa.conversation_id = c.conversation_id
    );
END;
$function$;

CREATE OR REPLACE FUNCTION public.log_verification_attempt(p_customer_id uuid, p_matched_customer_id uuid, p_input_data jsonb, p_match_confidence double precision, p_address_verified boolean, p_status text, p_agent_id text DEFAULT NULL::text, p_conversation_id text DEFAULT NULL::text)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
declare
  result jsonb;
begin
  insert into public.verification_attempts (
    customer_id,
    matched_customer_id,
    input_data,
    match_confidence,
    address_verified,
    status,
    agent_id,
    conversation_id,
    created_at,
    updated_at
  ) values (
    p_customer_id,
    p_matched_customer_id,
    p_input_data,
    p_match_confidence,
    p_address_verified,
    p_status,
    p_agent_id,
    p_conversation_id,
    now(),
    now()
  ) returning to_jsonb(verification_attempts.*) into result;

  return result;
exception when others then
  return jsonb_build_object(
    'error', true,
    'message', SQLERRM,
    'detail', SQLSTATE
  );
end;
$function$;

CREATE OR REPLACE FUNCTION public.log_new_conversation()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
  RAISE NOTICE 'New conversation created: %', NEW.conversation_id;
  RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.update_claim_sentiment()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    IF NEW.conversation_id IS NOT NULL THEN
        UPDATE claims c
        SET overall_sentiment = sa.overall_sentiment
        FROM (
            SELECT overall_sentiment
            FROM sentiment_analysis
            WHERE conversation_id = NEW.conversation_id
            ORDER BY created_at DESC
            LIMIT 1
        ) sa
        WHERE c.id = NEW.id
        AND (c.overall_sentiment IS DISTINCT FROM sa.overall_sentiment);
    END IF;

    RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.update_claim_sentiment_explicitly()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    UPDATE claims c
    SET overall_sentiment = (
        SELECT sa.overall_sentiment
        FROM sentiment_analysis sa
        WHERE sa.conversation_id = c.conversation_id
        ORDER BY sa.created_at DESC
        LIMIT 1
    )
    WHERE c.conversation_id = NEW.conversation_id
    AND (
        c.overall_sentiment IS DISTINCT FROM (
            SELECT sa.overall_sentiment
            FROM sentiment_analysis sa
            WHERE sa.conversation_id = c.conversation_id
            ORDER BY sa.created_at DESC
            LIMIT 1
        )
        OR c.overall_sentiment IS NULL
    );

    RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.generate_claim_number(claim_id uuid)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
DECLARE
  new_claim_number TEXT;
  claim_record RECORD;
BEGIN
  SELECT * INTO claim_record FROM claims WHERE id = claim_id;

  IF claim_record.claim_number IS NULL THEN
    new_claim_number := 'CLM-' ||
                       TO_CHAR(NOW() AT TIME ZONE 'UTC', 'YYYYMMDD') || '-' ||
                       UPPER(SUBSTRING(claim_id::text, 1, 4));

    UPDATE claims
    SET claim_number = new_claim_number
    WHERE id = claim_id;

    RETURN new_claim_number;
  ELSE
    RETURN claim_record.claim_number;
  END IF;
END;
$function$;

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.trigger_generate_claim_number()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
  IF NEW.claim_number IS NULL THEN
    NEW.claim_number := 'CLM-' ||
                       TO_CHAR(NOW() AT TIME ZONE 'UTC', 'YYYYMMDD') || '-' ||
                       UPPER(SUBSTRING(NEW.id::text, 1, 4));
  END IF;
  RETURN NEW;
END;
$function$;

CREATE OR REPLACE FUNCTION public.update_claims_from_sentiment()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $function$
BEGIN
    UPDATE claims
    SET overall_sentiment = NEW.overall_sentiment
    WHERE conversation_id = NEW.conversation_id
    AND (overall_sentiment IS DISTINCT FROM NEW.overall_sentiment);

    RETURN NEW;
END;
$function$;
