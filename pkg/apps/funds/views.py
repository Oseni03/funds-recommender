from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import FundProfileForm
from .models import Fund
from .filters import FundFilter

# Create your views here.
class FundProfileView(FormView):
    form_class = FundProfileForm
    template_name = "funds/profile.html"


class FundView(View):
    """
    List and retrieve a fund instance.
    """
    def get_object(self, request, slug):
        return get_object_or_404(Fund, slug=slug)

    def get(self, request, slug=None):
        """ Retrieve Fund(s) """
        context = {}
        if slug:
            context["fund"] = self.get_object(request, slug=slug)
            template_name = "fund.html"
        else:
            filters = FundFilter(request.GET, queryset=Fund.objects.all())
            paginator = Paginator(filters.qs, 25) # Show 25 funds per page.
            page_number = request.GET.get("page")
            context["funds"] = paginator.get_page(page_number)
            context["form"] = filters.form
            template_name = "funds.html"
        return render(request, f"funds/{template_name}", context)


class RecommendationView(LoginRequiredMixin, View):
    """
    List and retrieve recommended fund instance.
    """
    per_page = 25 # Show 25 funds per page.
    
    def get_object(self, request, slug):
        return get_object_or_404(Fund, slug=slug, profiles__user=request.user)

    def get(self, request, slug=None):
        """ Retrieve recommended fund(s) """
        context = {}
        if slug:
            context["fund"] = self.get_object(request, slug=slug)
            template_name = "fund.html"
        else:
            filters = FundFilter(request.GET, queryset=Fund.objects.filter(profiles__user=request.user))
            paginator = Paginator(filters.qs, self.per_page)
            page_number = request.GET.get("page")
            context["funds"] = paginator.get_page(page_number)
            context["form"] = filters.form
            template_name = "funds.html"
        return render(request, f"funds/{template_name}", context)