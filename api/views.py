from rest_framework import viewsets
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


class ChamberViewSet(viewsets.ModelViewSet):
    queryset = Chamber.objects.all()
    serializer_class = ChamberSerializer
    lookup_field = "slug"


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    lookup_field = "slug"


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = "slug"
