from django.urls import path
from .views import InsuranceAjaxView, get_subcategories, submit_lead_view, subcategory_detail, get_policy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', InsuranceAjaxView.as_view(), name='insurance_dynamic'),
    path('submit-lead/', submit_lead_view, name='submit_lead'),
    path('get-subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),
    path('subcategory/<int:main_id>/<int:sub_id>/', subcategory_detail, name='subcategory_detail'),
    path('policy/', get_policy, name='policy'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




