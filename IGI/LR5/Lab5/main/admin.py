# store_app/admin.py

from django.contrib import admin
from .models import (
    Client, Employee, ProductType, Manufacturer, Product,
    Order, OrderItem, CompanyInfo, NewsArticle, GlossaryTerm,
    Contact, Vacancy, Review, PromoCode
)

# Простейшая регистрация (будет использоваться стандартный интерфейс)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(ProductType)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CompanyInfo)
admin.site.register(NewsArticle)
admin.site.register(GlossaryTerm)
admin.site.register(Contact)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)
