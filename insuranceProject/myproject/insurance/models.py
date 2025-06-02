from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage


class InsuranceMainCategory(models.Model):
    """Основные категории страхования"""
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='category_images',  # Cloudinary folder
        blank=True,
        null=True
    )
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class InsuranceSubCategory(models.Model):
    """Подкатегории внутри основной категории"""
    main_category = models.ManyToManyField(InsuranceMainCategory, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='category_images',  # Cloudinary folder
        blank=True,
        null=True
    )
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class InsuranceLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.email}"


from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Story(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    snippet = models.TextField()
    content = models.TextField()
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='category_images',  # Cloudinary folder
        blank=True,
        null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExternalLink(models.Model):
    story = models.ForeignKey(Story, related_name='external_links', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return f"{self.title} → {self.url}"

