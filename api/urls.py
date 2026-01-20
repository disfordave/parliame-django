from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, ChamberViewSet, PartyViewSet, PollViewSet

router = DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"chambers", ChamberViewSet)
router.register(r"parties", PartyViewSet)
router.register(r"polls", PollViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
