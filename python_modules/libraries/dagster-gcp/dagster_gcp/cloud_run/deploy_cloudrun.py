from google.cloud import run_v2
from google.auth import credentials

def deploy_cloud_run_service(image, command, env_vars, memory='512Mi', cpu='1'):
    """
    Deploy a container to Google Cloud Run.
    """
    service_name = "example-service"
    location = "us-central1"
    project_id = "your-project-id"

    client = run_v2.ServicesClient()
    parent = f"projects/{project_id}/locations/{location}"

    service = run_v2.Service()
    service.name = service_name
    service.template.containers[0].image = image
    service.template.containers[0].command = command
    service.template.containers[0].args = []
    service.template.containers[0].resources.limits["memory"] = memory
    service.template.containers[0].resources.limits["cpu"] = cpu

    for key, value in env_vars.items():
        env_var = run_v2.EnvVar(name=key, value=value)
        service.template.containers[0].env.append(env_var)

    # Call the Google Cloud Run API to deploy the service
    operation = client.create_service(parent=parent, service=service, service_id=service_name)
    print("Service deployed:", operation.result())

deploy_cloud_run_service(
    image='gcr.io/your-project-id/example-image',
    command=['python', 'app.py'],
    env_vars={'EXAMPLE_VAR': 'example_value'}
)

