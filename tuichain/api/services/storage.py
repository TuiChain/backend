from django.conf import settings
from google.cloud import storage


def upload_file(file, name):

    storage_client = storage.Client.from_service_account_json(
        settings.GCP_CREDENTIALS
    )

    bucket = storage_client.get_bucket(settings.GCP_BUCKET_NAME)
    blob = bucket.blob(name)
    blob.upload_from_file(file)

    # returns a public url
    return blob.public_url
