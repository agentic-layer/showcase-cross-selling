#!/usr/bin/env bash

echo "Testing cross-selling conversation..."

# OpenAI API is stateless - no session needed
echo "Using OpenAI-compatible API endpoint"

# Start conversation with cross-selling request
echo "Sending cross-selling request..."
CONVERSATION_RESPONSE=$(timeout 90 curl -s -X POST http://localhost:8000/api/v1/chat/completions \
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
  }' || echo '{"error": "timeout"}')

echo "Conversation response:"
echo "$CONVERSATION_RESPONSE" | jq '.' 2>/dev/null || echo "$CONVERSATION_RESPONSE"

# Check if response contains expected content
if echo "$CONVERSATION_RESPONSE" | grep -q "cust001\|strategie\|kunde" -i; then
  echo "✅ SUCCESS: Agent responded with relevant cross-selling content"
else
  echo "❌ FAILURE: Agent response doesn't contain expected content"
  exit 1
fi
