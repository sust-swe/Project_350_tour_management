from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django import views
from .models import Guide
from.forms import GuideForm
from homepage.models import UserDetail
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
# from .models import @classname

# Create your views here.


def register(request):
    return render(request, 'register.html')


class MyGuide(views.View):
    template_name = 'my_guide.html'

    def get(self, request):
        if request.user.is_authenticated:
            qs = Guide.objects.filter(user_detail__user=request.user)
            return render(request, self.template_name, {'qs': qs})
        else:
            messages.info(request, 'You must log in to continue')
            return redirect('/')

class AddGuide(views.View):
    template_name = 'add_guide.html'
    form_class = GuideForm

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You need to log in continue')
            return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                ob = form.save(commit=False)
                ob.user_detail = UserDetail.objects.get(user=request.user)
                try:
                    ob.full_clean()
                    ob.save()
                    return redirect('/guide/my_guide/')
                except ValidationError as e:
                    nfe = e.message_dict[NON_FIELD_ERRORS]
                    return render(request, self.template_name, {'form': form, 'nfe': nfe})
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You need to log in continue')
            return redirect('/')

class GuideDetail(views.View):
    template_name = 'guide_detail.html'

    def get(self, request, id):
        guide = Guide.objects.get(pk=id)
        return render(request, self.template_name, {'guide': guide})


class UpdateGuide(views.View):
    template_name = 'update_guide.html'
    form_class = GuideForm

    def get(self, request, id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=id)
            if guide.user_detail.user == request.user:
                form = self.form_class(instance=guide)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in first')
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=id)
            if guide.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=guide)
                if form.is_valid():
                    ob = form.save(commit=False)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/guide/{}/'.format(id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You need to log in continue')
            return redirect('/')


class DeleteGuide(views.View):
    def get(self, request, id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=id)
            if guide.user_detail.user == request.user:
                guide.delete()
                return redirect('/guide/my_guide/')
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in first')
            return redirect('/')
