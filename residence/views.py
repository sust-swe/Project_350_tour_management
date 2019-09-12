from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django import views
from .models import Residence
from .models import Residence, Space
from .forms import ResidenceForm, SpaceForm
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
                ob.user_detail = UserDetail.objects.get(user=request.user)
                try:
                    ob.full_clean()
                    ob.save()
                    return redirect('/residence/my_residence/')
                except ValidationError as e:
                    nfe = e.message_dict[NON_FIELD_ERRORS]
                    return render(request, self.template_name, {'form': form, 'nfe': nfe})
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
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=id)
            if residence.user_detail.user == request.user:
                form = self.form_class(instance=residence)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            instance = Residence.objects.get(pk=id)
            if instance.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    ob = form.save(commit=False)
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
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class DeleteResidence(views.View):

    def get(self, request, id):
        if request.user.is_authenticated:
            instance = Residence.objects.get(pk=id)
            if instance.user_detail.user == request.user:
                instance.delete()
                return redirect('/residence/my_residence/')
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')


class ShowResidenceSpace(views.View):
    template_name = 'residence_space.html'

    def get(self, request, id):
        spaces = Space.objects.filter(residence_id=id)
        return render(request, self.template_name, {'spaces': spaces})


class AddSpace(views.View):
    template_name = 'add_space.html'
    form_class = SpaceForm

    def get(self, request, id):
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=id)
            if residence.user_detail.user == request.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=id)
            if residence.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    ob = form.save(commit=False)
                    ob.residence = residence
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/residence/{}/space/'.format(id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info('Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class SpaceDetail(views.View):
    template_name = 'space_detail.html'

    def get(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        return render(request, self.template_name, {'space': space})


class UpdateSpace(views.View):
    template_name = 'update_space.html'
    form_class = SpaceForm

    def get(self, request, space_id):
        if request.user.is_authenticated:
            space = Space.objects.get(pk=space_id)
            if space.residence.user_detail.user == request.user:
                form = self.form_class(instance=space)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

    def post(self, request, space_id):
        if request.user.is_authenticated:
            space = Space.objects.get(pk=space_id)
            if space.residence.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=space)
                if form.is_valid():
                    ob = form.save(commit=False)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/residence/space/{}/'.format(space.id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info(request, 'Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class DeleteSpace(views.View):
    def get(self, request, space_id):
        if request.user.is_authenticated:
            space = Space.objects.get(pk=space_id)
            if space.residence.user_detail.user == request.user:
                tmp = space.residence.id
                space.delete()
                return redirect('/residence/{}/space/'.format(tmp))
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')