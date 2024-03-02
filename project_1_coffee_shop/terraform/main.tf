terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = file(var.credentials)
  project = var.project
  region  = "asia-southeast1"
}

resource "google_storage_bucket" "static" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.storage_class
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

resource "google_bigquery_dataset" "dataset-zy" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.location
  delete_contents_on_destroy = true
}


resource "google_compute_instance" "default" {
  provider = google
  zone = "asia-southeast1-a"
  name = "the-malaysian-coffee"
  machine_type = "e2-standard-4"
  network_interface {
    network = "default"
    access_config {
      
    }
  }

  boot_disk {
    initialize_params {
      image = var.ubuntu_2004_sku
      size = 50
    }
    auto_delete = true
  }
  # Some changes require full VM restarts
  # consider disabling this flag in production
  #   depending on your needs
  # allow_stopping_for_update = true
}
