from django.db import models
from main.models import ProjectFiles, Users
# Create your models here.

class CreatingProject(models.Model):
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="creating_project_creator")
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    subsubcategory = models.CharField(max_length=60)
    employee_interests = models.CharField(max_length=200)
    price_no_more = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    file_1 = models.ForeignKey(ProjectFiles, on_delete=models.SET_NULL , null=True, related_name="creating_project_file_1")
    file_2 = models.ForeignKey(ProjectFiles, on_delete=models.SET_NULL , null=True, related_name="creating_project_file_2")
    file_3 = models.ForeignKey(ProjectFiles, on_delete=models.SET_NULL , null=True, related_name="creating_project_file_3")
    file_4 = models.ForeignKey(ProjectFiles, on_delete=models.SET_NULL , null=True, related_name="creating_project_file_4")
    file_5 = models.ForeignKey(ProjectFiles, on_delete=models.SET_NULL , null=True, related_name="creating_project_file_5")
    enable_price_upper = models.CharField(max_length=3, default="off")