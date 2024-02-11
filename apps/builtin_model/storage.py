from storages.backends.s3boto3 import S3Boto3Storage


class PublicModelsImagesStorage(S3Boto3Storage):
    location = 'models_images'
    file_overwrite = False
