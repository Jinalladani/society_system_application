from django.db.models import Q
import django_filters
from .models import Income_Expense_LedgerValue


class Income_Expense_LedgerFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Income_Expense_LedgerValue
        fields = ['q']
