from django.db import models

# Create your models here.
class Suggestion_Model(models.Model):
    suggestion = models.CharField(max_length=240)
    author = models.CharField(max_length=240, default="sean")
    def __str__(self):
        return self.suggestion

class Comment_Model(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(SuggestionModel, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment