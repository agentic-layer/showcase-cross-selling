-- Fix the verification_attempts RLS policy issue
DROP POLICY IF EXISTS "Allow insert access to service role" ON public.verification_attempts;
DROP POLICY IF EXISTS "Allow read access to own verification attempts" ON public.verification_attempts;

-- Create proper RLS policies for verification_attempts table
CREATE POLICY "Users can view their own verification attempts" ON public.verification_attempts
  FOR SELECT USING (auth.uid() = customer_id);

CREATE POLICY "Users can insert verification attempts" ON public.verification_attempts
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Service role can access all verification attempts" ON public.verification_attempts
  FOR ALL USING (auth.role() = 'service_role');
