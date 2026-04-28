provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "mesh_foundation" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Federated Identity & Access Control ---

resource "azurerm_user_assigned_identity" "mesh_control_plane" {
  name                = "id-mesh-control-${var.environment}"
  location            = azurerm_resource_group.mesh_foundation.location
  resource_group_name = azurerm_resource_group.mesh_foundation.name
}

# --- Global Metadata Discovery (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-mesh-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.mesh_foundation.name
  location               = azurerm_resource_group.mesh_foundation.location
  version                = "13"
  administrator_login    = "psqladmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Shared Compute Foundation (AKS for Mesh Control Plane) ---

resource "azurerm_kubernetes_cluster" "mesh_k8s" {
  name                = "aks-mesh-${var.environment}"
  location            = azurerm_resource_group.mesh_foundation.location
  resource_group_name = azurerm_resource_group.mesh_foundation.name
  dns_prefix          = "mesh-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- AWS Cross-Domain Data Sharing (S3/IAM) ---

resource "aws_s3_bucket" "mesh_products" {
  bucket = "mesh-data-products-${var.environment}"
}

resource "aws_iam_role" "domain_steward" {
  name = "DomainDataStewardRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}
