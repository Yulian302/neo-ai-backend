import shutil

import boto3
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        url = (
            "https://ui-avatars.com/api/?background=random&size=512&uppercase=true&format=png"
            "&name=%(name)s"
        )
        name_letter = instance.username[0]
        avatar_response = requests.get(url % {"name": name_letter}, stream=True)
        file_name = f"{instance.username}.png"
        try:
            local_file_path = f"{settings.BASE_DIR}/temp/{file_name}"
            with open(local_file_path, "wb") as f:
                shutil.copyfileobj(avatar_response.raw, f)
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            s3.upload_file(
                local_file_path,
                settings.AWS_STORAGE_BUCKET_NAME,
                f"avatars/{file_name}",
            )

            os.remove(local_file_path)

        except Exception as e:
            print("File could not be created!")
        UserProfile.objects.create(
            user=instance,
            avatar_url=f"{settings.AWS_S3_BASE_URL%{'dir_name':'avatars','file_name':file_name}}",
        )
