from django import forms

class UserArtForm(forms.Form):
    painting = forms.ImageField()