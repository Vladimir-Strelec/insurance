# Generated by Django 5.2 on 2025-06-10 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0008_remove_subcategory_main_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maincategory',
            name='seo_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='seo_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
