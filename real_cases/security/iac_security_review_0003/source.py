resource "google_compute_instance" "default" {
  machine_type = "f1-micro"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network = "default"
    access_configs {
      // No NAT
    }
  }
}