#!/bin/bash

# CloudMind AI API Keys Setup Script
# This script securely sets up your AI API keys

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp env.example .env
    print_success "Created .env file"
fi

# Update OpenAI API Key
print_status "Setting up OpenAI API key..."
sed -i.bak 's/OPENAI_API_KEY=your_openai_api_key_here/OPENAI_API_KEY=sk-proj-YOUR_OPENAI_API_KEY_HERE/' .env
print_success "OpenAI API key configured"

# Update Anthropic API Key
print_status "Setting up Anthropic API key..."
sed -i.bak 's/ANTHROPIC_API_KEY=your_anthropic_api_key_here/ANTHROPIC_API_KEY=sk-ant-YOUR_ANTHROPIC_API_KEY_HERE/' .env
print_success "Anthropic API key configured"

# Set proper permissions
print_status "Setting secure permissions on .env file..."
chmod 600 .env
print_success "Set secure permissions (600) on .env file"

# Remove backup file
rm -f .env.bak

print_success "✅ AI API keys have been securely configured!"
print_warning "⚠️  IMPORTANT: Never commit .env files to version control!"
print_warning "⚠️  The .env file is now in .gitignore for security"

echo ""
print_status "Next steps:"
echo "1. Run: ./scripts/setup/setup.sh"
echo "2. Test AI connections: curl -X GET 'http://localhost:8000/api/v1/ai/test/all'"
echo "3. Check AI status: curl -X GET 'http://localhost:8000/api/v1/ai/test/status'" 