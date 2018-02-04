from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
regexValidator = RegexValidator(regex=r'[0-9]{9}', message="Phone number should consist of 9 digits.")


class FacebookUser(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phoneNumber = models.CharField(validators=[regexValidator], max_length=17)
    emailAddress = models.EmailField()
    facebookId = models.CharField(max_length=50, unique=True)


class Message(models.Model):
    user = models.ForeignKey(FacebookUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    messageText = models.CharField(max_length=1000)
    actionTaken = models.CharField(max_length=50)
