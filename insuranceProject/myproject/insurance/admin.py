from django.utils.html import format_html

from .models import MainCategory, InsuranceLead, SubCategory, Video
from .models import Story, Category, Tag, ExternalLink
from django.contrib import admin

admin.site.register(InsuranceLead)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pdf_link')
    readonly_fields = ('pdf_link',)


@admin.register(MainCategory)
class InsuranceMainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')


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
