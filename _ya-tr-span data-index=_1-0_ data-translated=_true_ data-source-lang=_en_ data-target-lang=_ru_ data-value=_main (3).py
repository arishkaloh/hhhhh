## views.py
python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from myapp.models import CustomUser

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'email']  # добавьте остальные поля, которые нужно редактировать
    template_name = 'edit_profile.html'
    success_url = '/profile/edit/success/'

## settings.py
# в разделе установленные приложения добавьте 'allauth' и 'allauth.account'
INSTALLED_APPS = [
    ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    ...
]

# в разделе backend добавьте 'allauth.account.auth_backends.AuthenticationBackend'
AUTHENTICATION_BACKENDS = [
    ...
    'allauth.account.auth_backends.AuthenticationBackend',
    ...
]

# замените 'myapp.customuser' на путь к модели пользователя вашего приложения
AUTH_USER_MODEL = 'myapp.CustomUser'

# замените 'home' на имя url-шаблона, куда будет осуществлено перенаправление после успешного входа
LOGIN_REDIRECT_URL = 'home'

# разрешить получение email социальных аккаунтов
SOCIALACCOUNT_QUERY_EMAIL = True
# требовать указания email при регистрации
ACCOUNT_EMAIL_REQUIRED = True
# идентификатор сайта
SITE_ID = 1
# отключить подтверждение email
ACCOUNT_EMAIL_VERIFICATION = 'none'

# настройки для работы с google-аккаунтом
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

## urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp.views import RegisterView

urlpatterns = [
    ...
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(template_name='registration.html'), name='register'),
    ...
]

## models.py
from django.contrib.auth.models import Group
from django.db import models

# создайте группы authors и common
common_group, created = Group.objects.get_or_create(name='common')
authors_group, created = Group.objects.get_or_create(name='authors')

# добавьте пользователя в группу common
def create_user_handler(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(common_group)

# добавьте пользователя в группу authors
def create_author_handler(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(authors_group)

# зарегистрируйте обработчики сигнала
post_save.connect(create_user_handler, sender=CustomUser)
post_save.connect(create_author_handler, sender=CustomUser)

## admin.py
from django.contrib import admin
from myapp.models import Post

admin.site.register(Post)