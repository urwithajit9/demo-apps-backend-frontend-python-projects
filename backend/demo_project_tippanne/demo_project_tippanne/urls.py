# demo_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from news.views import NewsViewSet

router = DefaultRouter()
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/comments/", include("django_tippanee.urls")),
    path("api/", include(router.urls)),
]

"""
>>> user = User.objects.create_user("ajit", "ajitkumar.pu@gmail.com", "ajit")
>>> token = Token.objects.get(user=user)
>>> print(token.key)
8dc17cd3e721a72f7c276cb88946fc6b83ddac52
Username: ajitadmin
Email address: ajit.megaproject@gamil.com
ajit
"""
