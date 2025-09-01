#!/bin/bash

# Simple Local Secrets Management for Self-Hosted Deployment
# This script provides basic secrets management without cloud services

set -e

SECRETS_DIR="./secrets"
BACKUP_DIR="./backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create directories
mkdir -p "$SECRETS_DIR"
mkdir -p "$BACKUP_DIR"

# Generate strong secrets
generate_secret() {
    local length=${1:-32}
    openssl rand -base64 "$length" | tr -d "=+/" | cut -c1-"$length"
}

# Encrypt secrets file
encrypt_secrets() {
    local file="$1"
    if [ -f "$file" ]; then
        gpg --symmetric --cipher-algo AES256 "$file"
        rm "$file"
        print_status "Encrypted $file"
    fi
}

# Decrypt secrets file
decrypt_secrets() {
    local file="$1"
    if [ -f "$file.gpg" ]; then
        gpg --decrypt "$file.gpg" > "$file"
        print_status "Decrypted $file"
    fi
}

# Generate all secrets
generate_all_secrets() {
    print_status "Generating strong secrets..."
    
    # Generate secrets
    cat > "$SECRETS_DIR/secrets.env" << EOF
# CloudMind Secrets - Generated $(date)
# WARNING: Keep this file secure and never commit to version control!

# JWT Secret (64 characters)
SECRET_KEY=$(generate_secret 64)

# Database Passwords (32 characters each)
DB_PASSWORD=$(generate_secret 32)
TIMESCALE_PASSWORD=$(generate_secret 32)

# Service Passwords (32 characters each)
MINIO_SECRET_KEY=$(generate_secret 32)
NEO4J_PASSWORD=$(generate_secret 32)
GRAFANA_PASSWORD=$(generate_secret 32)
REDIS_PASSWORD=$(generate_secret 32)

# API Keys (if needed)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# SSL Certificate Password (if needed)
SSL_CERT_PASSWORD=$(generate_secret 24)
EOF

    print_status "Generated secrets in $SECRETS_DIR/secrets.env"
    
    # Create backup
    cp "$SECRETS_DIR/secrets.env" "$BACKUP_DIR/secrets_$(date +%Y%m%d_%H%M%S).env"
    print_status "Backup created in $BACKUP_DIR"
}

# Rotate secrets
rotate_secrets() {
    print_warning "This will generate new secrets. Make sure to update your deployment!"
    
    # Backup current secrets
    if [ -f "$SECRETS_DIR/secrets.env" ]; then
        cp "$SECRETS_DIR/secrets.env" "$BACKUP_DIR/secrets_backup_$(date +%Y%m%d_%H%M%S).env"
        print_status "Backed up current secrets"
    fi
    
    generate_all_secrets
    print_status "Secrets rotated successfully"
}

# Secure secrets file
secure_secrets() {
    if [ -f "$SECRETS_DIR/secrets.env" ]; then
        # Set restrictive permissions
        chmod 600 "$SECRETS_DIR/secrets.env"
        
        # Encrypt if GPG is available
        if command -v gpg &> /dev/null; then
            encrypt_secrets "$SECRETS_DIR/secrets.env"
            print_status "Secrets encrypted with GPG"
        else
            print_warning "GPG not available. Consider installing for encryption."
        fi
        
        print_status "Secrets secured with restrictive permissions"
    fi
}

# Load secrets into environment
load_secrets() {
    if [ -f "$SECRETS_DIR/secrets.env.gpg" ]; then
        decrypt_secrets "$SECRETS_DIR/secrets.env"
    fi
    
    if [ -f "$SECRETS_DIR/secrets.env" ]; then
        export $(cat "$SECRETS_DIR/secrets.env" | xargs)
        print_status "Secrets loaded into environment"
    else
        print_error "No secrets file found. Run 'generate' first."
        exit 1
    fi
}

# Validate secrets
validate_secrets() {
    local secrets_file="$SECRETS_DIR/secrets.env"
    
    if [ -f "$secrets_file.gpg" ]; then
        decrypt_secrets "$secrets_file"
    fi
    
    if [ -f "$secrets_file" ]; then
        print_status "Validating secrets..."
        
        # Check for weak passwords
        while IFS= read -r line; do
            if [[ $line =~ ^[A-Z_]+= ]]; then
                local key=$(echo "$line" | cut -d'=' -f1)
                local value=$(echo "$line" | cut -d'=' -f2-)
                
                # Skip comments and empty lines
                if [[ $key != \#* ]] && [[ -n $value ]]; then
                    if [[ $value == *"cloudmind"* ]] || [[ $value == *"password"* ]] || [[ $value == *"secret"* ]]; then
                        print_warning "Weak secret detected in $key"
                    fi
                    
                    if [[ ${#value} -lt 16 ]]; then
                        print_warning "Short secret detected in $key (${#value} chars)"
                    fi
                fi
            fi
        done < "$secrets_file"
        
        print_status "Secrets validation complete"
    else
        print_error "No secrets file found"
        exit 1
    fi
}

# Main script logic
case "${1:-help}" in
    "generate")
        generate_all_secrets
        secure_secrets
        ;;
    "rotate")
        rotate_secrets
        secure_secrets
        ;;
    "secure")
        secure_secrets
        ;;
    "load")
        load_secrets
        ;;
    "validate")
        validate_secrets
        ;;
    "backup")
        if [ -f "$SECRETS_DIR/secrets.env" ]; then
            cp "$SECRETS_DIR/secrets.env" "$BACKUP_DIR/secrets_$(date +%Y%m%d_%H%M%S).env"
            print_status "Backup created"
        else
            print_error "No secrets file to backup"
        fi
        ;;
    "help"|*)
        echo "CloudMind Secrets Management"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  generate  - Generate new strong secrets"
        echo "  rotate    - Rotate existing secrets"
        echo "  secure    - Secure secrets with encryption and permissions"
        echo "  load      - Load secrets into environment"
        echo "  validate  - Validate secrets for security"
        echo "  backup    - Create backup of current secrets"
        echo "  help      - Show this help message"
        echo ""
        echo "Security Features:"
        echo "  - Generates cryptographically strong secrets"
        echo "  - Encrypts secrets with GPG (if available)"
        echo "  - Sets restrictive file permissions"
        echo "  - Creates automatic backups"
        echo "  - Validates secrets for weak patterns"
        ;;
esac 