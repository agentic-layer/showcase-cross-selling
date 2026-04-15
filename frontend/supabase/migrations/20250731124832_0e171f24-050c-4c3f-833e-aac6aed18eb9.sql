-- Fix RLS policy for claims table to allow authenticated users to see all claims
-- This is appropriate for a demo environment where users should see all data

-- Drop the existing restrictive policy
DROP POLICY IF EXISTS "Users can view their own claims" ON public.claims;

-- Create a new policy that allows authenticated users to see all claims
CREATE POLICY "Authenticated users can view all claims"
ON public.claims
FOR SELECT
TO authenticated
USING (true);

-- Also update the insert and update policies to be less restrictive for demo purposes
DROP POLICY IF EXISTS "Users can insert their own claims" ON public.claims;
DROP POLICY IF EXISTS "Users can update their own claims" ON public.claims;

CREATE POLICY "Authenticated users can insert claims"
ON public.claims
FOR INSERT
TO authenticated
WITH CHECK (true);

CREATE POLICY "Authenticated users can update claims"
ON public.claims
FOR UPDATE
TO authenticated
USING (true);

-- Also fix the customers table policies to allow viewing all customer data
DROP POLICY IF EXISTS "Users can view their own customer data" ON public.customers;

CREATE POLICY "Authenticated users can view all customers"
ON public.customers
FOR SELECT
TO authenticated
USING (true);
