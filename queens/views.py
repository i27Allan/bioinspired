from django.shortcuts import render
from django.views import View
from queens.forms import *
from queens.api import solver


# Create your views here.
class IndexView(View):
    form = OptionsForm

    def get(self, request):
        form = self.form()
        return render(request, 'index.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
        return render(request, 'index.html', locals())
