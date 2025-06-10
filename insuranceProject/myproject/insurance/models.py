from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage


from django.db import models
from django.urls import reverse


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='category_images',  # Cloudinary folder
        blank=True,
        null=True
    )
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
    private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Main Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory_list', args=[self.slug])


class SubCategory(models.Model):
    main_category = models.ManyToManyField(MainCategory, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='category_images',  # Cloudinary folder
        blank=True,
        null=True
    )
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.main_category.name} → {self.name}"

    def get_absolute_url(self):
        return reverse('lead_create', args=[self.main_category.slug, self.slug])


class InsuranceLead(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='leads')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.subcategory})"

##################################################################################################


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

