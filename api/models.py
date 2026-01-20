from django.core.exceptions import ValidationError
from django.db import models


# 1. Country Model
class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g. "be"
    name = models.CharField(max_length=100)  # e.g. "Belgium"
    emoji = models.CharField(max_length=10, blank=True)  # e.g. "🇧🇪"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)


# 2. Chamber Model
class Chamber(models.Model):
    slug = models.CharField(max_length=50, unique=True)  # e.g. "be-federal"

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="chambers"
    )

    name = models.CharField(max_length=200)  # "De Kamer/La Chambre"
    short_name = models.CharField(max_length=50)  # "Fed"
    total_seats = models.IntegerField()  # 150

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)


# 3. Party Model
class Party(models.Model):
    slug = models.CharField(max_length=50, unique=True)  # e.g. "be-nva"

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    colour = models.CharField(max_length=20)  # Hex codes or names
    position = models.IntegerField()  # Political position (spectrum)
    is_independent = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="parties"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Parties"


# 4. Poll Model
class Poll(models.Model):
    class PollType(models.TextChoices):
        ELECTION = "election", "Election"
        POLL = "poll", "Poll"

    slug = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)

    chamber = models.ForeignKey(Chamber, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=20, choices=PollType.choices, default=PollType.POLL
    )

    date = models.DateField()

    polling_firm = models.CharField(max_length=100, blank=True, null=True)
    sample_size = models.IntegerField(blank=True, null=True)
    margin_of_error = models.FloatField(blank=True, null=True)
    official = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def country(self) -> Country:
        return self.chamber.country

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.date}"


# 5. PollResult Model
class PollResult(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="results")
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    seats = models.IntegerField(blank=True, null=True)
    vote_share = models.FloatField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.poll_id and self.party_id:
            if self.poll.chamber.country_id != self.party.country_id:
                raise ValidationError(
                    {
                        "party": "Party must belong to the same country as the poll's chamber."
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["poll", "party"], name="uniq_pollresult_poll_party"
            )
        ]

    def __str__(self):
        return f"{self.poll.name} - {self.party.short_name}"
