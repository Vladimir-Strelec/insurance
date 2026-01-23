from django.utils.html import format_html

from .models import MainCategory, InsuranceLead, SubCategory
from .models import Story, Category, Tag, ExternalLink
from django.contrib import admin

admin.site.register(InsuranceLead)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "pdf_link")

    def pdf_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">PDF öffnen</a>',
                obj.file.url
            )
        return "-"



@admin.register(MainCategory)
class InsuranceMainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


class ExternalLinkInline(admin.TabularInline):
    model = ExternalLink
    extra = 1


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'snippet')
    list_filter = ('category', 'tags')
    inlines = [ExternalLinkInline]


admin.site.register(Category)
admin.site.register(Tag)
