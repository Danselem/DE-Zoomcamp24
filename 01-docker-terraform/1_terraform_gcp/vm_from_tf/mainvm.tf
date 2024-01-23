resource "google_compute_instance" "vm-from-terraform" {
  name         = "vm-from-terraform"
  machine_type = "n2-standard-2"
  zone         = "us-central1-a"

  #   tags = ["foo", "bar"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        my_label = "value"
      }
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "NVME"
  }

  network_interface {
    network = "default"

    # access_config {
    #   // Ephemeral public IP
    # }
  }

  #   metadata = {
  #     foo = "bar"
  #   }

  metadata_startup_script = "echo hi > /test.txt"
  #   allow_stopping_for_update = true

  #   service_account {
  #     # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
  #     email  = google_service_account.default.email
  #     scopes = ["cloud-platform"]
  #   }
}
