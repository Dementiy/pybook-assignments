from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'title', 'body', 'pub_date')

