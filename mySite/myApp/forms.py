from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_slug
from django.contrib.auth.models import User


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

    image = forms.ImageField(
        label="Image File",
        required=False
    )

    image_description = forms.CharField(
        label="Image Description",
        max_length=240,
        required=False
    )

    def save(self):
        suggestion_instance = models.Suggestion_Model()
        suggestion_instance.suggestion = self.cleaned_data["suggestion"]
        suggestion_instance.author = request.user
        suggestion_instance.image = self.cleaned_data["image"]
        suggestion_instance.image_description = self.cleaned_data["image_description"]
        suggestion_instance.save()
        return suggestion_instance

class CommentForm(forms.Form):
    comment = forms.TextField(
        label='Comment',
        required=True
    )

    def save(self, request, sugg_id):
        suggestion_instance = models.SuggestionModel.objects.filter(id=sugg_id).get()
        comment_instance = models.CommentModel()
        comment_instance.suggestion = suggestion_instance
        comment_instance.comment = self.cleaned_data["comment"]
        comment_instance.author = request.user
        comment_instance.save()
        return comment_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = User
        fields = ("username", "email",
                    "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user