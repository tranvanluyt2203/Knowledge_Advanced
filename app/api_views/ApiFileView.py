from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.file_service import FileService
from ..serializers import FileSerializer


class FileCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        file = request.FILES.get("file")
        data["file"] = file
        data["name"] = file.name
        serializer = FileSerializer(data=data)
        print(data)
        if serializer.is_valid():
            file = FileService().addFile(file, serializer.validated_data["id_folder"])
            if not file:
                return Response(
                    {"Error": "Input is not valid"},
                    status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )
            return Response(FileSerializer(file).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileInforView(APIView):
    def post(self, request):
        search = request.data.get("search")
        page = request.data.get("page")
        id_folder = request.data.get("id_folder")
        per_page = request.data.get("per_page")
        order_by = request.data.get("order_by", "id")  # Mặc định là 'id' nếu không có
        order_direction = request.data.get(
            "order_direction", "asc"
        )  # Mặc định là 'asc' nếu không có
        # search = request.query_params.get('search')
        # page = request.query_params.get('page')
        # id_folder = request.query_params.get('id_folder')

        print(search, page, id_folder)

        if search != None and page != None:
            files = FileService().findFileByName(
                id_folder, search, page, per_page, order_by, order_direction
            )
            # if not files['files']:
            #     return Response(
            #         {
            #             "error": "No file found matching the search criteria."
            #         },
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            serializer = FileSerializer(files["files"], many=True)
            return Response(
                {
                    "files": serializer.data,
                    "total_pages": files["total_pages"],
                    "current_page": files["current_page"],
                    "has_next": files["has_next"],
                    "has_previous": files["has_previous"],
                    "total": files["total"],
                },
                status=status.HTTP_200_OK,
            )

        # id = request.query_params.get('id')
        id = request.data.get("id")
        if id != None:
            file_data = FileService().viewFileById(id)
            serializer = FileSerializer(file_data["file"])
            return Response(
                {"data": {"file": serializer.data, "folder": file_data["folder"]}},
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class FileUpdateView(APIView):
    def put(self, request):
        name = request.data.get("name")
        id = request.data.get("id")
        id_folder = request.data.get("id_folder")
        update_file = FileService().updateFile(id, name, id_folder)
        if not update_file:
            return Response(
                {"error": "Id is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": "Update success"}, status=status.HTTP_200_OK)


class FileDeleteView(APIView):
    def delete(self, request):
        deleted = FileService().deleteFile(request.query_params.get("id"))
        if not deleted:
            return Response(
                {"error": "File is not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Delete success"}, status=status.HTTP_204_NO_CONTENT
        )
