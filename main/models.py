from distutils.command.upload import upload
from django.db import models
from django.forms import CharField, ImageField
from tariffs.models import TariffSettings

# Create your models here.
class Users(models.Model):
    telegram_id = models.IntegerField(null=True)
    secret_key = models.CharField(max_length=50, null=True)
    name_surname = models.CharField(max_length=255, null=True)
    date_birth = models.CharField(max_length=10 ,null=True)
    city = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=100, null=True)
    subcategories = models.CharField(max_length=200, null=True)
    interests = models.CharField(max_length=400, null=True)
    portfolio = models.CharField(max_length=500, null=True)
    balance = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/users/')
    select = models.CharField(max_length=50, default="registration")
    status = models.CharField(max_length=50, default="Новичок")
    verification = models.CharField(max_length=50, default="Не пройдена")


class UserSettings(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="user_settings")
    save_cards = models.CharField(max_length=5, null=False)


class UserTariff(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_tariff")
    tariff = models.ForeignKey(TariffSettings, on_delete=models.CASCADE, related_name="user_tariff", null=True)
    runs_until = models.CharField(max_length=10, null=True)


class BankDetalis(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="card_holder_user")
    card_number = models.CharField(max_length=16)
    card_action_date = models.CharField(max_length=5)
    card_holder = models.CharField(max_length=50)


class ProjectFiles(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="file_owner")
    file = models.FileField(upload_to="files/", default="")
    extension = models.CharField(max_length=10, null=True)


class Project(models.Model):
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="project_creator")
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    subsubcategory = models.CharField(max_length=60)
    employee_interests = models.CharField(max_length=200)
    price_no_more = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    file_1 = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE, null=True, related_name="project_file_1")
    file_2 = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE, null=True, related_name="project_file_2")
    file_3 = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE, null=True, related_name="project_file_3")
    file_4 = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE, null=True, related_name="project_file_4")
    file_5 = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE, null=True, related_name="project_file_5")
    enable_price_upper = models.CharField(max_length=3)


class Service(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="service_user")
    image = models.ImageField(upload_to="images/service/", null=True)
    title = models.CharField(max_length=70, null=True)
    purpose = models.TextField(null=True)
    price = models.CharField(max_length=50, null=True)


class Orders(models.Model):
    employer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="order_employer")
    employee = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="order_employee")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name="servise")
    purpose = models.TextField(null=True)
    price = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, null=True)
    completed_on_time = models.CharField(max_length=10,  null=True)
    feedback_to_employer = models.CharField(max_length=10, null=True)
    feedback_to_employee = models.CharField(max_length=10, null=True)


class DiplomsSertificats(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="diploms_sertificatts_user")
    text = models.CharField(max_length=100)
    img = models.ImageField(upload_to="images/diploms_sertificats/")


class ProfileViews(models.Model):
    user_who_view = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_who_view")
    user_profile = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_profile")