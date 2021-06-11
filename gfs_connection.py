#Google's free firestore database (if you don't use it too much)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# from gcs_connection import json_acct_info

# Use the application default credentials
cred = credentials.ApplicationDefault()
# cred = credentials.Certificate(json_acct_info)
firebase_admin.initialize_app(cred, {
  'projectId': 'restaurant-app-314718',
})

db = firestore.client()