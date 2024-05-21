import logging
from google.cloud import run_v2
from google.api_core.exceptions import GoogleAPICallError
from dagster import Field, Permissive, RunLauncher, LaunchRunContext, DagsterRun, DagsterEvent
from typing import Optional


class CloudRunLauncher(RunLauncher):
    def __init__(self, project, location, service_name, client=None):
        self.project = project
        self.location = location
        self.service_name = service_name
        self.client = client or run_v2.ServicesClient()

    def launch_run(self, context: LaunchRunContext):
        """Launch a run on Google Cloud Run."""
        run = context.dagster_run
        image = self._get_image_for_run(context)
        command = self._get_command_args(context)

        try:
            response = self.client.create_service(
                parent=f"projects/{self.project}/locations/{self.location}",
                service={
                    "name": self.service_name,
                    "template": {
                        "containers": [{
                            "image": image,
                            "command": command,
                            "env": self._get_environment_variables(run),
                        }],
                        "resource_requirements": {
                            "cpu_allocation": "1000m",
                            "memory_allocation": "512Mi"
                        }
                    }
                }
            )
            logging.info(f"Launched Cloud Run service: {response.name}")
            return DagsterEvent.engine_event(context, f"Launched run as Cloud Run service: {response.name}")

        except GoogleAPICallError as e:
            logging.error(f"Failed to launch Cloud Run service: {str(e)}")
            raise

    @staticmethod
    def config_type():
        return {
            "project": Field(str, is_required=True, description="Google Cloud project ID."),
            "location": Field(str, is_required=True, description="Google Cloud Run region."),
            "service_name": Field(str, is_required=True, description="Cloud Run service name."),
        }

    def _get_command_args(self, context: LaunchRunContext):
        # Simplified example; should be adapted based on actual use case
        return ["python", "app.py"]

    def _get_image_for_run(self, context: LaunchRunContext) -> str:
        # Determine the container image to use; possibly from context or a fixed configuration
        return "gcr.io/project-id/image-name:tag"

    def _get_environment_variables(self, run: DagsterRun) -> dict:
        # Prepare environment variables for the container
        return {"DAGSTER_RUN_ID": run.run_id}

# Example instantiation
cloud_run_launcher = CloudRunLauncher(project="my-gcp-project", location="us-central1", service_name="my-dagster-service")
