
from homepage.base import *
from homepage.models import UserDetail
from .models import Space, SpaceAvailable, SpaceBooking, Residence, SpaceType
from .forms import SpaceForm, SpaceAvailabilityForm, ResidenceForm, CreateSpaceTypeForm, SpaceSearchForm, DateForm
from .views_1 import is_space_booked, create_avail_space, load_date_from_DateForm, make_space_unavailable


# Create your views here.

###################################        Complementary Methods         ################################

def register(request):
    return render(request, 'register.html')


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
        residence = Residence.objects.get(pk=id)
        # print(spaces)
        return render(request, self.template_name, {'spaces': spaces, 'residence': residence})


###############################################  Space Type  ###########################################


class ShowSpaceTypes(views.View):
    # displays the space types of a particular residence
    template_name = "show_space_type.html"

    def get(self, request, id):
        residence = Residence.objects.get(pk=id)
        qs = SpaceType.objects.filter(residence=residence)
        context = {
            'space_types': qs,
            'residence': residence
        }
        print(qs)
        print("ShowSpaceType")
        return render(request, self.template_name, context)


class CreateSpaceType(views.View):
    template_name = "create_update_space_type.html"
    form_class = CreateSpaceTypeForm

    def get(self, request, residence_id):
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=residence_id)
            if request.user == residence.user_detail.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")

    def post(self, request, residence_id):
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=residence_id)
            if residence.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    print("create space type")
                    new_space_type = form.save(commit=False)
                    new_space_type.residence = residence
                    try:
                        new_space_type.full_clean()
                        new_space_type.save()
                        return redirect("/residence/{}/space_type/".format(residence.id))
                    except ValidationError as ve:
                        for kk in ve.message_dict:
                            form.add_error(kk, ve.message_dict[kk])
                        return render(request, self.template_name, {'form': form})
                else:
                    print(form.as_table())
                    return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")


class ShowSpaceTypeDetail(views.View):
    template_name = "show_space_type_detail.html"

    def get(self, request, space_type_id):
        ob = SpaceType.objects.get(id=space_type_id)
        return render(request, self.template_name, {'space_type': ob})


class DeleteSpaceType(views.View):

    def get(self, request, space_type_id):
        if request.user.is_authenticated:
            space_type = SpaceType.objects.get(pk=space_type_id)
            if request.user == space_type.residence.user_detail.user:
                space_type.delete()
                return redirect("/residence/{}/space_type/".format(space_type.residence.id))
            else:
                return redirect('/permission_denied/')
        else:
            return redirect('/login_required/')


class UpdateSpaceType(views.View):
    template_name = "create_update_space_type.html"
    form_class = CreateSpaceTypeForm

    def get(self, request, space_type_id):
        if request.user.is_authenticated:
            space_type = SpaceType.objects.get(pk=space_type_id)
            if request.user == space_type.residence.user_detail.user:
                form = self.form_class(instance=space_type)
                return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied")
        else:
            return redirect("/login_required/")

    def post(self, request, space_type_id):
        if request.user.is_authenticated:
            space_type = SpaceType.objects.get(pk=space_type_id)
            if request.user == space_type.residence.user_detail.user:
                form = self.form_class(
                    request.POST, request.FILES, instance=space_type)
                if form.is_valid():
                    ob = form.save(commit=False)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect("/residence/{}/space_type/".format(space_type.residence.id))
                    except ValidationError as ve:
                        for kk in ve.message_dict:
                            form.add_error(kk, ve.message_dict[kk])
                        return render(request, self.template_name, {'form': form})
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")


##################################       Space        ##############################################################

class AddSpace(views.View):
    template_name = 'add_space.html'
    form_class = SpaceForm

    def get(self, request, id):
        if request.user.is_authenticated:
            residence = Residence.objects.get(pk=id)
            if residence.user_detail.user == request.user:

                form = self.form_class(initial={'residence': id})
                # print("AddSpace", id)
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
                form = self.form_class(
                    request.POST, request.FILES, initial={'residence': id})
                if form.is_valid():
                    ob = form.save(commit=False)
                    ob.residence = residence
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/residence/{}/space/'.format(id))
                    except ValidationError as ve:
                        for kk in ve.message_dict:
                            form.add_error(kk, ve.message_dict[kk])
                        return render(request, self.template_name, {'form': form})
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
    form_class = DateForm

    def get(self, request, space_id):
        # print("createspaceavailability get")
        space = Space.objects.get(pk=space_id)
        if request.user.is_authenticated and space.residence.user_detail.user == request.user:
            form = self.form_class()
            # print(form)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('/permission_denied/')

    def post(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        if request.user.is_authenticated and space.residence.user_detail.user == request.user:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                from_date, to_date = load_date_from_DateForm(form)
                # print("createspaceavailability", from_date, to_date)
                space_available = SpaceAvailable(
                    space=space, avail_from=from_date, avail_to=to_date)
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


class MakeSpaceUnavailable(views.View):
    template_name = "c_s_a.html"
    form_class = DateForm

    def get(self, request, space_id):
        if request.user.is_authenticated:
            space = Space.objects.get(pk=space_id)
            if request.user == space.residence.user_detail.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")

    def post(self, request, space_id):
        if request.user.is_authenticated:
            space = Space.objects.get(pk=space_id)
            if request.user == space.residence.user_detail.user:
                form = self.form_class(request.POST)
                if form.is_valid():
                    from_date, to_date = load_date_from_DateForm(form)
                    unavails = make_space_unavailable(
                        SpaceAvailable, space, from_date, to_date)
                    return redirect("/residence/space/{}/".format(space_id))
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")


######################################   SpaceBookings    ####################################


class BookSpace(views.View):
    pass


'''
        if request.user.is_authenticated:
            if request.user == :
            
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")
'''
