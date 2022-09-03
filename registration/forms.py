

from django import forms
from django.forms import DateField, ModelForm, Textarea, TextInput, DateInput
from main.models import Users

CATEGORIES = (('Категория 1', 'Категория 1'),('Категория 2', 'Категория 2'),)

class UserPhoto(forms.Form):
    userphoto = forms.ImageField()


class NameSurnameForm(ModelForm):
    class Meta:
        model = Users
        fields = ["name_surname"]
        widgets = {
            "name_surname": TextInput(attrs={
                "name": "name_surname",
                "type": "text",
                "placeholder": "Введите Имя Фамилию",
            })
        }


class DateBirthForm(ModelForm):
    class Meta:
        model = Users
        fields = ["date_birth"]
        widgets = {
            "date_birth": DateInput(attrs={
                "id": "date_birth",
                "name": "date_birth",
            })
        }



class CategoryForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES)


class SubCategoriesForm(forms.Form):
    OPTIONS = (
        ("Подкатегория 1", "Подкатегория 1"),
        ("Подкатегория 2", "Подкатегория 2"),
        ("Подкатегория 3", "Подкатегория 3"),
        ("Подкатегория 4", "Подкатегория 4"),
        ("Подкатегория 5", "Подкатегория 5"),
        ("Подкатегория 6", "Подкатегория 6"),
        ("Подкатегория 7", "Подкатегория 7"),
        ("Подкатегория 8", "Подкатегория 8"),
        ("Подкатегория 9", "Подкатегория 9"),
        ("Подкатегория 10", "Подкатегория 10"),
        ("Подкатегория 11", "Подкатегория 11"),
        ("Подкатегория 12", "Подкатегория 12"),
    )
    subcategories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                    choices=OPTIONS)


class InterestsForm(forms.Form):
    OPTIONS = (
        ("Интерес 1", "Интерес 1"),
        ("Интерес 2", "Интерес 2"),
        ("Интерес 3", "Интерес 3"),
        ("Интерес 4", "Интерес 4"),
        ("Интерес 5", "Интерес 5"),
        ("Интерес 6", "Интерес 6"),
        ("Интерес 7", "Интерес 7"),
        ("Интерес 8", "Интерес 8"),
        ("Интерес 9", "Интерес 9"),
        ("Интерес 10", "Интерес 10"),
        ("Интерес 11", "Интерес 11"),
        ("Интерес 12", "Интерес 12"),
    )
    interests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)
    

class PortfolioForm(forms.Form):
    instagram = forms.Field(help_text="instagram", required=False) #https://www.instagram.com/username
    dribbble = forms.Field(help_text="dribbble", required=False) #https://dribbble.com/username
    behance = forms.Field(help_text="behance", required=False)   #https://www.behance.net/username
    vk = forms.Field(help_text="vk", required=False) #https://vk.com/username



