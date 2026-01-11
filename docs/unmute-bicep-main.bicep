// UNMUTE: Indie Culture OS - Infrastructure as Code (Bicep)
// 2 Environments: dev, prod
// Core Services: PostgreSQL + Azure AI Search + Storage + App Service + OpenAI Integration
// Author: UNMUTE Team | Date: 2026-01-11

metadata description = 'UNMUTE Indie Culture Platform - Infrastructure deployment'
metadata version = '1.0'

// ============================================================================
// PARAMETERS
// ============================================================================

@minLength(1)
@maxLength(11)
@description('Prefix for all resource names (e.g., unmute)')
param namePrefix string = 'unmute'

@allowed(['dev', 'prod'])
@description('Deployment environment')
param env string = 'dev'

@description('Azure region for deployment')
param location string = 'eastus'

@description('PostgreSQL admin username')
param postgresAdminUsername string = 'unmute_admin'

@secure()
@description('PostgreSQL admin password')
param postgresAdminPassword string

@description('Azure AI Search SKU: basic or standard')
param searchSku string = 'basic'

@secure()
@description('OpenAI API Key')
param openAiApiKey string

@description('Environment-specific tags')
param tags object = {
  project: 'UNMUTE'
  environment: env
  managedBy: 'Bicep'
  createdDate: utcNow('yyyy-MM-dd')
}

// ============================================================================
// VARIABLES
// ============================================================================

var resourceGroupName = resourceGroup().name
var envSuffix = env == 'prod' ? '' : '-${env}'
var uniqueSuffix = uniqueString(resourceGroup().id)
var storageAccountName = '${namePrefix}stor${uniqueSuffix}'
var keyVaultName = '${namePrefix}-kv${envSuffix}-${substring(uniqueSuffix, 0, 5)}'
var postgresSeverName = '${namePrefix}-postgres${envSuffix}-${substring(uniqueSuffix, 0, 5)}'
var postgresDbName = 'unmute_db'
var searchServiceName = '${namePrefix}-search${envSuffix}-${substring(uniqueSuffix, 0, 5)}'
var aiServicesName = '${namePrefix}-ai${envSuffix}-${substring(uniqueSuffix, 0, 5)}'
var appServicePlanName = '${namePrefix}-asp${envSuffix}'
var webAppName = '${namePrefix}-api${envSuffix}-${substring(uniqueSuffix, 0, 5)}'
var appInsightsName = '${namePrefix}-appinsights${envSuffix}'
var logAnalyticsName = '${namePrefix}-law${envSuffix}'

// ============================================================================
// KEY VAULT
// ============================================================================

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
  }
}

resource openAiApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'openai-api-key'
  properties: {
    value: openAiApiKey
  }
}

// ============================================================================
// STORAGE ACCOUNT
// ============================================================================

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource blobContainerRawInstagram 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/raw-instagram'
  properties: {
    publicAccess: 'None'
  }
}

resource blobContainerRawOperator 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/raw-operator'
  properties: {
    publicAccess: 'None'
  }
}

resource blobContainerProcessed 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/processed'
  properties: {
    publicAccess: 'None'
  }
}

// ============================================================================
// POSTGRESQL
// ============================================================================

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01-preview' = {
  name: postgresSeverName
  location: location
  tags: tags
  sku: {
    name: env == 'prod' ? 'Standard_D4s_v3' : 'Standard_B1ms'
    tier: env == 'prod' ? 'GeneralPurpose' : 'Burstable'
  }
  properties: {
    administratorLogin: postgresAdminUsername
    administratorLoginPassword: postgresAdminPassword
    version: '15'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: env == 'prod' ? 30 : 7
      geoRedundantBackup: env == 'prod' ? 'Enabled' : 'Disabled'
    }
    network: {
      delegatedSubnetResourceId: ''
      privateDnsZoneArmResourceId: ''
    }
    highAvailability: {
      mode: env == 'prod' ? 'ZoneRedundant' : 'Disabled'
    }
    replicationRole: 'Primary'
  }
}

resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01-preview' = {
  parent: postgresServer
  name: postgresDbName
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

resource fireWallRuleAllowAll 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = if (env == 'dev') {
  parent: postgresServer
  name: 'AllowAllAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
  }
}

// ============================================================================
// AZURE AI SERVICES
// ============================================================================

resource aiServices 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: aiServicesName
  location: location
  tags: tags
  kind: 'CognitiveServices'
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  properties: {
    apiProperties: {
      statisticsEnabled: false
    }
    customSubDomainName: replace(aiServicesName, '-', '')
  }
}

// ============================================================================
// AZURE AI SEARCH
// ============================================================================

resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: searchSku
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    networkRuleSet: {
      ipRules: []
    }
  }
}

// ============================================================================
// APP INSIGHTS & LOG ANALYTICS
// ============================================================================

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}

// ============================================================================
// APP SERVICE
// ============================================================================

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: env == 'prod' ? 'P1V2' : 'B1'
    capacity: env == 'prod' ? 2 : 1
  }
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    clientAffinityEnabled: false
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: env == 'prod' ? true : false
      http20Enabled: true
      minTlsVersion: '1.2'
      scmMinTlsVersion: '1.2'
      ftpsState: 'Disabled'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'true'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'ApplicationInsightsAgent_EXTENSION_VERSION'
          value: '~3'
        }
        {
          name: 'XDT_MicrosoftApplicationInsights_Mode'
          value: 'recommended'
        }
        {
          name: 'DATABASE_URL'
          value: 'postgresql+psycopg2://${postgresAdminUsername}:${postgresAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}:5432/${postgresDbName}'
        }
        {
          name: 'AZURE_STORAGE_CONNECTION_STRING'
          value: 'DefaultEndpointProtocol=https;AccountName=${storageAccount.name};AccountKey=${listKeys(storageAccount.id, '2023-01-01').keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'STORAGE_CONTAINER_INSTAGRAM'
          value: 'raw-instagram'
        }
        {
          name: 'STORAGE_CONTAINER_OPERATOR'
          value: 'raw-operator'
        }
        {
          name: 'SEARCH_SERVICE_ENDPOINT'
          value: 'https://${searchService.name}.search.windows.net'
        }
        {
          name: 'SEARCH_SERVICE_ADMIN_KEY'
          value: listAdminKeys(searchService.id, '2023-11-01').primaryKey
        }
        {
          name: 'SEARCH_INDEX_NAME'
          value: 'unmute-index'
        }
        {
          name: 'OPENAI_API_KEY'
          value: openAiApiKey
        }
        {
          name: 'OPENAI_API_VERSION'
          value: '2024-02-01'
        }
        {
          name: 'OPENAI_EMBEDDING_MODEL'
          value: 'text-embedding-3-small'
        }
        {
          name: 'ENVIRONMENT'
          value: env
        }
      ]
    }
  }
}

// ============================================================================
// OUTPUTS
// ============================================================================

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output storageAccountEndpoint string = storageAccount.properties.primaryEndpoints.blob
output searchEndpoint string = 'https://${searchService.name}.search.windows.net'
output postgresqlFqdn string = postgresServer.properties.fullyQualifiedDomainName
output keyVaultUri string = keyVault.properties.vaultUri
output appInsightsKey string = appInsights.properties.InstrumentationKey
output resourceGroupName string = resourceGroupName
output environment string = env

