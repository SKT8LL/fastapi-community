#!/bin/bash
# UNMUTE Infrastructure Deployment Script
# Usage: ./deploy.sh [dev|prod]

set -e

ENV=${1:-dev}
LOCATION="eastus"
RESOURCE_GROUP="unmute-${ENV}-rg"
TEMPLATE_FILE="unmute-bicep-main.bicep"
PARAMETER_FILE="unmute-parameters-${ENV}.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

# Validate input
if [[ ! "$ENV" =~ ^(dev|prod)$ ]]; then
  log_error "Invalid environment. Use 'dev' or 'prod'."
  exit 1
fi

log_info "========== UNMUTE Infrastructure Deployment =========="
log_info "Environment: $ENV"
log_info "Resource Group: $RESOURCE_GROUP"
log_info "Region: $LOCATION"
echo ""

# Check Azure CLI
if ! command -v az &> /dev/null; then
  log_error "Azure CLI is not installed."
  exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
  log_error "Not logged in to Azure. Run 'az login' first."
  exit 1
fi

log_info "Creating resource group: $RESOURCE_GROUP..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --tags project=UNMUTE environment=$ENV managedBy=Bicep \
  || log_warn "Resource group already exists or creation error"

log_info "Validating Bicep template..."
if ! az deployment group validate \
  --resource-group $RESOURCE_GROUP \
  --template-file $TEMPLATE_FILE \
  --parameters $PARAMETER_FILE; then
  log_error "Template validation failed."
  exit 1
fi

# Confirmation for prod
if [ "$ENV" = "prod" ]; then
  log_warn "You are about to deploy to PRODUCTION."
  read -p "Are you sure? (yes/no): " confirmation
  if [ "$confirmation" != "yes" ]; then
    log_info "Deployment cancelled."
    exit 0
  fi
fi

log_info "Deploying infrastructure..."
az deployment group create \
  --name "unmute-${ENV}-$(date +%Y%m%d-%H%M%S)" \
  --resource-group $RESOURCE_GROUP \
  --template-file $TEMPLATE_FILE \
  --parameters $PARAMETER_FILE \
  --verbose

log_info "========== Deployment Completed =========="
log_info "Getting outputs..."

az deployment group show \
  --name $(az deployment group list -g $RESOURCE_GROUP --query "[-1].name" -o tsv) \
  --resource-group $RESOURCE_GROUP \
  --query properties.outputs \
  --output table

log_info "Environment: $ENV"
log_info "Resource Group: $RESOURCE_GROUP"
log_info "Deployment completed successfully!"
