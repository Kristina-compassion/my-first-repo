# store_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse


# 1. Клиент (покупатель)
class Client(models.Model):
    # Ссылка на встроенную User (если планируем логин через auth.User)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile',
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone_regex = RegexValidator(
        regex=r'^\+375\s?\(?(17|25|29|33|44)\)?\s?\d{3}-\d{2}-\d{2}$',
        message='Телефон должен быть в формате +375 (XX) XXX-XX-XX'
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        unique=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    address = models.CharField(max_length=255, verbose_name='Адрес проживания')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if self.date_of_birth:
            age = (timezone.now().date() - self.date_of_birth).days / 365
            if age < 18:
                raise ValidationError("Клиент должен быть старше 18 лет.")


# 2. Сотрудник
class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone_regex = RegexValidator(
        regex=r'^\+375\s?\(?(17|25|29|33|44)\)?\s?\d{3}-\d{2}-\d{2}$',
        message='Телефон должен быть в формате +375 (XX) XXX-XX-XX'
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        unique=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    # Можно сделать OneToOne c User, если хотим авторизовать сотрудников:
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='employee_profile',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.position}"

    def clean(self):
        if self.date_of_birth:
            age = (timezone.now().date() - self.date_of_birth).days / 365
            if age < 18:
                raise ValidationError("Клиент должен быть старше 18 лет.")


# 3. Вид товара
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    def __str__(self):
        return self.name


# 4. Производитель
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название производителя')
    country = models.CharField(max_length=100, verbose_name='Страна')
    contact_info = models.TextField(blank=True, verbose_name='Контактная информация')

    def __str__(self):
        return self.name


# 5. Товар
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Тип товара'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Производитель'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.manufacturer.name})'

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        if self.quantity < 0:
            raise ValidationError('Количество не может быть отрицательным')

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': str(self.product_type_id),
            'manufacturer_id': str(self.manufacturer_id),
            'price': str(self.price),
            'quantity': self.quantity
        }


# 14. Промокоды/Купоны (PromoCode)
class PromoCode(models.Model):
    PERCENT = 'percent'
    FIXED   = 'fixed'
    DISCOUNT_TYPE_CHOICES = [
        (PERCENT, 'Процент'),
        (FIXED,   'Фиксированная сумма'),
    ]

    code           = models.CharField(max_length=50, unique=True, verbose_name='Код промокода')
    discount_type  = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default=PERCENT)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    date_start     = models.DateTimeField()
    date_end       = models.DateTimeField()
    is_active      = models.BooleanField(default=True)
    clients_used   = models.ManyToManyField('Client', blank=True, related_name='used_promocodes')

    def __str__(self):
        return self.code

    def is_currently_valid(self):
        now = timezone.now()
        return self.is_active and (self.date_start <= now <= self.date_end)

    def calculate_discount(self, total_amount):
        if not self.is_currently_valid():
            return 0
        if self.discount_type == self.PERCENT:
            return (total_amount * self.discount_value / 100).quantize(self.discount_value)
        return min(self.discount_value, total_amount)


# 6. Заказ (Order)
class Order(models.Model):
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='Клиент'
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_orders',
        verbose_name='Сотрудник, оформивший заказ'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
    )
    delivery_date = models.DateField(verbose_name='Дата доставки')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    total_sum = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Общая сумма заказа'
    )

    def clean(self):
        if self.delivery_date and self.delivery_date <= timezone.now().date():
            raise ValidationError({'delivery_date': 'Дата доставки должна быть больше текущей даты'})
        
        if self.delivery_address and len(self.delivery_address) < 10:
            raise ValidationError({'delivery_address': 'Адрес доставки должен быть более подробным'})

    def update_total(self):
        """Обновляет общую сумму заказа на основе позиций"""
        total = sum(item.total_price for item in self.order_items.all())
        self.total_sum = total
        self.save()

    def __str__(self):
        return f'Заказ {self.id} от {self.date_created.strftime("%d.%m.%Y")}'

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# 7. Позиция заказа (OrderItem)
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена на момент заказа'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Итоговая стоимость позиции'
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        # При сохранении автоматически заполняем price_at_order и total_price
        if not self.price_at_order:
            self.price_at_order = self.product.price
        self.total_price = self.price_at_order * self.quantity
        super().save(*args, **kwargs)
        # После сохранения позиции обновляем общую сумму заказа
        self.order.update_total()


# 8. Информация о компании (CompanyInfo)
class CompanyInfo(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название компании')
    description = models.TextField(verbose_name='Описание компании')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    # Можно добавить логотип:
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.title
    


# 9. Новости/Статьи (NewsArticle)
class NewsArticle(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_content = models.CharField(max_length=255, verbose_name='Краткое содержание')
    full_content = models.TextField(verbose_name='Полный текст статьи')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    date_published = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title


# 10. Словарь терминов (GlossaryTerm)
class GlossaryTerm(models.Model):
    term = models.CharField(max_length=100, unique=True, verbose_name='Термин')
    definition = models.TextField(verbose_name='Определение')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.term


# 11. Контакты сотрудников (Contact) – связь с Employee (OneToOne)
class Contact(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='contact_info',
        verbose_name='Сотрудник'
    )
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    job_description = models.TextField(verbose_name='Описание выполняемых работ')
    # Поля телефона и email сотрудника мы уже задали в Employee, здесь можно указать дополнительных:
    extra_phone = models.CharField(max_length=20, blank=True, verbose_name='Доп. телефон')
    extra_email = models.EmailField(blank=True, verbose_name='Доп. Email')

    def __str__(self):
        return f"Контакты {self.employee.first_name} {self.employee.last_name}"


# 12. Вакансии (Vacancy)
class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание вакансии')
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_open = models.BooleanField(default=True, verbose_name='Открыта/Закрыта')

    def __str__(self):
        return self.title


# 13. Отзывы (Review)
class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован/На модерации')

    def __str__(self):
        return f"Отзыв #{self.id} — {self.author.username} ({self.rating})"