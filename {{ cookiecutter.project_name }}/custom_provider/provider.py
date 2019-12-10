import json
import logging
import os
from cfn_resource_provider import ResourceProvider


class CustomProvider(ResourceProvider):
    def __init__(self):
        super(CustomProvider, self).__init__()

    def create(self):
        self.fail("not implemented")

    def update(self):
        self.fail("not implemented")

    def delete(self):
        self.fail("not implemented")


provider = CustomProvider()


def handle(event, context):
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    return provider.handle(event, context)
