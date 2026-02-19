from rest_framework.routers import SimpleRouter
from .views import DropBoxViewset
from django.urls import path
from .views import UserProfileView

router = SimpleRouter()
router.register("accounts", DropBoxViewset)
urlpatterns = router.urls

urlpatterns += [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
