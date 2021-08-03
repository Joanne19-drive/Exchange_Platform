from django.db import models

# Create your models here.

<<<<<<< Updated upstream

class Question(models.Model):
    author = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    home_university = models.ForeignKey(
        to='domestic.Domestic University', on_delete=models.CASCADE, null=True, blank=True)
    away_university = models.ForeignKey(
        to='foreign.Foreign University', on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(
        to='country.Country', on_delete=models.CASCADE, null=True, blank=True)
    question_title = models.CharField(max_length=50)
    question_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_author = models.ForeignKey(
        to='login.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
