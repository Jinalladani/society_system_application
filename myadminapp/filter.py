from django.db.models import Q
import django_filters
from myapp.models import Society


class SocietyListFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Society
        fields = ['q']
