from django.urls import re_path
from . import views
from .views import register

urlpatterns = [
    # Публичные страницы
    re_path(r'^$', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home_alt'),
    re_path(r'^about/$', views.company_info, name='company_info'),
    re_path(r'^about/edit/$', views.company_info_edit, name='company_info_edit'),
    re_path(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    re_path(r'^register/$', register, name='register'),
    re_path(r'^products/$', views.product_list, name='product_list'),
    re_path(r'^products/(?P<pk>\d+)/$', views.product_detail, name='product_detail'),

    # Защищенные страницы
    re_path(r'^clients/$', views.client_list, name='client_list'),
    re_path(r'^clients/(?P<pk>\d+)/$', views.client_detail, name='client_detail'),

    re_path(r'^orders/$', views.order_list, name='order_list'),
    re_path(r'^orders/new/$', views.order_form, name='order_create'),
    re_path(r'^orders/(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    re_path(r'^orders/(?P<pk>\d+)/edit/$', views.order_form, name='order_edit'),
    re_path(r'^orders/(?P<pk>\d+)/delete/$', views.order_delete, name='order_delete'),

    re_path(r'^news/$', views.news_list, name='news_list'),
    re_path(r'^news/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
    re_path(r'^news/create/$', views.news_create, name='news_create'),
    re_path(r'^news/(?P<pk>\d+)/edit/$', views.news_edit, name='news_edit'),
    re_path(r'^news/(?P<pk>\d+)/delete/$', views.news_delete, name='news_delete'),

    re_path(r'^glossary/$', views.glossary_list, name='glossary_list'),
    re_path(r'^glossary/(?P<pk>\d+)/$', views.glossary_detail, name='glossary_detail'),
    re_path(r'^glossary/create/$', views.glossary_create, name='glossary_create'),
    re_path(r'^glossary/(?P<pk>\d+)/edit/$', views.glossary_edit, name='glossary_edit'),
    re_path(r'^glossary/(?P<pk>\d+)/delete/$', views.glossary_delete, name='glossary_delete'),

    re_path(r'^vacancies/$', views.vacancy_list, name='vacancy_list'),
    re_path(r'^vacancies/(?P<pk>\d+)/$', views.vacancy_detail, name='vacancy_detail'),
    re_path(r'^vacancies/create/$', views.vacancy_create, name='vacancy_create'),
    re_path(r'^vacancies/(?P<pk>\d+)/edit/$', views.vacancy_edit, name='vacancy_edit'),
    re_path(r'^vacancies/(?P<pk>\d+)/delete/$', views.vacancy_delete, name='vacancy_delete'),

    re_path(r'^reviews/$', views.review_list, name='review_list'),
    re_path(r'^reviews/create/$', views.review_create, name='review_create'),
    re_path(r'^reviews/(?P<pk>\d+)/edit/$', views.review_edit, name='review_edit'),
    re_path(r'^reviews/(?P<pk>\d+)/delete/$', views.review_delete, name='review_delete'),

    re_path(r'^promocodes/$', views.promocode_list, name='promocode_list'),
    re_path(r'^promocodes/create/$', views.promocode_create, name='promocode_create'),
    re_path(r'^promocodes/(?P<pk>\d+)/edit/$', views.promocode_edit, name='promocode_edit'),
    re_path(r'^promocodes/(?P<pk>\d+)/delete/$', views.promocode_delete, name='promocode_delete'),

    re_path(r'^contacts/$', views.contact_list, name='contact_list'),
    re_path(r'^contacts/(?P<pk>\d+)/$', views.contact_detail, name='contact_detail'),
    re_path(r'^contacts/create/$', views.contact_create, name='contact_create'),
    re_path(r'^contacts/(?P<pk>\d+)/edit/$', views.contact_edit, name='contact_edit'),
    re_path(r'^contacts/(?P<pk>\d+)/delete/$', views.contact_delete, name='contact_delete'),

    re_path(r'^profile/$', views.profile, name='profile'),

    # API endpoints
    re_path(r'^api/products/$', views.api_product_list, name='api_product_list'),
    re_path(r'^api/orders/$', views.api_order_list, name='api_order_list'),
]
