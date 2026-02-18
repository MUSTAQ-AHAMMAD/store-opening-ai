#!/bin/bash
# Example script to test WhatsApp template message API endpoint

# Configuration
API_URL="http://localhost:5000"
PHONE="+966555313890"
CONTENT_SID="HXb5b62575e6e4ff6129ad7c8efe1f983e"

echo "======================================================================="
echo "🧪 Testing WhatsApp Template Message API"
echo "======================================================================="
echo ""

# Test 1: Send template message
echo "📱 Test 1: Sending template message with ContentSid and variables"
echo "-----------------------------------------------------------------------"
curl -X POST "${API_URL}/api/whatsapp/send-template" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE}\",
    \"content_sid\": \"${CONTENT_SID}\",
    \"content_variables\": {
      \"1\": \"12/1\",
      \"2\": \"3pm\"
    }
  }" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo ""

# Test 2: Send regular text message (backward compatibility)
echo "📝 Test 2: Sending regular text message (backward compatibility)"
echo "-----------------------------------------------------------------------"
curl -X POST "${API_URL}/api/whatsapp/send-follow-up" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE}\",
    \"message\": \"This is a regular text message for testing\"
  }" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo ""

# Test 3: Error handling - missing content_sid
echo "❌ Test 3: Error handling - missing content_sid"
echo "-----------------------------------------------------------------------"
curl -X POST "${API_URL}/api/whatsapp/send-template" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE}\"
  }" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo ""

# Test 4: Error handling - missing phone
echo "❌ Test 4: Error handling - missing phone"
echo "-----------------------------------------------------------------------"
curl -X POST "${API_URL}/api/whatsapp/send-template" \
  -H "Content-Type: application/json" \
  -d "{
    \"content_sid\": \"${CONTENT_SID}\"
  }" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo "======================================================================="
echo "✅ API Tests Complete"
echo "======================================================================="
