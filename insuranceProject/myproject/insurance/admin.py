from django.contrib import admin
from django.utils.html import format_html

from .models import InsuranceMainCategory, InsuranceSubCategory, InsuranceLead



admin.site.register(InsuranceLead)


@admin.register(InsuranceSubCategory)
class InsuranceSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(InsuranceMainCategory)
class InsuranceMainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'