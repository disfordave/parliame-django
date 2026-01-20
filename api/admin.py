from django.contrib import admin
from .models import Country, Chamber, Party, Poll, PollResult

admin.site.register(Country)
admin.site.register(Chamber)
admin.site.register(Party)
admin.site.register(Poll)
admin.site.register(PollResult)
