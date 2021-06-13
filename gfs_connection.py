#Google's free firestore database (if you don't use it too much)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from GOOGLE_APPLICATION_CREDENTIALS import GOOGLE_APPLICATION_CREDENTIALS

# from gcs_connection import json_acct_info

# Use the application default credentials
# cred = credentials.ApplicationDefault()

cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS())

firebase_admin.initialize_app(cred, {
  'projectId': 'restaurant-app-314718',
})

db = firestore.client()