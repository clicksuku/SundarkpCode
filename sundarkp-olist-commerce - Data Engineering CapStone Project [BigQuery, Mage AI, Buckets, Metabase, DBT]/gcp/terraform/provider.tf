terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.22.0"
    }
  }
}

provider "google" {
  project     = var.projectId
  credentials = file("${var.gcpkey}")
  #region      = var.region
  zone = var.zone
}
