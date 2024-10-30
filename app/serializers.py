from rest_framework import serializers
from .models import Folder,File

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name','id_parent']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'id_folder', 'name','content','src']