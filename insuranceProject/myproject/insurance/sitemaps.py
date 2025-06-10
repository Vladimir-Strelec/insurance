from django.contrib.sitemaps import Sitemap
from .models import Story, MainCategory, SubCategory

class StorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Story.objects.all()

    def location(self, obj):
        return f"/story/{obj.slug}/"

class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return SubCategory.objects.all()

    def location(self, obj):
        main_cat = obj.main_category.first()
        if main_cat:
            return f"/{main_cat.slug}/{obj.slug}/"
        return f"/{obj.slug}/"  # fallback, если нет main_category
