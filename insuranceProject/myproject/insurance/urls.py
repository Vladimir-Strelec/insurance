from django.urls import path
from .views import InsuranceAjaxView, get_subcategories, submit_lead_view, subcategory_detail

urlpatterns = [
    path('', InsuranceAjaxView.as_view(), name='insurance_dynamic'),
    path('submit-lead/', submit_lead_view, name='submit_lead'),
    path('get-subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),
    path('subcategory/<int:main_id>/<int:sub_id>/', subcategory_detail, name='subcategory_detail'),

]


