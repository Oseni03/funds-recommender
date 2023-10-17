from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
            profile = form.cleaned_data.get("profile")
            query = form.cleaned_data.get("query")
            
            if "writer_chain" not in request.session:
                writer_chain = get_writer_chain()
                request.session["writer_chain"] = writer_chain
            else:
                writer_chain = request.session.get("writer_chain")
            
            response = writer_chain.predict(question=query, summary=profile.summary)
            
            context["response"] = response
            
            if request.htmx:
                return render(request, "tools/partials/_response.html", context)
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return render(request, self.template_name, context)