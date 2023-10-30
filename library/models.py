from django.db import models
from django.contrib.auth.models import User


class Tokens(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    token_refresh = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        blank=True, null= True
    )


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    release_year = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
    blank=False, null=True)

    pages = models.IntegerField()
    publishing_company = models.CharField(max_length=255)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    lent_book = models.BooleanField(blank=True, null= True)
    refund_book = models.BooleanField(blank=True, null= True)
    id_borrowed = models.ForeignKey(
        User,
        on_delete= models.SET_NULL,
        blank=True, null= True
    )

    def __str__(self) -> str:
        return self.title

