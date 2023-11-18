import django_filters
from . import models


def applicant_types(request):
    return models.ApplicantType.objects.all()


def opportunity_categories(request):
    return models.OpportunityCategory.objects.all()


def eligibilities(request):
    return models.FundEligibility.objects.all()


class FundFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    agency = django_filters.CharFilter(lookup_expr='icontains')
    applicant_type = django_filters.ModelMultipleChoiceFilter(queryset=applicant_types)
    opportunity_category = django_filters.ModelMultipleChoiceFilter(queryset=opportunity_categories)
    eligibility = django_filters.ModelMultipleChoiceFilter(queryset=eligibilities)
    
    class Meta:
        model = models.Fund
        fields = ["title", "agency", "applicant_type", "opportunity_category", "eligibility"]