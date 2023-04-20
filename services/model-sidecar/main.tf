variable "project" {
  type = string
  description = "The project under which the resources will be allocated."
  default = "blog-model-hosting"
}

variable "model_runtime_id" {
  type = string
  description = "The id you'd like to assign to this model runtime."
  default = "test0x01"
}

variable "model_runtime_region" {
  type = string
  description = "The region in which you'd like to allocate the runtime."
  default = "us-west1"
}

variable "min_instance_count" {
  type = number
  description = "Minimum number of instances for the runtime."
  default = 1
}

variable "max_instance_count" {
  type = number
  description = "Maximum number of instances for the runtime."
  default = 1
}

variable "model_runtime_container" {
  type = string
  description = "URI for the runtime container."
  default = "gcr.io/blog-model-hosting/model-runtime"
}

variable "model_runtime_prompt" {
  type = string
  description = "The prompt to use when the container starts."
  nullable = true
  default = null
}


provider "google" {
  project = var.project
}

resource "google_cloud_run_v2_service" "default" {

  name     =  var.model_runtime_id
  location = var.model_runtime_region
  ingress = "INGRESS_TRAFFIC_ALL"
  

  template {

    scaling {
        min_instance_count = var.min_instance_count
        max_instance_count = var.max_instance_count
    }
   
    containers {
      image = var.model_runtime_container
      env {
        name = "PROMPT"
        value = var.model_runtime_prompt
      }
    }  

    annotations = {
      "run.googleapis.com/cpu-throttling"      = false
    }

  }

}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_v2_service.default.location
  project     = google_cloud_run_v2_service.default.project
  service     = google_cloud_run_v2_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}



output "cloud_run_instance_url" {
  value = google_cloud_run_v2_service.default.uri
}
