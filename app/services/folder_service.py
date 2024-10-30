from typing import List, Dict
from django.core.paginator import Paginator
from ..repositories.folder_repository import FolderRepository
from ..models import Folder


class FolderService:
    def __init__(self):
        self.repository = FolderRepository()

    def addFolder(self, name, id_parent):
        return self.repository.add_folder(name, id_parent)

    def updateFolder(self, idFolder, newNameFolder, id_parent):
        return self.repository.update_folder(idFolder, newNameFolder, id_parent)

    def deleteFolder(self, idFolder):
        return self.repository.delete_folder(idFolder)

    def findFolderByName(
        self,
        search_name: str,
        page: int,
        num_item: int = 20,
        order_by: str = "id",
        order_direction: str = "asc",
    ) -> Dict:
        folders = self.repository.find_folder_by_name(search_name=search_name)

        if order_direction.lower() == "desc":
            folders = folders.order_by(f"-{order_by}")
        else:
            folders = folders.order_by(order_by)

        paginator = Paginator(folders, num_item)
        page = paginator.get_page(page)
        return {
            "folders": page.object_list,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
            "total": len(folders),
        }

    def getAllFolder(self) -> List[Folder]:
        return [folder for folder in self.repository.get_all_folder()]

    def getTree(self) -> List:
        return self.repository.get_tree()
