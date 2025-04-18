from django.shortcuts import render, get_object_or_404
from .models import InsuranceMainCategory, InsuranceSubCategory, InsuranceProduct
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json
from .models import InsuranceLead, InsuranceProduct


class InsuranceAjaxView(View):
    def get(self, request):
        categories = InsuranceMainCategory.objects.prefetch_related('subcategories').all()

        return render(request, 'base.html',
                      {
                          'categories': categories,

                       })


def subcategory_detail(request, id):
    subcategory = get_object_or_404(InsuranceSubCategory, id=id)
    return render(request, 'insurance/subcategory_detail.html', {'subcategory': subcategory})


def load_subcategories(request):
    main_category_id = request.GET.get('main_category_id')
    subcategories = InsuranceSubCategory.objects.filter(main_category_id=main_category_id)
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


def load_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    products = InsuranceProduct.objects.filter(subcategory_id=subcategory_id)
    return JsonResponse(list(products.values('id', 'name')), safe=False)


@csrf_exempt
def submit_lead_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Получены данные:", data)
        return JsonResponse({'message': 'Спасибо, мы свяжемся с вами!'})
    return JsonResponse({'error': 'Неверный метод'}, status=400)
