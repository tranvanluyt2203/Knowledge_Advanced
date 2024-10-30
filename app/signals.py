from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Folder, File
from django.conf import settings
from .Module_Final.class_text2neo4j import Text2Neo4j as t2n
import os


@receiver(post_delete, sender=Folder)
def delete_files_on_folder_delete(sender, instance, **kwargs):
    files = instance.files.all()
    if files:
        for file in files:
            file_path = os.path.join(settings.BASE_DIR, file.src.lstrip("/"))
            if os.path.isfile(file_path):
                os.remove(file_path)
            file.delete()


@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    print("receive delete file")
    file_path = instance.src
    # file_path = os.path.join(settings.BASE_DIR, instance.src.lstrip("/"))
    if instance.content_cypher:
        t2n().del_to_neo4j(instance.content_cypher)
    else:
        print("File have not cypher")
    if os.path.isfile(file_path):
        os.remove(file_path)
