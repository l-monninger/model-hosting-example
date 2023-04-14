from ..deployer import Deployer
from typing import Optional
from google.cloud.run_v2 import ServicesAsyncClient, CreateServiceRequest, Service, RevisionTemplate, Container, DeleteServiceRequest, RevisionScaling
import os

CONTAINER_IMAGE = os.environ.get("CONTAINER_IMAGE", "gcr.io/blog-model-hosting/model-sidecar")

class CloudRunDeployer(Deployer):
    
    # CreateServiceRequest, Service, RevisionTemplate, Container
    
    sidecar_url : Optional[str]
    client : ServicesAsyncClient
    
    image : str
    project : str
    region : str
    
    def __init__(
        self, *,
        client : ServicesAsyncClient = ServicesAsyncClient(),
        image : str = os.environ.get("IMAGE", "gcr.io/blog-model-hosting/model-sidecar"),
        project : str = os.environ.get("PROJECT", "blog-model-hosting"),
        region : str = os.environ.get("REGION", "us-west1"),
    ) -> None:
        super().__init__()
        self.sidecar_url = None
        self.client = client
        self.image = image
        self.project = project
        self.region = region
        
    async def deploy_sidecar(self, id: str) -> str:
        op = await self.client.create_service(CreateServiceRequest(
            parent=f"projects/{self.project}/locations/{self.region}",
            service_id=id,
            service=Service(
                uid=id,
                ingress="INGRESS_TRAFFIC_ALL",
                template=RevisionTemplate(
                    scaling=RevisionScaling(
                        min_instance_count=1,
                        max_instance_count=1
                    ),
                    containers=[
                        Container(
                            image=self.image
                        )
                    ],
                    annotations={
                        
                    }
                )
            )
        ))
        await self.client.set_iam_policy({
            "resource" : f"projects/{self.project}/locations/{self.region}/services/{id}",
            "policy": {"bindings": [{"members": ["allUsers"], "role": "roles/run.invoker"}]},
        })
        return (await op.result()).uri
    
    async def destroy_sidecar(self, id: str):
        op = await self.client.delete_service(DeleteServiceRequest(
            name=f"projects/{self.project}/locations/{self.region}/services/{id}"
        ))