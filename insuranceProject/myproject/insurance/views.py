import json
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client

from .models import InsuranceMainCategory, InsuranceSubCategory


class InsuranceAjaxView(View):
    def get(self, request):
        main_categories = InsuranceMainCategory.objects.all()
        sub_categories = InsuranceSubCategory.objects.all()

        return render(request, 'base.html',
                      {
                          'main_categories': main_categories,
                          'sub_categories': sub_categories,
                          'category_for_option': main_categories[0] if main_categories else None

                      })


def get_subcategories(request, category_id):
    subcategories = InsuranceSubCategory.objects.filter(main_category_id=category_id)
    data = {"subcategories": list(subcategories.values("id", "name"))}
    return JsonResponse(data)


def subcategory_detail(request, main_id, sub_id):
    main_category = get_object_or_404(InsuranceMainCategory, id=main_id)
    subcategory = get_object_or_404(InsuranceSubCategory, id=sub_id)
    categories = InsuranceMainCategory.objects.all()
    return render(request, 'insurance/subcategory_detail.html',
                  {'subcategory': subcategory, 'main_category': main_category, 'categories': categories, })


# def load_subcategories(request):
#     main_category_id = request.GET.get('main_category_id')
#     subcategories = InsuranceSubCategory.objects.filter(main_category__id=main_category_id)
#     return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

load_dotenv()
def get_subcategories(request, category_id):
    subcategories = InsuranceSubCategory.objects.filter(main_category=category_id)
    data = {"subcategories": list(subcategories.values("id", "name"))}
    return JsonResponse(data)


@csrf_exempt
def submit_lead_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Вызов отправки в WhatsApp
        send_whatsapp_message(
            name=data['name'],
            phone=data['phone'],
            main_category=data['main_category'],
            subcategory=data['subcategory']
        )

        return redirect('insurance_dynamic')
    return JsonResponse({'error': 'Неверный метод'}, status=400)


def send_whatsapp_message(name, phone, main_category, subcategory):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    from_whatsapp_number = os.getenv('FROM_WHATSAPP_NUMBER')  # Twilio sandbox number
    to_whatsapp_number = os.getenv('TO_WHATSAPP_NUMBER')  # Твой номер

    client = Client(account_sid, auth_token)

    body = (
        f"📩 Новый лид\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Категория: {InsuranceMainCategory.objects.filter(id=main_category).first()}\n"
        f"Подкатегория: {InsuranceSubCategory.objects.filter(id=subcategory).first()}"
    )

    message = client.messages.create(
        body=body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    return message.sid
