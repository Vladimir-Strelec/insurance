import json
import os

from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from twilio.rest import Client
from django.views.generic import TemplateView
from .models import MainCategory, SubCategory
from .models import Story

load_dotenv()


from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from .models import MainCategory, SubCategory, InsuranceLead
from .forms import LeadForm


class HomeView(ListView):
    model = MainCategory
    template_name = "home.html"
    context_object_name = 'main_categories'


    def get_queryset(self):
        self.main_categories = MainCategory.objects.all()
        self.main_category = MainCategory.objects.first()
        self.subcategory = SubCategory.objects.first()
        self.stories = Story.objects.all().order_by('-created_at')
        return self.stories

    def post(self, request, *args, **kwargs):
        form = LeadForm(request.POST)
        if form.is_valid():
            send_whatsapp_message(
                name=form.cleaned_data.get('full_name'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone'),
                message=form.cleaned_data.get('message'),
                main_category=None,
                subcategory=None
            )
            messages.success(request, "Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet.")
            return self.get(request)  # повторный GET для рендера страницы с сообщением
        else:
            self.form = form
            return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['stories'] = self.stories
        context['main_categories'] = self.main_categories
        context['subcategory'] = self.subcategory
        context['main_category'] = self.main_category
        context['form'] = getattr(self, 'form', LeadForm())
        return context




class MainCategoryListView(ListView):
    model = MainCategory
    template_name = 'categories/main_category_list.html'
    context_object_name = 'main_categories'


class SubCategoryListView(ListView):
    template_name = 'categories/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        self.main_category = get_object_or_404(MainCategory, slug=self.kwargs['main_slug'])
        self.main_categories = MainCategory.objects.all()
        return SubCategory.objects.filter(main_category=self.main_category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_category'] = self.main_category
        context['main_categories'] = self.main_categories
        return context


class SubCategoryDetailListView(ListView):
    template_name = 'categories/subcategory_detail.html'
    context_object_name = 'subcategory'

    def get_queryset(self):
        self.main_category = get_object_or_404(MainCategory, slug=self.kwargs['main_slug'])
        self.sub_category = get_object_or_404(SubCategory, main_category=self.main_category, slug=self.kwargs['sub_slug'])
        self.main_categories = MainCategory.objects.all()

        return self.main_category, self.sub_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_category'] = self.main_category
        context['sub_category'] = self.sub_category
        context['main_categories'] = self.main_categories
        return context


class LeadCreateView(CreateView):
    model = InsuranceLead
    form_class = LeadForm
    template_name = 'categories/lead_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.main_category = get_object_or_404(MainCategory, slug=self.kwargs['main_slug'])
        self.subcategory = get_object_or_404(SubCategory, slug=self.kwargs['sub_slug'], main_category=self.main_category)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.subcategory = self.subcategory
        response = super().form_valid(form)
        messages.success(self.request, "Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet.")

        # 🟢 Отправка WhatsApp-сообщения
        send_whatsapp_message(
            name=form.cleaned_data.get('full_name'),
            email=form.cleaned_data.get('email'),
            phone=form.cleaned_data.get('phone'),
            message=form.cleaned_data.get('message'),
            main_category=self.main_category.id,
            subcategory=self.subcategory.id
        )

        return response

    def get_success_url(self):
        return self.request.path + '?success=1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        context['main_category'] = self.main_category
        return context




@csrf_exempt
def submit_lead_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Вызов отправки в WhatsApp
        send_whatsapp_message(name=data['name'], phone=data['phone'], main_category=data['main_category'],
                              subcategory=data['subcategory'])

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Неверный метод'}, status=400)


def send_whatsapp_message(name, email, phone, message, main_category, subcategory):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    from_whatsapp_number = os.getenv('FROM_WHATSAPP_NUMBER')
    to_whatsapp_number = os.getenv('TO_WHATSAPP_NUMBER')
    client = Client(account_sid, auth_token)

    main = MainCategory.objects.filter(id=main_category).first()
    sub = SubCategory.objects.filter(id=subcategory).first()

    body = (
        f"📩 Новый лид\n"
        f"Имя: {name}\n"
        f"Emeil: {email}\n"
        f"Телефон: {phone}\n"
        f"Сообщение: {message}\n"
        f"Категория: {main.name if main else '—'}\n"
        f"Подкатегория: {sub.name if sub else '—'}"
    )

    message = client.messages.create(
        body=body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    return message.sid


def get_policy(requets):
    return render(requets, 'policy.html', {})


def story_list(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'story_list.html', {'stories': stories})


def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    return render(request, 'story_detail.html', {'story': story})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://inschurance.de/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
