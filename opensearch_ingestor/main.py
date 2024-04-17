"""
OpenSearch Client

This module provides a convenient way to interact with Amazon OpenSearch Service (formerly known as Amazon Elasticsearch Service).
It encapsulates the setup and configuration needed to make authenticated requests to OpenSearch Service using the `opensearchpy` library.

Features:
- Fetches the current AWS account's details (ID, region, OpenSearch endpoint) based on the `ACCOUNT_DETAILS` mapping.
- Automatically uses the `boto3` library to create a session and fetches the necessary AWS credentials.
- Handles the AWS Signature Version 4 signing process to authorize the OpenSearch requests.
- Provides methods `ingest_to_opensearch` and `bulk_ingest_to_opensearch` to ingest a document into a specified OpenSearch index.

Author: Brad Kovaluk
Last Updated: July 2023
"""

import boto3
import json
import logging
from opensearchpy import AsyncOpenSearch, AsyncHttpConnection, AWSV4SignerAsyncAuth
from datetime import datetime

# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# A constant to hold the service name
SERVICE = "es"


class OpenSearchClient:
    """
    A class to interact with OpenSearch service.
    """

    def __init__(self, os_host, session: boto3.Session = None):
        """
        Constructor method. Initializes OpenSearch client.

        Uses environment variables to set region and OpenSearch host.

        :param session: Optional boto3 Session object. If None, creates a default session.
        """
        if session is None:
            session = boto3.Session()

        self.credentials = session.get_credentials()
        self.region = session.region_name
        self.os_host = os_host

        # Initialize the AWS V4 signer with credentials, region, and service
        self.awsauth = AWSV4SignerAsyncAuth(self.credentials, self.region, SERVICE)

    async def __aenter__(self):
        """
        Async context manager enter method. Initializes the OpenSearch client.
        """
        self.client = AsyncOpenSearch(
            hosts=[{"host": self.os_host, "port": 443}],
            http_auth=self.awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=AsyncHttpConnection,
            pool_maxsize=20,
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Async context manager exit method. Closes the OpenSearch transport.
        """
        await self.client.transport.close()

    async def ingest_to_opensearch(self, index_prefix: str, doc: dict) -> None:
        """
        Ingests a document into OpenSearch.

        :param index_prefix: Prefix of the index to which the document should be ingested.
        :param doc: The document to be ingested. Expected to be a dictionary.

        Returns:
        dict: Response dict from OpenSearch.
        """
        index = f"{index_prefix}-{datetime.now().strftime('%Y.%m.%d')}"
        try:
            # Index the document
            response = await self.client.index(index=index, body=doc)
            logger.info(f"OpenSearch response: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to ingest document into OpenSearch. Error: {str(e)}")

    async def bulk_ingest_to_opensearch(self, index_prefix: str, docs: list) -> None:
        """
        Ingests multiple documents into OpenSearch using the bulk API.

        :param index_prefix: Prefix of the index to which the documents should be ingested.
        :param docs: The list of documents to be ingested. Each document is expected to be a dictionary.
        """
        bulk_data = ""
        index_date = datetime.now().strftime("%Y.%m.%d")
        for doc in docs:
            action_and_meta_data = {
                "index": {
                    "_index": f"{index_prefix}-{index_date}",
                    # Optionally, specify a unique ID for each document
                    # "_id": doc.get("id") or str(uuid.uuid4()),
                }
            }
            bulk_data += f"{json.dumps(action_and_meta_data)}\n{json.dumps(doc)}\n"

        try:
            # Perform the bulk ingest
            response = await self.client.bulk(body=bulk_data, index=index_prefix)
            logger.info(f"Bulk OpenSearch response: {response}")
            return response
        except Exception as e:
            logger.error(
                f"Failed to bulk ingest documents into OpenSearch. Error: {str(e)}"
            )
