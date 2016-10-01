import django_filters

from rest_framework import generics, filters
from learn.dictionary.models import Word
from learn.dictionary.serializers import WordSerializer


class WordView(generics.ListAPIView):
    """
    Returns a list of all authors.
    """
    serializer_class = WordSerializer

    def get_queryset(self):
        queryset = Word.objects.all()
        tag = self.request.GET.get('tag', None)
        if tag is not None:
            tags = tag.split(',')
            print tags
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset
