from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, View

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
            context["funds"] = filters.qs
            context["form"] = filters.form
            template_name = "funds.html"
        return render(request, f"funds/{template_name}", context)
    