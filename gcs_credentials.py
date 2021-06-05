import json

from google.oauth2 import service_account
from google.cloud import secretmanager

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = "projects/689769360983/secrets/GOOGLE_APPLICATION_CREDENTIALS/versions/1"

# Access the secret version.
response = client.access_secret_version(request={"name": name})

# Print the secret payload.
#
# WARNING: Do not print the secret in a production environment - this
# snippet is showing how to access the secret material.
payload = response.payload.data.decode("UTF-8")


json_acct_info = json.loads(payload)
credentials = service_account.Credentials.from_service_account_info(
    json_acct_info)