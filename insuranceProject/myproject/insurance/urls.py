from django.urls import path
from .views import get_policy, robots_txt, story_detail, story_list, MainCategoryListView, SubCategoryListView, \
    LeadCreateView, HomeView, SubCategoryDetailListView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [

    path('stories/', story_list, name='story_list'),
    path('story/<slug:slug>/', story_detail, name='story_detail'),

    path('', HomeView.as_view(), name='home'),
    path('inschurances/', MainCategoryListView.as_view(), name='main_category_list'),
    path('<slug:main_slug>/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('<slug:main_slug>/<slug:sub_slug>/detail/', SubCategoryDetailListView.as_view(), name='subcategory_detail'),
    path('<slug:main_slug>/<slug:sub_slug>/', LeadCreateView.as_view(), name='lead_create'),
    # path('', InsuranceAjaxView.as_view(), name='insurance_dynamic'),
    # path('submit-lead/', submit_lead_view, name='submit_lead'),
    # path('get-subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),
    # path('subcategory/<int:main_id>/<int:sub_id>/', subcategory_detail, name='subcategory_detail'),
    # path('policy/', get_policy, name='policy'),



    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("robots.txt", robots_txt),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




