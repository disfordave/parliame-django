from django.contrib import admin
from .models import Country, Chamber, Party, Poll, PollResult


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "emoji", "created_at")
    search_fields = ("name", "code")


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name", "country", "position", "is_independent")
    list_filter = ("country", "is_independent")
    search_fields = ("name", "short_name")


@admin.register(Chamber)
class ChamberAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "country", "total_seats")
    list_filter = ("country",)
    search_fields = ("name", "short_name")


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("slug", "chamber", "created_at", "date")
    list_filter = ("chamber", "date")
    search_fields = ("slug",)


@admin.register(PollResult)
class PollResultAdmin(admin.ModelAdmin):
    list_display = ("poll", "party", "seats", "vote_share")
    list_filter = ("poll", "party")
