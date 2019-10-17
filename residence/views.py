from .forms import SpaceSearchForm
from homepage.base import *
from homepage.models import UserDetail
from .models import Space, SpaceAvailable, SpaceBooking, Residence
from .forms import SpaceForm, SpaceAvailabilityForm, ResidenceForm
from .views_1 import is_space_booked, create_avail_space


# Create your views here.


def register(request):
    return render(request, 'register.html')

# searches spaces available using the parameters


def search_space(from_date, to_date, country, city, person_n, space_n, **kwargs):
    if from_date > to_date:
        return []

    qs = SpaceAvailable.objects.filter(space__residence__city__id=city, avail_from__lte=from_date,
                                       avail_to__gte=to_date, space__space_type__person=person_n)

    res_count = {}

    for ob in qs:
        if res_count.get(ob.space.residence_id, None):
            res_count[ob.space.residence_id] += 1
        else:
            res_count[ob.space.residence_id] = 1

    res_id_list = []

    for kk in res_count:
        if res_count.get(kk) >= space_n:
            res_id_list += [kk]

    residence_qs = 0

##########################################      Residence      #####################################################


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
                messages.info(request, 'Invalid Credentials')
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class ResidenceDetail(views.View):
    template_name = 'residence_detail.html'

    def get(self, request, id):
        # print('hi')
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
                form = self.form_class(
                    request.POST, request.FILES, instance=instance)
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


##################################       Space        ##############################################################

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
        avail = SpaceAvailable.objects.filter(
            space_id=space_id).order_by('avail_from')
        return render(request, self.template_name, {'space': space, 'avails': avail})


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
                form = self.form_class(
                    request.POST, request.FILES, instance=space)
                if form.is_valid():
                    ob = form.save(commit=False)
                    # print('Update space post')
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

############################################    Availability        ################################################


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
                    space_available.save()
                    return redirect('/residence/space/{}/'.format(space.id))
                except ValidationError as ve:
                    # print(ve.message_dict)
                    for k in ve.message_dict:
                        # form error filled by ve
                        form.add_error(k, ve.message_dict.get(k, None))
                    # print(form.as_table())
                    return render(request, self.template_name, {'form': form})
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return redirect('/permission_denied/')


class BookSpace(views.View):
    template_name = "book_space.html"
    form_class = SpaceAvailabilityForm

    def get(self, request, space_id):
        date_form = SpaceBookForm()
        return render(request, self.template_name, {'form': date_form})

    def post(self, request, space_id):
        form = SpaceBookForm(request.POST or None)
        print(form.as_table())
        if form.is_valid():
            year = int(form.cleaned_data['from_year'])
            month = int(form.cleaned_data['from_month'])
            day = int(form.cleaned_data['from_day'])
            from_date = date(year, month, day)
            year = int(form.cleaned_data['to_year'])
            month = int(form.cleaned_data['to_month'])
            day = int(form.cleaned_data['to_day'])
            to_date = date(year, month, day)

            space = Space.objects.get(pk=space_id)
            new_booking = SpaceBooking()
            new_booking.space = space
            new_booking.guest = UserDetail.objects.get(user=request.user)
            new_booking.booking_time = datetime.now()
            new_booking.total_rent = space.rent
            new_booking.book_from = from_date
            new_booking.book_to = to_date

            try:
                new_booking.full_clean()
                new_booking.save()
                return redirect("/residence/{}/".format(space_id))
            except ValidationError as ve:
                # adding form error after being valid
                for kk in ve.message_dict:
                    print(kk, ve.message_dict[kk])
                    form.add_error(kk, ve.message_dict.get(kk))
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class SearchSpace(views.View):
    template_name = "search_space.html"
    form_class = SpaceSearchForm

    def get(self, request):
        form = self.form_class()
        print('space search view')
        # print(form.as_table())
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            space_n = int(form.cleaned_data['space_n'])
            person_n = int(form.cleaned_data['person_n'])
            year = int(form.cleaned_data['from_year'])
            month = int(form.cleaned_data['from_month'])
            day = int(form.cleaned_data['from_day'])
            from_date = date(year, month, day)
            year = int(form.cleaned_data['to_year'])
            month = form.cleaned_data['to_month']
            day = form.cleaned_data['to_day']
            to_date = date(year, month, day)
