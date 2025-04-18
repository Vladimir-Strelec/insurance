from django.urls import path
from .views import InsuranceAjaxView, load_subcategories, load_products, submit_lead_view, subcategory_detail

urlpatterns = [
    path('insurance-dynamic/', InsuranceAjaxView.as_view(), name='insurance_dynamic'),
    path('submit-lead/', submit_lead_view, name='submit_lead'),
    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
    path('subcategory/<int:id>/', subcategory_detail, name='subcategory_detail'),
    path('ajax/load-products/', load_products, name='ajax_load_products'),
]

