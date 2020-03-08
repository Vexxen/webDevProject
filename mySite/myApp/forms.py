from django import forms
from django.core.validators import validate_slug


from . import models

def must_be_lowercase(value):
    if not value.islower():
        raise forms.ValidationError("Not all lowercase")
    return value

class SuggestionForm(forms.Form):
    suggestion = forms.CharField(
    label='Suggestion', 
    required=False, 
    max_length=240,
    #validators=[must_be_lowercase,validate_slug]
    )

    def save(self):
        suggestion_instance = models.Suggestion_Model()
        suggestion_instance.suggestion = self.cleaned_data["suggestion"]
        suggestion_instance.save()
        return suggestion_instance