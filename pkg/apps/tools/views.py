from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from apps.funds.models import FundProfile
from .forms import WritingToolForm
# from .utils import get_writer_chain

# Create your views here.
class WriterView(LoginRequiredMixin, View):
    template_name = "tools/writing.html"
    form_class = WritingToolForm 
    
    def get(self, request, *args, **kwargs):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            profile_id = form.cleaned_data.get("profile")
            question = form.cleaned_data.get("question")
            style = form.cleaned_data.get("style")
            add_profile_summary = form.cleaned_data.get("add_profile_summary")
            
            profile = get_object_or_404(FundProfile, id=profile_id, user=request.user)
            
            writer_chain = get_writer_chain(add_profile_summary)
            
            if add_profile_summary:
                response = writer_chain.predict(
                    question=question, 
                    formatted_tone=form.formatted_tones, 
                    writing_style=style, 
                    summary=profile.summary
                )
            else:
                response = writer_chain.predict(
                    question=question, 
                    formatted_tone=form.formatted_tones, 
                    writing_style=style
                )
            
            context["response"] = response
            
            if request.htmx:
                return render(request, "tools/partials/_response.html", context)
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return render(request, self.template_name, context)