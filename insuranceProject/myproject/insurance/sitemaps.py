from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['insurance_dynamic', 'submit_lead', 'policy']  # названия URL name из urls.py

    def location(self, item):
        return reverse(item)
