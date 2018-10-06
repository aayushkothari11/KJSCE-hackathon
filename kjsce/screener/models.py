from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator



class Event(models.Model):
    user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    csv_file = models.FileField(upload_to='uploads/',null=True,blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    github_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    quora_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    resume_link = models.TextField(validators=[URLValidator()], null=True, blank=True)
    text_result = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    number = models.BigIntegerField(validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)], blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)
    event = models.ForeignKey(Event, blank=True, null=True,on_delete=models.CASCADE)
    college = models.CharField(max_length=100, blank=True, null=True)


class Keyword(models.Model):
    word = models.CharField(max_length=50, blank=True, null=True)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
