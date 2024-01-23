terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # go to API & Services then search for compute engine and then enable the api.
  credentials = var.credentials
  project     = var.project
  region      = var.region
  zone        = var.zone
}