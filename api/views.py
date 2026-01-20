from rest_framework import viewsets

from api.permissions import IsAdminOrReadOnly
from .models import Country, Chamber, Party, Poll
from .serializers import (
    CountrySerializer,
    ChamberSerializer,
    PartySerializer,
    PollSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "code"
    permission_classes = [IsAdminOrReadOnly]


class ChamberViewSet(viewsets.ModelViewSet):
    queryset = Chamber.objects.all()
    serializer_class = ChamberSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["country"]


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["country", "is_independent"]


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["chamber", "official", "type", "date"]
