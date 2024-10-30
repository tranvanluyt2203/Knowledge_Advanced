from django.urls import path
from .api_views.ApiFolderView import *
from .api_views.ApiFileView import *
from .api_views.ApiChatbotView import *
from .views import chatbot, cypher

urlpatterns = [
    path("folder/", FolderListView.as_view(), name="folder-list"),
    path("folder/add/", FolderCreateView.as_view(), name="folder-add"),
    path("folder/update/", FolderUpdateView.as_view(), name="folder-update"),
    path("folder/delete/", FolderDeleteView.as_view(), name="folder-delete"),
    path("folder/tree", FolderGetTree.as_view(), name="folder-get-tree"),
    
    path("file/", FileInforView.as_view(), name="file-list"),
    path("file/add/", FileCreateView.as_view(), name="file-add"),
    path("file/update/", FileUpdateView.as_view(), name="file-update"),
    path("file/delete/", FileDeleteView.as_view(), name="file-delete"),

    path("chatbot/", chatbot),
    path("cypher/", cypher),
    

    path("chatbotv2/", ChatbotAnswerView.as_view(), name="chatbot-answer"),
]
