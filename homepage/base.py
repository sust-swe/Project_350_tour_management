from django import forms, views
from django.db import models
from django.urls import path, include
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User, auth
from datetime import *
from django.contrib import messages
from django.db.models import Q, F
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _
