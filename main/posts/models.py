from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=256)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
