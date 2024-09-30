from rest_framework import serializers
from cinema.models import Actor, Genre, CinemaHall, Movie


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ["id", "name", "rows", "seats_in_row"]


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    duration = serializers.IntegerField()
    actors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all()
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )

    def create(self, validated_data: dict) -> Movie:
        actors = validated_data.pop("actors", [])
        genres = validated_data.pop("genres", [])
        movie = Movie.objects.create(**validated_data)
        movie.set_related_fields(actors=actors, genres=genres)
        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        actors = validated_data.pop("actors", None)
        genres = validated_data.pop("genres", None)

        instance.title = validated_data.get(
            "title",
            instance.title
        )
        instance.description = validated_data.get(
            "description",
            instance.description
        )
        instance.duration = validated_data.get(
            "duration",
            instance.duration
        )

        instance.set_related_fields(actors=actors, genres=genres)
        instance.save()
        return instance
