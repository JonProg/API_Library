from django.db import models
from utils.rands import slugify_new
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    name = models.CharField(max_length=150)
    slug = models.SlugField(
        unique = True, default = None,
        null = True, blank = True, max_length = 150
    )

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=150)
    slug = models.SlugField(
        unique = True, default = None,
        null = True, blank = True, max_length = 150
    )

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    id_book = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    release_year = models.IntegerField()

    state = models.ForeignKey(Category, on_delete=models.SET_NULL,
    blank=False, null=True)

    pages = models.IntegerField()
    publishing_company = models.CharField(max_length=255)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=False, default='')

    def __str__(self) -> str:
        return self.title

