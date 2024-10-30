from ..repositories.file_repository import FileRepository
from django.core.paginator import Paginator
from ..models import File
from typing import Dict


class FileService:
    def __init__(self):
        self.fileReposiroty = FileRepository()

    def addFile(self, file, folder):
        return self.fileReposiroty.add_file(file, folder)

    def updateFile(self, id_file, new_name_file, id_folder):
        return self.fileReposiroty.update_file(id_file, new_name_file, id_folder)

    def deleteFile(self, id_file):
        return self.fileReposiroty.delete_file(id_file)

    def viewFileById(self, id_file):
        return self.fileReposiroty.view_file_by_id(id_file)

    def findFileByName(
        self,
        id_folder: int,
        search: str,
        page: int,
        num_item: int = 20,
        order_by: str = "id",
        order_direction: str = "asc",
    ) -> Dict:
        files = self.fileReposiroty.find_file_by_name(id_folder, search)

        if order_direction.lower() == "desc":
            files = files.order_by(f"-{order_by}")
        else:
            files = files.order_by(order_by)

        paginator = Paginator(files, num_item)
        page = paginator.get_page(page)
        return {
            "files": page.object_list,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
            "total": len(files),
        }
