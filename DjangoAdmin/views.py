from django import views
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse


class PermissionDenied(views.View):

    def get(self, request):
        messages.info(request, 'Permission Denied')
        return redirect('/')


class LoginRequired(views.View):

    def get(self, request):
        messages.info(request, 'Login Required')
        return redirect('/')
