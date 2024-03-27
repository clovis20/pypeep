from django import forms
from .models import Peep

class PeepForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Escreva seu Peep!",
                                   "class":"form-control",
                               }
                           ),
                           label="",
                           )
    
    class Meta:
        model = Peep
        exclude = ('user',)