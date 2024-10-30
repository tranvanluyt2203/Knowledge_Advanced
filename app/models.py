from django.db import models


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    id_parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def update_idParent(self, id_parent):
        self.id_parent = id_parent
        self.save()

    def get_tree(self):
        children = [child.get_tree() for child in self.children.all()]
        files = list(self.files.values("name", "src"))

        return {"folder": self.name, "file": files, "children": children}

    def __str__(self):
        return self.name


class File(models.Model):

    id = models.AutoField(primary_key=True)
    id_folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files"
    )
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    content_cypher = models.JSONField(blank=True, null=True)
    src = models.CharField(max_length=100, null=True)

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def update_idFolder(self, id_folder):
        self.id_folder = id_folder

    def update_content_construct(self, new_content):
        self.content_construct = new_content
        self.save()

    def update_content(self, new_content):
        self.content = new_content
        self.save()

    def update_src(self, src):
        self.src = src
        self.save()

    def __str__(self):
        return self.name
