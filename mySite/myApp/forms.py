from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_slug 
from django.contrib.auth.models import User


from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already Exists")
    # Always return the cleaned data, whether you have changed it or
    # not.
    return value

def must_be_lowercase(value):
    if not value.islower():
        raise forms.ValidationError("Not all lowercase")
    return value

class SuggestionForm(forms.Form):
    suggestion = forms.CharField(
    label='Suggestion', 
    required=True, 
    max_length=240
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

    def save(self, request):
        suggestion_instance = models.Suggestion_Model()
        suggestion_instance.suggestion = self.cleaned_data["suggestion"]
        suggestion_instance.author = request.user
        suggestion_instance.image = self.cleaned_data["image"]
        suggestion_instance.image_description = self.cleaned_data["image_description"]
        suggestion_instance.save()
        return suggestion_instance

class PostForm(forms.Form):
    title = forms.CharField(
        label='title',
        required=True,
        max_length=50
    )
    body = forms.CharField(
        widget=forms.Textarea,
        label='body',
        required=False
    )

    def save(self, sub):
        subreddit_instance = models.Subreddit.objects.filter(title=sub).get()
        post_instance = models.Post()
        post_instance.title = self.cleaned_data["title"]
        post_instance.body = self.cleaned_data["body"]
        post_instance.subreddit = subreddit_instance
        post_instance.save()
        return post_instance

class ReplyForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea,
        label='body',
        required=False
    )

    def save(self, sub, post_id):
        post_instance = models.Post.objects.filter(id=post_id).get()
        subreddit_instance = models.Subreddit.objects.filter(title=sub).get()
        reply_instance = models.Post()
        reply_instance.parent = post_instance
        reply_instance.body = self.cleaned_data["body"]
        reply_instance.subreddit = subreddit_instance
        reply_instance.save()
        return reply_instance

# class CommentForm(forms.Form):
#     comment = forms.CharField(
#         widget=forms.Textarea,
#         label='Comment',
#         required=True
#     )

#     def save(self, request, sugg_id):
#         suggestion_instance = models.Suggestion_Model.objects.filter(id=sugg_id).get()
#         comment_instance = models.Comment_Model()
#         comment_instance.suggestion = suggestion_instance
#         comment_instance.comment = self.cleaned_data["comment"]
#         comment_instance.author = request.user
#         comment_instance.save()
#         return comment_instance

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



class SubredditForm(forms.Form):
    # class Meta:
    #     model = Subreddit
    #     fields = ['title', 'description']

    #create new Subreddit
    title = forms.CharField(
        label='title',
        max_length=30,
        required=True,
        validators=[validate_slug]
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label='description',
        required=True
    )
    def save(self, request):
        subreddit_instance = models.Subreddit()
        subreddit_instance.title = self.cleaned_data["title"]
        subreddit_instance.description = self.cleaned_data['description']
        subreddit_instance.creator = request.user
        subreddit_instance.save()
        return subreddit_instance

    # def __init__(self, *args, **kwargs):
    #     super(SubredditForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.layout.append(Submit('submit', 'Submit', css_class='btn btn-primary'))



# class UserForm(forms.Form):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email)')

# class ProfileForm(forms.Form):
#         class Meta:
#             model = Profile
#             fields = ('url', 'location', 'company')