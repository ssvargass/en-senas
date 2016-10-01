from rest_framework import serializers

from learn.dictionary.models import (
    Word,
)

from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)

class WordSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Word
        fields = ('id', 'title', 'image', 'tags')
