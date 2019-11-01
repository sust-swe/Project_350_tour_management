from homepage.base import *
from django.contrib.auth.models import User, auth
from django import views
from .models import Guide, GuideAvailable, GuideBooking
from .forms import CreateGuideForm, DateForm
from homepage.models import UserDetail
from .first_views import create_avail_guide, make_guide_unavailable_amap


def register(request):
    return render(request, 'register.html')


def load_date_from_DateForm(form):
    year = int(form.cleaned_data['from_year'])
    month = int(form.cleaned_data['from_month'])
    day = int(form.cleaned_data['from_day'])
    from_date = date(year, month, day)
    year = int(form.cleaned_data['to_year'])
    month = int(form.cleaned_data['to_month'])
    day = int(form.cleaned_data['to_day'])
    to_date = date(year, month, day)
    return from_date, to_date

# ***********************************************  Guide    ************************************************************


class MyGuide(views.View):
    template_name = 'my_guide.html'

    def get(self, request):
        if request.user.is_authenticated:
            qs = Guide.objects.filter(user_detail__user=request.user)
            return render(request, self.template_name, {'qs': qs})
        else:
            return redirect("/login_required/")


class AddGuide(views.View):
    template_name = 'add_guide.html'
    form_class = CreateGuideForm

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect("/login_required/")

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
                except ValidationError as ve:
                    for kk in ve.message_dict:
                        form.add_error(kk, ve.message_dict[kk])
                    return render(request, self.template_name, {'form': form})
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return redirect("/login_required/")


class GuideDetail(views.View):
    template_name = 'guide_detail.html'

    def get(self, request, id):
        guide = Guide.objects.get(pk=id)
        return render(request, self.template_name, {'guide': guide})


class UpdateGuide(views.View):
    template_name = 'update_guide.html'
    form_class = CreateGuideForm

    def get(self, request, id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=id)
            if guide.user_detail.user == request.user:
                form = self.form_class(instance=guide)
                return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")

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
                    except ValidationError as ve:
                        for kk in ve.message_dict:
                            form.add_error(kk, ve.message_dict[kk])
                        return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")


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


# *************************************   availability    **************************************************


class GuideAvailability(views.View):
    template_name = "guide_available.html"
    
    def get(self, request, guide_id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if guide.user_detail.user == request.user:
                avails = GuideAvailable.objects.filter(guide=guide)
                return render(request, self.template_name, {"avails": avails, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")
        
        
class CreateGuideAvailability(views.View):
    template_name = "create_guide_availability.html"
    form_class = DateForm

    def get(self, request, guide_id):

        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if guide.user_detail.user == request.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect('/login_required/')

    def post(self, request, guide_id):
        
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if guide.user_detail.user == request.user:
                form = self.form_class(request.POST or None)
                if form.is_valid():
                    from_date, to_date = load_date_from_DateForm(form)
                    create_avail_guide(GuideAvailable, GuideBooking, guide, from_date, to_date)
                    return redirect('/guide/{}/availability/'.format(guide.id))
                else:
                    return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect('/permission_denied/')
        else:
            return redirect("/login_required/")


class MakeGuideUnavailable(views.View):
    template_name = "make_guide_unavail.html"
    form_class = DateForm

    def get(self, request, guide_id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if request.user == guide.user_detail.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")

    def post(self, request, guide_id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if request.user == guide.user_detail.user:
                form = self.form_class(request.POST)
                if form.is_valid():
                    from_date, to_date = load_date_from_DateForm(form)
                    make_guide_unavailable_amap(GuideAvailable, guide, from_date, to_date)
                    return redirect("/guide/{}/availability/".format(guide_id))
                else:
                    return render(request, self.template_name, {'form': form, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")
        
        
class GuideBookings(views.View):
    template_name = 'guide_bookings.html'
    
    def get(self, request, guide_id):
        if request.user.is_authenticated:
            guide = Guide.objects.get(pk=guide_id)
            if guide.user_detail.user == request.user:
                bookings = GuideBooking.objects.filter(guide=guide)
                return render(request, self.template_name, {"bookings": bookings, "guide": guide})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")