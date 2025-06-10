from django import forms
from django.forms import inlineformset_factory
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json

from .models import (
    NewsArticle, Vacancy, Client, Employee,
    Order, OrderItem, GlossaryTerm,
    Review, PromoCode, Contact, CompanyInfo, Product
)

# Валидатор для телефона +375 (29) XXX-XX-XX
phone_validator = RegexValidator(
    regex=r'^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате "+375 (29) XXX-XX-XX".'
)

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['title', 'description', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'description': forms.Textarea(attrs={'rows': 8, 'cols': 60, 'required': True}),
            'address': forms.TextInput(attrs={'required': True}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['employee', 'photo', 'job_description', 'extra_phone', 'extra_email']
        widgets = {
            'employee': forms.Select(attrs={'required': True}),
            'job_description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True}),
            'extra_phone': forms.TextInput(attrs={
                'pattern': r'^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$',
                'placeholder': '+375 (29) XXX-XX-XX'
            }),
            'extra_email': forms.EmailInput(),
        }

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = [
            'code',
            'discount_type',
            'discount_value',
            'date_start',
            'date_end',
            'is_active',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'required': True}),
            'discount_type': forms.Select(attrs={'required': True}),
            'discount_value': forms.NumberInput(attrs={
                'required': True,
                'step': '0.01',
                'min': '0',  # для fixed
                'max': '100'  # общее ограничение, контролируется дополнительно
            }),
            'date_start': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'date_end': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'is_active': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        discount_type = cleaned_data.get("discount_type")
        discount_value = cleaned_data.get("discount_value")

        if discount_type == 'percent':
            if not (1 <= discount_value <= 100):
                raise ValidationError("Для процентной скидки значение должно быть от 1 до 100.")
        elif discount_type == 'fixed':
            if discount_value < 0:
                raise ValidationError("Фиксированная скидка не может быть отрицательной.")

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'number', 'min': '1', 'max': '5', 'required': True
        })
    )
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True})
        }

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'is_open']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True}),
            'is_open': forms.CheckboxInput(),
        }

class GlossaryTermForm(forms.ModelForm):
    class Meta:
        model = GlossaryTerm
        fields = ['term', 'definition']
        widgets = {
            'term': forms.TextInput(attrs={'required': True}),
            'definition': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['employee', 'delivery_date', 'delivery_address', 'comment']
        widgets = {
            'employee': forms.Select(attrs={
                'required': True
            }),
            'delivery_date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
            'delivery_address': forms.TextInput(attrs={
                'placeholder': 'Введите адрес доставки'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Дополнительные комментарии к заказу'
            })
        }

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if delivery_date and delivery_date < timezone.now().date():
            raise forms.ValidationError('Дата доставки не может быть раньше текущей даты')
        return delivery_date

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(),
            'quantity': forms.NumberInput(attrs={
                'type': 'number',
                'min': '1',
                'required': True
            })
        }

    def __init__(self, *args, products=None, **kwargs):
        super().__init__(*args, **kwargs)
        if products is not None:
            self.fields['product'].queryset = products
        else:
            self.fields['product'].queryset = Product.objects.select_related('product_type', 'manufacturer').order_by('name')

# Используем OrderItemForm в formset
OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'short_content', 'full_content', 'image', 'date_published']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'short_content': forms.Textarea(attrs={'rows': 3, 'cols': 60, 'required': True}),
            'full_content': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'required': True}),
            'image': forms.ClearableFileInput(),
            'date_published': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
            'title': 'Введите корректный email адрес'
        })
    )
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '^[А-Яа-яA-Za-z\s-]+$',
            'title': 'Имя может содержать только буквы, пробелы и дефисы'
        })
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '^[А-Яа-яA-Za-z\s-]+$',
            'title': 'Фамилия может содержать только буквы, пробелы и дефисы'
        })
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
            'placeholder': '+375 (29) XXX-XX-XX',
            'title': 'Номер телефона должен быть в формате +375 (29) XXX-XX-XX'
        }),
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Номер телефона должен быть в формате +375 (29) XXX-XX-XX'
            )
        ]
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max': timezone.now().date().isoformat(),
            'class': 'form-control'
        }),
        help_text='Вам должно быть не менее 18 лет'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def clean_date_of_birth(self):
        birth_date = self.cleaned_data.get('date_of_birth')
        if birth_date:
            today = timezone.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise forms.ValidationError('Вам должно быть не менее 18 лет для регистрации')
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update the associated Client
            Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user
