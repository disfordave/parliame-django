from rest_framework import serializers
from .models import Country, Chamber, Party, Poll, PollResult


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "code", "name", "emoji"]


class ChamberSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="code", queryset=Country.objects.all()
    )

    class Meta:
        model = Chamber
        fields = ["id", "slug", "country", "name", "short_name", "total_seats"]


class PartySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="code", queryset=Country.objects.all()
    )

    class Meta:
        model = Party
        fields = [
            "id",
            "slug",
            "name",
            "short_name",
            "colour",
            "position",
            "is_independent",
            "country",
        ]


class PollResultSerializer(serializers.ModelSerializer):
    party = serializers.SlugRelatedField(
        slug_field="slug", queryset=Party.objects.all()
    )

    class Meta:
        model = PollResult
        fields = ["party", "seats", "vote_share"]


class PollSerializer(serializers.ModelSerializer):
    results = PollResultSerializer(many=True)

    chamber = serializers.SlugRelatedField(
        slug_field="slug", queryset=Chamber.objects.all()
    )

    class Meta:
        model = Poll
        fields = [
            "id",
            "slug",
            "name",
            "chamber",
            "type",
            "date",
            "polling_firm",
            "official",
            "results",
        ]

    def create(self, validated_data):
        results_data = validated_data.pop("results")
        poll = Poll.objects.create(**validated_data)

        for result_data in results_data:
            PollResult.objects.create(poll=poll, **result_data)

        return poll
