import json
import os

from django.contrib import messages
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from dotenv import load_dotenv
from twilio.rest import Client


from .models import Story

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import models
from django.utils.text import slugify


from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from .models import MainCategory, SubCategory, InsuranceLead
from .forms import LeadForm

load_dotenv()





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
            return self.get(request)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_category = None
        self.main_categories = None

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


@method_decorator(csrf_protect, name="dispatch")
class LeadCreateView(CreateView):
    model = InsuranceLead
    form_class = LeadForm
    http_method_names = ["post"]  # никаких GET -> шаблон не нужен

    def dispatch(self, request, *args, **kwargs):
        self.main_category = get_object_or_404(MainCategory, slug=kwargs["main_slug"])
        self.subcategory = get_object_or_404(
            SubCategory, slug=kwargs["sub_slug"], main_category=self.main_category
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    # маппим name -> full_name, если фронт прислал старое имя поля
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = kwargs.get("data")
        if data:
            data = data.copy()
            if not data.get("full_name") and data.get("name"):
                data["full_name"] = data["name"]
            kwargs["data"] = data
        return kwargs

    def form_invalid(self, form):
        # ошибки — JSON 400, HTMX сам не будет ничего вставлять при hx-swap="none"
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    def form_valid(self, form):
        form.instance.subcategory = self.subcategory
        if hasattr(form.instance, "main_category"):
            form.instance.main_category = self.main_category

        self.object = form.save()

        # WhatsApp не роняет ответ
        try:
            cd = form.cleaned_data
            send_whatsapp_message(
                name=cd.get("full_name") or cd.get("name") or "",
                email=cd.get("email") or "",
                phone=cd.get("phone") or "",
                message=cd.get("message") or "",
                main_category=self.main_category.id,
                subcategory=self.subcategory.id,
            )
        except Exception:
            pass

        if self.request.headers.get("HX-Request"):
            # отдаём пустой 204 и триггерим клиентское событие с полезной нагрузкой
            payload = {
                "name": cd.get("full_name") or cd.get("name") or "",
                "main": self.main_category.name,
                "sub": self.subcategory.name,
            }
            resp = HttpResponse(status=204)
            resp["HX-Trigger"] = json.dumps({"lead:created": payload})
            return resp

        # не-HTMX: просто JSON "ok"
        return JsonResponse({"ok": True, "id": self.object.id})


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
    main_categories = MainCategory.objects.all()
    return render(request, 'story_detail.html', {'story': story, 'main_categories': main_categories})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://inschurance.de/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def api_subcategories(request: HttpRequest):
    main = request.GET.get("main") or request.GET.get("main_category")
    if not main:
        return JsonResponse({"error": "missing main"}, status=400)
    try:
        main_id = int(main)
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid main"}, status=400)

    qs = (SubCategory.objects
          .filter(main_category=main_id)
          .values("id", "name", "slug")
          .order_by("name"))

    data = [{"id": r["id"], "name": r["name"], "slug": r["slug"] or slugify(r["name"])} for r in qs]
    return JsonResponse(data, safe=False)