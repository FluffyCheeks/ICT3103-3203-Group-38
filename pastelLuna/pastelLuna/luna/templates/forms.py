from django import forms

class NameForm(forms.form):
    email = forms.EmailField(label="Email", max_length=100)