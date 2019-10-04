from django import forms, views
from datetime import datetime as dt
from django.shortcuts import render, redirect
from django.urls import path


class DateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'] = forms.ChoiceField(
            choices=[(o, o) for o in range(dt.today().year, dt.today().year+5)])
        self.fields['month'] = forms.ChoiceField(choices=[])
        self.fields['day'] = forms.ChoiceField(choices=[])


class View1(views.View):
    template_name = 'search_by_time.html'

    def get(self, request):
        form = DateForm()
        # print(form)
        return render(request, self.template_name, {'form': form})


urlpatterns = [
    path('', View1.as_view())
]
