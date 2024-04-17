# OpenSearch Ingestor
This is a sample Python package managed with Poetry. It provides a simplified interaction with an Amazon OpenSearch Service, encapsulating the setup, configuration, and authenticated requests using the `opensearchpy` library.
## Features
- Automates the fetching of current AWS account details (ID, region, OpenSearch endpoint).
- Manages sessions and fetches necessary AWS credentials using `boto3`.
- Handles the AWS Signature Version 4 signing process.
- Provides methods for ingesting documents into specified OpenSearch indices.
## Requirements
- Python 3.7 or higher
- Poetry for dependency management
## Installation
First, clone this repository to your local machine:
``````
git clone https://github.com/bkovaluk/opensearch-ingestor.git
cd opensearch-ingestor
``````
Then, install the dependencies using Poetry:
``````
poetry install
``````
## Usage
To use this package, ensure that you have configured your AWS credentials properly and that you have access to an Amazon OpenSearch Service instance.
### Sample Code
Here's a quick example of how to use the `OpenSearchClient`:
``````
from opensearch_ingestor import OpenSearchClient
client = OpenSearchClient(os_host='your-opensearch-host-url')
async with client:
response = await client.ingest_to_opensearch('your-index-prefix', {'key': 'value'})
print(response)
``````
## Development
To contribute to this project, install the development dependencies:
``````
poetry install
``````
Then, you can run tests and linters:
``````
poetry run pytest
poetry run flake8
``````
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.