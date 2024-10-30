from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.folder_service import FolderService
from ..serializers import FolderSerializer


class FolderListView(APIView):
    def post(self, request):
        # search = request.data.get('search')
        # page = request.data.get('page')
        search = request.data.get("search")
        page = request.data.get("page")
        per_page = request.data.get("per_page")
        order_by = request.data.get("order_by", "id")  # Mặc định là 'id' nếu không có
        order_direction = request.data.get(
            "order_direction", "asc"
        )  # Mặc định là 'asc' nếu không có

        if page is not None:
            folders = FolderService().findFolderByName(
                search, page, per_page, order_by, order_direction
            )
            # if not folders['folders']:
            #     return Response(
            #         {"error": "No folders found matching the search criteria."},
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            serializer = FolderSerializer(folders["folders"], many=True)
            return Response(
                {
                    "folders": serializer.data,
                    "total_pages": folders["total_pages"],
                    "current_page": folders["current_page"],
                    "has_next": folders["has_next"],
                    "has_previous": folders["has_previous"],
                    "total": folders["total"],
                },
                status=status.HTTP_200_OK,
            )

        folders = FolderService().getAllFolder()
        serializer = FolderSerializer(folders, many=True)
        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class FolderCreateView(APIView):
    def post(self, request):
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            folder = FolderService().addFolder(
                serializer.validated_data["name"],
                serializer.validated_data.get("id_parent"),
            )
            return Response(
                FolderSerializer(folder).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderUpdateView(APIView):
    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        id_parent = request.data.get("id_parent")
        if id == id_parent:
            return Response(
                {"error": "Id and id parent not same"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        updated_folder = FolderService().updateFolder(id, name, id_parent)
        if not updated_folder:
            return Response(
                {"error": "Folder is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": "Update success"}, status=status.HTTP_200_OK)


class FolderDeleteView(APIView):
    def delete(self, request):
        deleted = FolderService().deleteFolder(request.query_params.get("id"))
        if not deleted:
            return Response(
                {"error": "Folder is not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Delete success"}, status=status.HTTP_204_NO_CONTENT
        )


class FolderGetTree(APIView):
    def get(self, request):
        result = FolderService().getTree()
        print(result)
        return Response(
            {"data": result},
            status=status.HTTP_200_OK,
        )
