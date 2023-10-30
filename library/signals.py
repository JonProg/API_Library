from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Book

@receiver(pre_delete, sender=User)
def update_book(sender, instance, **kwargs):
    Book.objects.filter(borrowed=instance).update(lent_book=True)
