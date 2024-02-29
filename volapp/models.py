from django.db import models

def default_emotions():
    return {'emotions': []}

def default_answers():
    return {'answers': []}

class Users(models.Model):
    email = models.CharField(unique=True, max_length=500)
    streak = models.PositiveIntegerField(default=0)
    maxStreak = models.PositiveIntegerField(default=0)
    lastPostTime = models.DateTimeField(null=True)
    joinedOn = models.DateTimeField(auto_now_add=True)

class Posts(models.Model):
    multimedia = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    emotions = models.JSONField(default=default_emotions)
    answers = models.JSONField(default=default_answers)
    total_likes = models.PositiveBigIntegerField(default=0)

class Likes(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE)