import json
from uuid import uuid4
import custom_provider


def test_create():
    request = CustomResourceRequest("Create", {})
    response = custom_provider.handle(request, {})
    assert response["Status"] == "SUCCESS", response["Reason"]

def test_update():
    request = CustomResourceRequest("Update", {})
    response = custom_provider.handle(request, {})
    assert response["Status"] == "SUCCESS", response["Reason"]

def test_delete():
    request = CustomResourceRequest("Delete", {})
    response = custom_provider.handle(request, {})
    assert response["Status"] == "SUCCESS", response["Reason"]


class CustomResourceRequest(dict):
    def __init__(
        self, request_type: str, properties: dict, physical_resource_id: str = None
    ):
        self.update(
            {
                "RequestType": "Create",
                "ResponseURL": "https://httpbin.org/anything",
                "StackId": "arn:aws:cloudformation:us-west-2:111111111111:stack/stack-name/guid",
                "RequestId": str(uuid4()),
                "ResourceType": "Custom::Custom",
                "LogicalResourceId": "MyTestResource",
                "ResourceProperties": properties,
            }
        )
        if physical_resource_id:
            self["PhysicalResourceId"] = physical_resource_id
