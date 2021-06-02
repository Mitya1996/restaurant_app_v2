from google.cloud import storage

GCS_BASE_URL = "https://storage.googleapis.com"

def image_urls(bucket_name, prefix):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    return [f'{GCS_BASE_URL}/{bucket_name}/{blob.name}' for blob in blobs] 


