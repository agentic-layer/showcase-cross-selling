#!/usr/bin/env bash

echo "Testing cross-selling conversation..."

# Start conversation with cross-selling request
echo "Sending cross-selling request..."

# -s: silent mode (no progress meter)
# -S: show error message even with -s
# -f: fail silently (no HTML output on server errors like 404)
CONVERSATION_RESPONSE=$(curl --max-time 90 -sfS -X POST http://localhost:8000/api/v1/chat/completions \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -d '{
     "model": "insurance_host_agent",
     "messages": [
       {
         "role": "user",
         "content": "Bitte entwickle eine cross-selling-strategie für Kunde cust001"
       }
     ]
   }')
exit_code=$?

echo "Conversation response:"
echo "$CONVERSATION_RESPONSE" | jq '.' 2>/dev/null || echo "$CONVERSATION_RESPONSE"

# Check the exit code
if [[ $exit_code -eq 0 ]]; then
  # Check if response contains expected content
  if echo "$CONVERSATION_RESPONSE" | grep -q "cust001\|strategie\|kunde" -i; then
      echo "✅ SUCCESS: Agent responded with relevant cross-selling content"
    else
      echo "❌ FAILURE: Agent response doesn't contain expected content"
      exit 1
    fi
else
  echo "❌ ERROR: curl command failed with exit code $exit_code"
  exit 1
fi
