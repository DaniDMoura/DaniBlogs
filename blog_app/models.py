from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class Signup(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.username}"


class Post(models.Model):
    title = models.CharField("Título", max_length=255)
    content = models.TextField("Conteúdo")
    date_published = models.DateField("Data de publicação", auto_now_add=True)
    slug = models.CharField("Slug", max_length=255, unique=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
