import django_filters
from . import models


def fund_types(request):
    return models.FundType.objects.all()


def fund_categories(request):
    return models.FundCategory.objects.all()


def eligibilities(request):
    return models.FundEligibility.objects.all()


class FundFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    agency = django_filters.CharFilter(lookup_expr='icontains')
    fund_type = django_filters.ModelMultipleChoiceFilter(queryset=fund_types)
    fund_category = django_filters.ModelMultipleChoiceFilter(queryset=fund_categories)
    eligibility = django_filters.ModelMultipleChoiceFilter(queryset=eligibilities)
    
    class Meta:
        model = models.Fund
        fields = ["title", "agency", "fund_type", "fund_category", "eligibility"]