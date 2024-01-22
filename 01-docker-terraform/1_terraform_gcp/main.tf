terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  #credentials = "../../.ssh/gcp-sv.json"
  project = "dtc-de-412020"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "dtc-de-412020-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}