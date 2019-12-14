from django import views
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse


class PermissionDenied(views.View):

    def get(self, request):
        return render(request, "index.html", {"error": "Permission DENIED !"})


class LoginRequired(views.View):

    def get(self, request):
        return render(request, "index.html", {"error": "Login REQUIRED !"})
