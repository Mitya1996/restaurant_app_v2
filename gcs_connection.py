#GCS (google cloud storage) connection file that imports some google libraries in order to create special credentials* and create an authenticated storage_client object that can interacts with GCS

#special credentials* are required to get the storage.Client().generate_signed_post_policy_v4() method to work, needed to upload images

import json

from google.oauth2 import service_account #standard google.cloud lib
from google.cloud import secretmanager #had to install
from google.cloud import storage #standard google.cloud lib

from GOOGLE_APPLICATION_CREDENTIALS import GOOGLE_APPLICATION_CREDENTIALS
import os

#JSON service account key uploaded to google secretmanager

# Create the Secret Manager client.
secretmanager_client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = "projects/689769360983/secrets/GOOGLE_APPLICATION_CREDENTIALS/versions/1"

# Access the secret version.
response = secretmanager_client.access_secret_version(request={"name": name})

payload = response.payload.data.decode("UTF-8")

# json_acct_info = json.loads(payload)
json_acct_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_TEXT'))

credentials = service_account.Credentials.from_service_account_info(json_acct_info)

#export storage_client variable to be used in models_gcs
storage_client = storage.Client(credentials=credentials)
