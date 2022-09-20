from django.forms import FileField
from django.forms import Form
from django import forms

class FileInputForm(Form):
    file = FileField(required=False, allow_empty_file=False, widget=forms.FileInput(attrs={"class":"file_input", "onchange": "add_file(this)", "accept": ".pdf, .docx, .xlsx, .png, .jpg, .jpeg"}))

