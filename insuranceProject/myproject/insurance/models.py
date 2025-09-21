from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage
from urllib.parse import urljoin, urlparse

from django.db import models
from django.urls import reverse

PLACEHOLDER_MAIN = "https://placehold.co/600x400/png?text=Main+Category"


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=500, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
    private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Main Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("insurance:subcategory_list", args=[self.slug])

    @property
    def image_url(self) -> str:
        """
        Возвращает пригодный к использованию URL картинки для категории.
        Работает и с URLField (строка), и с File/ImageField (если вернёте его в будущем).
        """
        v = getattr(self, "image", None)
        if not v:
            return PLACEHOLDER_MAIN

        # Если когда-нибудь снова будет ImageField/FileField
        if hasattr(v, "url"):
            try:
                return v.url
            except Exception:
                return PLACEHOLDER_MAIN

        # Строка
        if isinstance(v, str):
            # Абсолютный URL?
            if urlparse(v).scheme in ("http", "https"):
                return v
            # Относительный – сделаем относительно MEDIA_URL
            from myproject import settings
            return urljoin(settings.MEDIA_URL, v.lstrip("/"))

        return PLACEHOLDER_MAIN


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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or f"sub-{self.pk or ''}".strip('-')
            s = base
            i = 1
            # гарантируем уникальность
            while SubCategory.objects.filter(slug=s).exclude(pk=self.pk).exists():
                i += 1
                s = f"{base}-{i}"
            self.slug = s
        super().save(*args, **kwargs)

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
        return f"{self.full_name} ({self.subcategory}) datum: {self.created_at}"

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
    image = models.URLField(max_length=500, blank=True, null=True)
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

