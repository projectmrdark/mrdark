#!/bin/bash

echo "======================================"
echo "Mr.Dark Platform - System Test Suite"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Testing $name... "
    response=$(curl -s "$url")
    
    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Expected: $expected"
        echo "  Got: $response"
        ((FAILED++))
        return 1
    fi
}

# Function to test POST endpoint
test_post() {
    local name=$1
    local url=$2
    local data=$3
    local expected=$4
    
    echo -n "Testing $name... "
    response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$data")
    
    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Expected: $expected"
        echo "  Got: $response"
        ((FAILED++))
        return 1
    fi
}

echo "1. Backend API Tests"
echo "--------------------"
test_endpoint "Health Check" "http://localhost:8000/health" "healthy"
test_endpoint "API Config" "http://localhost:8000/api/config" "vc_api_configured"
test_endpoint "Root Endpoint" "http://localhost:8000/" "Mr.Dark"

echo ""
echo "2. AI Service Tests"
echo "-------------------"
test_endpoint "AI Connection Test" "http://localhost:8000/api/chat/test" "AI service is working correctly"
test_post "Simple Chat" "http://localhost:8000/api/chat/simple" '{"message":"Hello"}' "success"
test_endpoint "Available Models" "http://localhost:8000/api/chat/models" "models"

echo ""
echo "3. Frontend Tests"
echo "-----------------"
test_endpoint "Frontend Homepage" "http://localhost:3001" "Mr.Dark"
test_endpoint "Frontend Title" "http://localhost:3001" "AI Agent Platform"

echo ""
echo "4. Integration Tests"
echo "--------------------"

# Test full chat flow
echo -n "Testing Full Chat Flow... "
chat_response=$(curl -s -X POST "http://localhost:8000/api/chat/simple" \
    -H "Content-Type: application/json" \
    -d '{"message":"What is 2+2?"}')

if echo "$chat_response" | grep -q "success" && echo "$chat_response" | grep -q "response"; then
    echo -e "${GREEN}PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAILED${NC}"
    echo "  Response: $chat_response"
    ((FAILED++))
fi

# Test chat completions endpoint
echo -n "Testing Chat Completions... "
completion_response=$(curl -s -X POST "http://localhost:8000/api/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {"role": "user", "content": "Say hello"}
        ],
        "temperature": 0.7
    }')

if echo "$completion_response" | grep -q "success" && echo "$completion_response" | grep -q "data"; then
    echo -e "${GREEN}PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAILED${NC}"
    echo "  Response: $completion_response"
    ((FAILED++))
fi

echo ""
echo "======================================"
echo "Test Results Summary"
echo "======================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
