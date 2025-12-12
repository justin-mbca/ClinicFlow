#!/bin/bash
# Azure CLI setup script for Clinical NLP PoC
# Usage: bash setup_azure_cli.sh

# Set variables (replace these with your actual values or export them before running)
SUBSCRIPTION_ID="<YOUR_SUBSCRIPTION_ID>"
RESOURCE_GROUP="<YOUR_RESOURCE_GROUP>"
LOCATION="eastus"
KEY_VAULT_NAME="<YOUR_KEY_VAULT_NAME>"
COG_SERVICE_NAME="<YOUR_COG_SERVICE_NAME>"
COG_SERVICE_SKU="S"
STORAGE_ACCOUNT="<YOUR_STORAGE_ACCOUNT>"
SQL_SERVER="<YOUR_SQL_SERVER_NAME>"
SQL_ADMIN="<YOUR_SQL_ADMIN_USER>"
SQL_PASSWORD="<YOUR_SQL_ADMIN_PASSWORD>"
SQL_DB="<YOUR_SQL_DATABASE_NAME>"

# Login and set subscription
az login
az account set --subscription "$SUBSCRIPTION_ID"

# Create Resource Group
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# Create Key Vault
az keyvault create --name "$KEY_VAULT_NAME" --resource-group "$RESOURCE_GROUP" --location "$LOCATION"

# Create Cognitive Services for Health
az cognitiveservices account create \
  --name "$COG_SERVICE_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --kind TextAnalytics \
  --sku "$COG_SERVICE_SKU" \
  --location "$LOCATION" \
  --yes

# Store Cognitive Services Key and Endpoint in Key Vault
COG_KEY=$(az cognitiveservices account keys list --name "$COG_SERVICE_NAME" --resource-group "$RESOURCE_GROUP" --query key1 -o tsv)
COG_ENDPOINT=$(az cognitiveservices account show --name "$COG_SERVICE_NAME" --resource-group "$RESOURCE_GROUP" --query properties.endpoint -o tsv)
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "cog-service-key" --value "$COG_KEY"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "cog-service-endpoint" --value "$COG_ENDPOINT"

# Create Storage Account and Blob Container
az storage account create --name "$STORAGE_ACCOUNT" --resource-group "$RESOURCE_GROUP" --location "$LOCATION" --sku Standard_LRS
STORAGE_KEY=$(az storage account keys list --resource-group "$RESOURCE_GROUP" --account-name "$STORAGE_ACCOUNT" --query [0].value -o tsv)
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "storage-key" --value "$STORAGE_KEY"
az storage container create --account-name "$STORAGE_ACCOUNT" --name "raw-data"

# Create Azure SQL Server and Database
az sql server create --name "$SQL_SERVER" --resource-group "$RESOURCE_GROUP" --location "$LOCATION" --admin-user "$SQL_ADMIN" --admin-password "$SQL_PASSWORD"
az sql db create --resource-group "$RESOURCE_GROUP" --server "$SQL_SERVER" --name "$SQL_DB" --service-objective S0
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "sql-admin" --value "$SQL_ADMIN"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "sql-password" --value "$SQL_PASSWORD"

# Set Key Vault access policy for yourself (replace with your Azure AD user objectId)
USER_OBJECT_ID=$(az ad signed-in-user show --query objectId -o tsv)
az keyvault set-policy --name "$KEY_VAULT_NAME" --object-id "$USER_OBJECT_ID" --secret-permissions get list

echo "Azure resources and Key Vault secrets setup complete."
