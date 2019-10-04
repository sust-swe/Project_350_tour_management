from django import forms, views
from django.db import models
from django.urls import path, include
from django.shortcuts import redirect, render, HttpResponse
from datetime import datetime
from .models import *
from restaurant.models import *
from residence.models import *
from guide.models import *
from search.models import *
from blog.models import *
