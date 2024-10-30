from ..models import Folder, File
from typing import Dict, List
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from ..Module_Final.class_text2neo4j import Text2Neo4j as t2n


class FileRepository:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileRepository,cls).__new__(cls)
        return cls._instance
    
    def add_file(self, file, folder) -> File:
        folder = Folder.objects.filter(id=folder.id).first()
        if not folder:
            return None
        print("type", file.content_type)
        if (
            file.content_type == "text/plain"
            or file.content_type == "application/octet-stream"
        ):
            file_content = file.read()
        else:
            return None
        # print("content", file_content)
        file_path = default_storage.save(
            f"uploads/{file.name}", ContentFile(file_content)
        )
        src = f"/media/{file_path}"
        content_ = t2n().gen_structure_data(
            t2n().process_data(file_content.decode("utf-8"))
        )
        newFile = File(
            id_folder=folder,
            name=file.name,
            content=content_,
            src=settings.DELOY_URL + src,
            content_cypher=t2n().convert_to_cypher(content_),
        )
        t2n().push_to_neo4j(newFile.content_cypher)
        print("Push to neo4j")

        newFile.save()
        return newFile

    def get_file_by_id(self, id) -> File:
        return File.objects.filter(id=id).first()

    def update_file(self, id_file, new_name_file, id_folder) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        if new_name_file:
            file.update_name(new_name_file)
        if id_folder:
            if Folder.objects.filter(id=id_folder).first():
                file.update_idFolder(Folder.objects.filter(id=id_folder).first())
            else:
                return None
        file.save()
        return file

    def delete_file(self, id_file) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        file.delete()
        return file

    def view_file_by_id(self, id_file) -> Dict:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        folder = Folder.objects.filter(id=file.id_folder.id).first()

        data = {"file": file, "folder": folder.name}
        return data

    def find_file_by_name(self,id_folder=None, search_name="") -> List[File]:
        result_files = File()
        if not id_folder:
            result_files = File.objects.filter(name__icontains=search_name)
        else:
            result_files = File.objects.filter(
                name__icontains=search_name, id_folder=id_folder
            )
        return result_files
