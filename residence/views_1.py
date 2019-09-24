from django import views
from .forms import SpaceAvailabilityForm
from django.shortcuts import render, redirect
from .models import Space, SpaceAvailable
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib import messages
from django.db.models import Q


class CreateSpaceAvailability(views.View):
    template_name = 'c_s_a.html'
    form_class = SpaceAvailabilityForm

    def get(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        if request.user.is_authenticated and space.residence.user_detail.user == request.user:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('/permission_denied/')

    def post(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        if request.user.is_authenticated and space.residence.user_detail.user == request.user:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                space_available = form.save(commit=False)
                space_available.space = space
                try:
                    space_available.full_clean()
                    if SpaceAvailable.objects.filter(

                    ):
                        pass
                    space_available.save()
                    return redirect('/residence/space/{}/'.format(space.id))
                except ValidationError as e:
                    nfe = e.message_dict[NON_FIELD_ERRORS]
                    messages.info(request, nfe)
                    return render(request, self.template_name, {'form': form})
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return redirect('/permission_denied/')


def is_space_ordered(space, from_date, to_date):
    pass
