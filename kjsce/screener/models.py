from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class Event(models.Model):
    user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    csv_file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return name


class Applicant(models.Model):
    github_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    linkedin_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    resume_link = models.TextField(validators=[URLValidator()], null=True, blank=True)
    text_result = models.CharField(max_length=1000, blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)
    event = models.ForeignKey(Event, blank=True, null=True,on_delete=models.CASCADE)


class Keyword(models.Model):
    word = models.CharField(max_length=50, blank=True, null=True)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return word
