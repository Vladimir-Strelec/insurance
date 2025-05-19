from django.db import models

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

    def __str__(self):
        return self.name


class InsuranceSubCategory(models.Model):
    """Подкатегории внутри основной категории"""
    main_category = models.ManyToManyField(InsuranceMainCategory, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subcategory_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class InsuranceLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.email}"