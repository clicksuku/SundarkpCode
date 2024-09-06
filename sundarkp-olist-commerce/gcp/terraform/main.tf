resource "google_compute_instance" "trans-array-412413" {
  name         = var.vmname
  machine_type = var.machinetype
  zone         = var.zone
  tags         = ["externalssh"]

  metadata = {
    enable-osconfig = "TRUE"
    ssh-keys        = "${var.user}:${file(var.publickeypath)}"
  }

  boot_disk {
    auto_delete = true

    initialize_params {
      image = var.osimage
      size  = 256
      type  = "pd-standard"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src           = "vm_add-tf"
    goog-ops-agent-policy = "v2-x86-template-1-2-0"
  }

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/trans-array-412413/regions/us-west4/subnetworks/default"
  }


  scheduling {
    automatic_restart   = false
    on_host_maintenance = "TERMINATE"
    preemptible         = true
    provisioning_model  = "SPOT"
  }


  provisioner "file" {
    connection {
      type        = "ssh"
      user        = var.user
      host        = google_compute_instance.trans-array-412413.network_interface[0].access_config[0].nat_ip
      private_key = file(var.privatekeypath)
    }

    source      = "installfiles.tar.gz"
    destination = "/tmp/installfiles.tar.gz"
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.user
      host        = google_compute_instance.trans-array-412413.network_interface[0].access_config[0].nat_ip
      private_key = file(var.privatekeypath)
    }
    inline = [
      "mv /tmp/installfiles.tar.gz ~",
      "tar xvzf ~/installfiles.tar.gz -C . ",
      "chmod u+x ~/installfiles/* ",
      "~/installfiles/setupscript.sh",
    ]
  }

  service_account {
    email  = google_service_account.skpsacustomca.email
    scopes = ["cloud-platform", "bigquery", "storage-full"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }
}
