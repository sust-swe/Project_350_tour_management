from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django import views
from .models import Residence
from .models import Residence
from .forms import ResidenceForm
from homepage.models import UserDetail, User
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

# Create your views here.


def register(request):
    return render(request, 'register.html')


class MyResidence(views.View):
    template_name = 'my_residence.html'

    def get(self, request):
        if request.user.is_authenticated:
            qs = Residence.objects.filter(user_detail__user=request.user)
            return render(request, self.template_name, {'qs': qs})
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class AddResidence(views.View):
    form_class = ResidenceForm
    template_name = 'add_residence.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                ob = form.save(commit=False)
                ob.user_detail = UserDetail.objects.filter(user=request.user)
                try:
                    ob.full_clean()
                    ob.save()
                    return redirect('/residence/my_residence/')
                except ValidationError as e:
                    nfe = e.message_dict[NON_FIELD_ERRORS]
                    return (request, self.template_name, {'form': form, 'nfe': nfe})
            else:
                messages.info('Invalid Credentials')
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

class ResidenceDetail(views.View):
    template_name = 'residence_detail.html'

    def get(self, request, id):
        print('hi')
        ob = Residence.objects.get(pk=id)
        return render(request, self.template_name, {'ob': ob})

class UpdateResidence(views.View):
    template_name = 'update_residence.html'
    form_class = ResidenceForm

    def get(self, request, id):
        form = ResidenceForm()