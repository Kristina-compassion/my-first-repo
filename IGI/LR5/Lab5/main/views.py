from django.shortcuts import HttpResponse
from .models import Product, Client, Employee
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, ProductType, Manufacturer
from .forms import OrderForm, OrderItemFormSet
from .models import NewsArticle
from .forms import NewsArticleForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import GlossaryTerm
from .forms import GlossaryTermForm
from .models import Vacancy
from .forms import VacancyForm
from .models import Review
from .forms import ReviewForm
from .models import PromoCode
from .forms import PromoCodeForm
from django.utils import timezone
from .models import Contact
from .forms import ContactForm
from .models import CompanyInfo
from .forms import CompanyInfoForm
import requests
import statistics
from collections import Counter
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Установка бэкенда до импорта pyplot
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import logging
from django.forms import formset_factory, ModelForm, DateInput
from django.core.exceptions import ValidationError

# Получаем логгер для нашего приложения
logger = logging.getLogger(__name__)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['employee', 'delivery_date', 'delivery_address', 'comment']
        widgets = {
            'delivery_date': DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()})
        }

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if delivery_date and delivery_date < timezone.now().date():
            raise ValidationError('Дата доставки не может быть раньше текущей даты')
        return delivery_date

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

def api_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.warning(f'Unauthorized API access attempt from {request.META.get("REMOTE_ADDR")}')
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        raise PermissionDenied
    return wrapped_view

@staff_member_required
def dashboard(request):
    logger.info(f'Dashboard accessed by staff member {request.user.username}')
    try:
        # --- Базовые данные ---
        items = OrderItem.objects.select_related(
            'product__product_type',
            'order__client',
            'order'
        ).all()
        
        products = Product.objects.all().order_by('name')
        clients = Client.objects.all().order_by('last_name', 'first_name')
        
        # --- Статистика по продажам ---
        popularity_by_type = Counter()  # количество проданных единиц
        profit_by_type = Counter()  # прибыль по типам
        monthly_sales = {}  # продажи по месяцам
        product_sales = Counter()  # продажи по продуктам
        all_sales = []  # все суммы продаж для статистики
        
        # Возраст клиентов
        client_ages = []
        for client in clients:
            age = (timezone.now().date() - client.date_of_birth).days // 365
            client_ages.append(age)
        
        # Статистика по возрасту
        age_stats = {
            'mean': round(statistics.mean(client_ages), 1) if client_ages else 0,
            'median': round(statistics.median(client_ages), 1) if client_ages else 0
        }

        # Создаем полный список месяцев для анализа
        if items:
            min_date = min(item.order.date_created for item in items)
            max_date = max(item.order.date_created for item in items)
            
            # Создаем список всех месяцев в диапазоне
            current_date = min_date.replace(day=1)
            max_date = max_date.replace(day=1)
            
            while current_date <= max_date:
                month_key = current_date.strftime('%Y-%m')
                monthly_sales[month_key] = {
                    'by_type': Counter(),
                    'total': 0,
                    'count': 0
                }
                current_date = (current_date.replace(day=1) + timezone.timedelta(days=32)).replace(day=1)

        # Собираем статистику
        for item in items:
            type_name = item.product.product_type.name
            quantity = item.quantity
            total = float(item.total_price)
            date = item.order.date_created
            
            # Популярность типов
            popularity_by_type[type_name] += quantity
            
            # Прибыль по типам
            profit_by_type[type_name] += total
            
            # Продажи по продуктам
            product_sales[item.product.name] += quantity
            
            # Все суммы продаж
            all_sales.append(total)
            
            # Месячные продажи
            month_key = date.strftime('%Y-%m')
            if month_key not in monthly_sales:
                monthly_sales[month_key] = {
                    'by_type': Counter(),
                    'total': 0,
                    'count': 0
                }
            monthly_sales[month_key]['by_type'][type_name] += total
            monthly_sales[month_key]['total'] += total
            monthly_sales[month_key]['count'] += 1

        # Статистика по суммам продаж
        sales_stats = {
            'mean': round(statistics.mean(all_sales), 2) if all_sales else 0,
            'median': round(statistics.median(all_sales), 2) if all_sales else 0
        }
        try:
            sales_stats['mode'] = round(statistics.mode(all_sales), 2)
        except statistics.StatisticsError:
            sales_stats['mode'] = 0

        # Сортировка и преобразование в списки
        most_popular = dict(sorted(
            popularity_by_type.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        most_profitable = dict(sorted(
            profit_by_type.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        # Товары без продаж
        unsold_products = [p.name for p in products if p.name not in product_sales]
        
        # Получаем списки для графиков
        popular_types = list(most_popular.keys())
        popular_values = list(most_popular.values())
        profitable_types = list(most_profitable.keys())
        profitable_values = list(most_profitable.values())

        # --- Построение графиков ---
        
        # 1. Столбчатая диаграмма популярности товаров
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(popular_types, popular_values)
        ax1.set_title('Популярность типов товаров (количество проданных единиц)')
        ax1.set_xlabel('Тип товара')
        ax1.set_ylabel('Количество')
        plt.xticks(rotation=45)
        fig1.tight_layout()
        buf1 = io.BytesIO()
        fig1.savefig(buf1, format='png')
        plt.close(fig1)
        popularity_chart = base64.b64encode(buf1.getvalue()).decode()

        # 2. Столбчатая диаграмма прибыли
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.bar(profitable_types, profitable_values)
        ax2.set_title('Прибыль по типам товаров')
        ax2.set_xlabel('Тип товара')
        ax2.set_ylabel('Сумма (руб.)')
        plt.xticks(rotation=45)
        fig2.tight_layout()
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format='png')
        plt.close(fig2)
        profit_chart = base64.b64encode(buf2.getvalue()).decode()

        return render(request, 'main/dashboard.html', {
            # Списки клиентов и товаров
            'clients': clients,
            'products': products,
            
            # Статистика продаж
            'total_sales': sum(all_sales),
            'sales_stats': sales_stats,
            'age_stats': age_stats,
            
            # Популярность и прибыльность
            'most_popular': most_popular,
            'most_profitable': most_profitable,
            'unsold_products': unsold_products,
            
            # Данные по месяцам
            'monthly_sales': monthly_sales,
            
            # Графики
            'popularity_chart': popularity_chart,
            'profit_chart': profit_chart,
            
            # Списки для шаблона
            'popular_types': popular_types,
            'popular_values': popular_values,
            'profitable_types': profitable_types,
            'profitable_values': profitable_values,
        })
    except Exception as e:
        logger.error(f'Error in dashboard view: {str(e)}', exc_info=True)
        raise


@login_required
def profile(request):
    user = request.user

    # Профиль клиента
    client_profile = None
    try:
        client_profile = Client.objects.get(user=user)
    except Client.DoesNotExist:
        pass

    # Профиль сотрудника
    employee_profile = None
    if user.is_staff:
        try:
            employee_profile = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            pass

    # Заказы клиента
    client_orders = Order.objects.none()
    if client_profile:
        client_orders = Order.objects.filter(client=client_profile) \
                                     .order_by('-date_created')

    # Заказы сотрудника
    staff_orders = Order.objects.none()
    if employee_profile:
        staff_orders = Order.objects.filter(employee=employee_profile) \
                                    .order_by('-date_created')

    return render(request, 'main/profile.html', {
        'client_profile': client_profile,
        'employee_profile': employee_profile,
        'client_orders': client_orders,
        'staff_orders': staff_orders,
    })

# Публичные страницы
def home(request):
    logger.debug(f'Home page accessed by {"authenticated" if request.user.is_authenticated else "anonymous"} user')
    try:
        latest = NewsArticle.objects.order_by('-date_published').first()
        quote = {}
        try:
            resp = requests.get('https://favqs.com/api/qotd')
            data = resp.json()
            q = data.get('quote', {})
            quote = {
                'body': q.get('body', ''),
                'author': q.get('author', 'Unknown')
            }
        except Exception as e:
            logger.warning(f'Failed to fetch quote: {str(e)}')
            quote = {'body': 'Не удалось получить цитату.', 'author': ''}

        joke = {}
        try:
            r = requests.get('https://official-joke-api.appspot.com/random_joke')
            j = r.json()
            joke = {'setup': j['setup'], 'punchline': j['punchline']}
        except Exception as e:
            logger.warning(f'Failed to fetch joke: {str(e)}')
            joke = {'setup': 'Ошибка при получении шутки', 'punchline': ''}

        return render(request, 'main/home.html', {
            'latest': latest,
            'quote': quote,
            'joke': joke,
        })
    except Exception as e:
        logger.error(f'Error in home view: {str(e)}', exc_info=True)
        raise

def company_info(request):
    info = CompanyInfo.objects.order_by('-pk').first()
    return render(request, 'main/company_info.html', {'info': info})

@staff_member_required
def company_info_edit(request):
    info = CompanyInfo.objects.order_by('-pk').first()
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            return redirect('company_info')
    else:
        form = CompanyInfoForm(instance=info)
    action = 'Редактировать' if info else 'Создать'
    return render(request, 'main/company_info_form.html', {
        'form': form,
        'action': action
    })

def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')


def contact_list(request):
    contacts = Contact.objects.select_related('employee').all().order_by('employee__last_name')
    return render(request, 'main/contact_list.html', {'contacts': contacts})

def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'main/contact_detail.html', {'contact': contact})

@staff_member_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'main/contact_form.html', {'form': form, 'action': 'Добавить контакт'})

@staff_member_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_detail', pk=pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'main/contact_form.html', {'form': form, 'action': 'Редактировать контакт'})

@staff_member_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'main/contact_confirm_delete.html', {'contact': contact})

def promocode_list(request):
    """
    Публичный список кодов, которые активны и текуще действуют.
    """
    now = timezone.now()
    promocodes = PromoCode.objects.filter(
        is_active=True,
        date_start__lte=now,
        date_end__gte=now
    ).order_by('date_end')
    return render(request, 'main/promocode_list.html', {'promocodes': promocodes})

@staff_member_required
def promocode_create(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promocode_list')
    else:
        form = PromoCodeForm()
    return render(request, 'main/promocode_form.html', {
        'form': form,
        'action': 'Создать промокод'
    })

@staff_member_required
def promocode_edit(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        form = PromoCodeForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            return redirect('promocode_list')
    else:
        form = PromoCodeForm(instance=promo)
    return render(request, 'main/promocode_form.html', {
        'form': form,
        'action': 'Редактировать промокод'
    })

@staff_member_required
def promocode_delete(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        promo.delete()
        return redirect('promocode_list')
    return render(request, 'main/promocode_confirm_delete.html', {
        'promocode': promo
    })

def review_list(request):
    """
    Показываем только опубликованные отзывы
    """
    reviews = Review.objects.filter(is_published=True).order_by('-date_created')
    return render(request, 'main/review_list.html', {'reviews': reviews})

@login_required
def review_create(request):
    """
    Любой залогиненный пользователь может оставить отзыв.
    Поле author заполняется из request.user.
    is_published=False по умолчанию — модерация в админке.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.is_published = True
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'main/review_form.html', {'form': form, 'action': 'Оставить отзыв'})

@staff_member_required
def review_edit(request, pk):
    """
    Редактирование (модерация) отзыва: можно сразу менять is_published в админке, 
    но в сайте пусть сотрудник может редактировать текст и публикацию.
    """
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        # добавим возможность менять is_published через отдель поле
        is_pub = request.POST.get('is_published') == 'on'
        if form.is_valid():
            rev = form.save(commit=False)
            rev.is_published = is_pub
            rev.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'main/review_form.html', {
        'form': form,
        'action': 'Редактировать отзыв',
        'can_publish': True,
        'is_published': review.is_published,
    })

@staff_member_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'main/review_confirm_delete.html', {'review': review})


def vacancy_list(request):
    """
    Публичный список вакансий (открытые вверху).
    """
    vacancies = Vacancy.objects.order_by('-date_posted')
    return render(request, 'main/vacancy_list.html', {'vacancies': vacancies})

def vacancy_detail(request, pk):
    """
    Публичная детальная страница вакансии.
    """
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'main/vacancy_detail.html', {'vacancy': vacancy})

@staff_member_required
def vacancy_create(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancy_list')
    else:
        form = VacancyForm()
    return render(request, 'main/vacancy_form.html', {'form': form, 'action': 'Добавить вакансию'})

@staff_member_required
def vacancy_edit(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('vacancy_detail', pk=pk)
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, 'main/vacancy_form.html', {'form': form, 'action': 'Редактировать вакансию'})

@staff_member_required
def vacancy_delete(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST':
        vacancy.delete()
        return redirect('vacancy_list')
    return render(request, 'main/vacancy_confirm_delete.html', {'vacancy': vacancy})


def glossary_list(request):
    """
    Публичный список терминов, отсортированных по дате добавления (новые снизу).
    """
    terms = GlossaryTerm.objects.order_by('term')
    return render(request, 'main/glossary_list.html', {'terms': terms})

def glossary_detail(request, pk):
    """
    Публичная страница термина.
    """
    term = get_object_or_404(GlossaryTerm, pk=pk)
    return render(request, 'main/glossary_detail.html', {'term': term})

@staff_member_required
def glossary_create(request):
    if request.method == 'POST':
        form = GlossaryTermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('glossary_list')
    else:
        form = GlossaryTermForm()
    return render(request, 'main/glossary_form.html', {'form': form, 'action': 'Добавить термин'})

@staff_member_required
def glossary_edit(request, pk):
    term = get_object_or_404(GlossaryTerm, pk=pk)
    if request.method == 'POST':
        form = GlossaryTermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('glossary_detail', pk=pk)
    else:
        form = GlossaryTermForm(instance=term)
    return render(request, 'main/glossary_form.html', {'form': form, 'action': 'Редактировать термин'})

@staff_member_required
def glossary_delete(request, pk):
    term = get_object_or_404(GlossaryTerm, pk=pk)
    if request.method == 'POST':
        term.delete()
        return redirect('glossary_list')
    return render(request, 'main/glossary_confirm_delete.html', {'term': term})

# Защищенные страницы (требуют авторизации)
@staff_member_required
def client_list(request):
    clients = Client.objects.all().order_by('last_name', 'first_name')
    return render(request, 'main/client_list.html', {'clients': clients})

@staff_member_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'main/client_detail.html', {'client': client})

@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.select_related('client', 'employee').order_by('-date_created')
    else:
        client_profile, created = Client.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'date_of_birth': '1900-01-01',
                'phone': '',
                'email': request.user.email,
                'address': '',
            }
        )
        orders = Order.objects.filter(client=client_profile).order_by('-date_created')

    return render(request, 'main/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff and order.client.user != request.user:
        raise PermissionDenied
    items = order.order_items.select_related('product')
    return render(request, 'main/order_detail.html', {
        'order': order,
        'items': items,
    })

@login_required
def order_form(request, pk=None):
    """
    Форма создания/редактирования заказа
    """
    # Получаем профиль клиента
    client_profile = None
    if not request.user.is_staff:
        client_profile = Client.objects.get(user=request.user)

    # Получаем заказ если редактируем
    order = None
    if pk:
        order = get_object_or_404(Order, pk=pk)
        if not request.user.is_staff and order.client.user != request.user:
            raise PermissionDenied

    # Получаем список товаров для фильтрации
    products = Product.objects.select_related('product_type', 'manufacturer')
    if request.method == 'POST':
        # Фильтруем товары если применены фильтры
        if request.POST.get('category'):
            products = products.filter(product_type_id=request.POST['category'])
        if request.POST.get('manufacturer'):
            products = products.filter(manufacturer_id=request.POST['manufacturer'])
        if request.POST.get('search'):
            products = products.filter(name__icontains=request.POST['search'])

        if 'save_order' in request.POST:
            form = OrderForm(request.POST, instance=order)
            formset = OrderItemFormSet(request.POST, instance=order)
            
            if form.is_valid() and formset.is_valid():
                # Сохраняем основную форму заказа
                order = form.save(commit=False)
                if not request.user.is_staff:
                    order.client = client_profile
                order.save()
                
                # Сохраняем формсет с привязкой к заказу
                formset.instance = order
                formset.save()
                
                return redirect('order_list')
        else:
            form = OrderForm(instance=order)
            formset = OrderItemFormSet(instance=order)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    # Настраиваем форму в зависимости от типа пользователя
    if not request.user.is_staff:
        if client_profile:
            form.fields['delivery_address'].initial = client_profile.address
        if 'employee' in form.fields:
            form.fields.pop('employee')

    context = {
        'form': form,
        'formset': formset,
        'products': products,
        'action': 'Изменить заказ' if pk else 'Создать заказ',
        'categories': ProductType.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'employees': Employee.objects.all(),
    }
    return render(request, 'main/order_form.html', context)

@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff and order.client.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order, user=request.user)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order, user=request.user)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'main/order_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Редактировать заказ',
    })

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff and order.client.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'main/order_confirm_delete.html', {'order': order})

def news_list(request):
    """
    Список всех новостей, отсортированных по дате (сначала новые).
    """
    articles = NewsArticle.objects.order_by('-date_published')
    return render(request, 'main/news_list.html', {'articles': articles})


def news_detail(request, pk):
    """
    Детальная страница новости.
    """
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, 'main/news_detail.html', {'article': article})

@staff_member_required
def news_create(request):
    """
    Форма создания новости.
    """
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsArticleForm()
    return render(request, 'main/news_form.html', {'form': form, 'action': 'Создать новость'})

@staff_member_required
def news_edit(request, pk):
    """
    Форма редактирования новости.
    """
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=pk)
    else:
        form = NewsArticleForm(instance=article)
    return render(request, 'main/news_form.html', {'form': form, 'action': 'Редактировать новость'})

@staff_member_required
def news_delete(request, pk):
    """
    Подтверждение удаления новости.
    """
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('news_list')
    return render(request, 'main/news_confirm_delete.html', {'article': article})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def product_list(request):
    logger.debug('Product list accessed')
    try:
        qs = Product.objects.select_related('product_type', 'manufacturer')

        # Поиск
        q = request.GET.get('q', '').strip()
        if q:
            logger.info(f'Product search query: {q}')
            qs = qs.filter(name__icontains=q)

        # Фильтры
        category = request.GET.get('category')
        if category:
            logger.debug(f'Product filter by category: {category}')
            qs = qs.filter(product_type_id=category)

        manufacturer = request.GET.get('manufacturer')
        if manufacturer:
            logger.debug(f'Product filter by manufacturer: {manufacturer}')
            qs = qs.filter(manufacturer_id=manufacturer)

        # Сортировка
        sort = request.GET.get('sort')
        allowed = ('price', '-price')
        if sort in allowed:
            qs = qs.order_by(sort)
        else:
            if sort:
                logger.warning(f'Invalid sort parameter: {sort}')
            qs = qs.order_by('name')

        return render(request, 'main/product_list.html', {
            'products': qs,
            'categories': ProductType.objects.all(),
            'manufacturers': Manufacturer.objects.all(),
            'current_q': q,
            'current_category': category,
            'current_manufacturer': manufacturer,
            'current_sort': sort,
            'user_authenticated': request.user.is_authenticated,
        })
    except Exception as e:
        logger.error(f'Error in product_list view: {str(e)}', exc_info=True)
        raise

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {
        'product': product,
        'user_authenticated': request.user.is_authenticated,
    })

# API эндпоинты
@api_login_required
def api_product_list(request):
    products = Product.objects.select_related('product_type', 'manufacturer').all()
    data = [{
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'type': p.product_type.name,
        'manufacturer': p.manufacturer.name
    } for p in products]
    return JsonResponse({'products': data})

@api_login_required
def api_order_list(request):
    if request.user.is_staff:
        orders = Order.objects.select_related('client').all()
    else:
        client = Client.objects.get(user=request.user)
        orders = Order.objects.filter(client=client)
    
    data = [{
        'id': o.id,
        'date': o.date_created.isoformat(),
        'total': float(o.total_price),
        'status': o.status
    } for o in orders]
    return JsonResponse({'orders': data})