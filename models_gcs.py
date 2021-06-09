#models for Google Cloud Storage

from connection_gcs import storage_client

#for uploading images
import os, requests, uuid, datetime, re

#for cropping images
from PIL import Image



GOOGLE_STORAGE_BUCKET = os.environ.get('GOOGLE_STORAGE_BUCKET', 'restaurant-app-314718-public')

TEMP_UPLOAD_FOLDER = './user-uploads'


class GCS():

    @staticmethod
    def user_blobs():
        USER_IMAGES_PREFIX = 'user-images/img' 
        return storage_client.list_blobs(GOOGLE_STORAGE_BUCKET, prefix=USER_IMAGES_PREFIX)

    @classmethod
    def image_urls(cls):
        """Lists all the blobs in the bucket."""
        # Note: Client.list_blobs requires at least package version 1.17.0.
        GCS_BASE_URL = "https://storage.googleapis.com"

        blobs = cls.user_blobs()

        return [f'{GCS_BASE_URL}/{GOOGLE_STORAGE_BUCKET}/{blob.name}' for blob in blobs] 

    @staticmethod
    def delete_blob(blob_name):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"
        bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
        blob = bucket.blob(blob_name)
        blob.delete()

    @classmethod
    def process_image(cls, image_file):

        #save original image
        extension = re.findall("(jpg|jpeg|png|gif|bmp)", image_file.filename)[0]
        filename = f'img-{uuid.uuid4()}.{extension}'
        image_path = os.path.join(TEMP_UPLOAD_FOLDER, filename)
        image_file.save(image_path)

        #crop to fit carousel
        cls.crop(image_path)

        policy = storage_client.generate_signed_post_policy_v4(
            GOOGLE_STORAGE_BUCKET,
            f'user-images/{filename}',
            expiration=datetime.timedelta(minutes=10),
            conditions=[
                ["content-length-range", 0, 1000000]
            ],
        )
        with open(image_path, "rb") as f:
            files = {"file": (image_path, f)}
            #try this, if fails then return False
            response = requests.post(policy["url"], data=policy["fields"], files=files)
            return response


    #methods crop, crop_center, and crop_max_square are PIL methods, not related to GCS
    @classmethod
    def crop(cls, image_path):
        with Image.open(image_path) as im:
            im_new = cls.crop_max_square(im)
            im_new.save(image_path, quality=95)

    @staticmethod
    def crop_center(pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))

    @classmethod
    def crop_max_square(cls, pil_img):
        return cls.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

