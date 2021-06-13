#GCS (google cloud storage) connection file that imports some google libraries in order to create special credentials* and create an authenticated storage_client object that can interacts with GCS

#special credentials* are required to get the storage.Client().generate_signed_post_policy_v4() method to work, needed to upload images
import os
import json

from google.oauth2 import service_account 
from google.cloud import storage 

json_acct_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_TEXT'))
credentials = service_account.Credentials.from_service_account_info(json_acct_info)

#export storage_client variable to be used in models_gcs
storage_client = storage.Client(credentials=credentials)
