from rest_framework import serializers

from bobross.models import Paints, Episode, UserArt, User


class UserArtSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #episode_id = serializers.ReadOnlyField(source='episode.id')
    episode = serializers.PrimaryKeyRelatedField(queryset=Episode.objects.all())

    class Meta:
        model = UserArt
        fields = ('owner', 'painting', 'episode')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    paintings = serializers.HyperlinkedRelatedField(many=True,
                                                    view_name='user-art-detail',
                                                    read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'paintings')


class EpisodeSerializer(serializers.ModelSerializer):
    paintings = serializers.ReadOnlyField(source='episode.epi_paintings')

    class Meta:
        model = Episode
        fields = ('title', 'thumbnail', 'transcript', 'wordcloud', 'paints', 'paintings')


class PaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paints
        fields = ('color', 'amazon_link')