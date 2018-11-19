from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# Create your models here.


class Chat(models.Model):
    chatname = models.CharField(max_length=20, default='noname')
    private = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='creator')
    members = models.ManyToManyField(User, related_name='members')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)
    viewed = models.BooleanField(default=False)
