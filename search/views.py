from homepage.base import *
from .forms import SearchRestaurantForm, SpaceSearchForm
from homepage.models import City
from restaurant.models import Restaurant
from residence.models import SpaceAvailable, SpaceType, Residence
from .first_view import load_city_choice, load_flw_from_day, load_flw_to_day, load_flw_from_month, load_flw_to_month, load_flw_to_year, load_date_from_DateForm

##########################################   non-class views        ##########################

#######################################        class based views          ################################################################


class SearchRestaurant(views.View):
    template_name = 'search_restaurant.html'
    form_class = SearchRestaurantForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            country_id = form.cleaned_data.get('country', None)
            city_id = form.cleaned_data.get('city', None)
            restaurant_name = form.cleaned_data.get('name', None)
            # print(country_id, city_id, restaurant_name, type(country_id))
            # print(Restaurant.objects.all())

            restaurants = Restaurant.objects.all()

            if country_id:
                restaurants = Restaurant.objects.filter(
                    country_id=country_id)
            # print(restaurants)
            if city_id:
                restaurants = restaurants.filter(city_id=int(city_id))
            # print(restaurants)
            if restaurant_name:
                restaurants = restaurants.filter(
                    name__contains=restaurant_name)
            # print(restaurants)

            return render(request, self.template_name, {'restaurants': restaurants, 'form': form})
        else:
            # print(form.as_table())
            return render(request, self.template_name, {'form': form})


class SearchSpace(views.View):
    template_name = "search_space.html"
    form_class = SpaceSearchForm

    def get(self, request):
        form = self.form_class()
        #print('space search view')
        # print(form.as_table())
        return render(request, self.template_name, {'form': form})

    # search by form's optional fields
    def search_by_optionals(self, form, qs):
        max_rent = min_rent = residence_id = None
        if form.cleaned_data.get('max_rent', None):
            max_rent = float(form.cleaned_data['max_rent'])
            qs = qs.filter(space__space_type__rent__lte=max_rent)
        if form.cleaned_data.get('min_rent', None):
            min_rent = float(form.cleaned_data['min_rent'])
            qs = qs.filter(space__space_type__rent__gte=min_rent)
        if form.cleaned_data.get('residence', None):
            residence_id = int(form.cleaned_data['residence'])
            qs = qs.filter(space__residence__id=residence_id)
        return qs

    # searches by form's mandatory fields
    def search_by_essentials(self, form, user):
        person_n = int(form.cleaned_data['person_n'])
        from_date, to_date = load_date_from_DateForm(form)
        city = int(form.cleaned_data['city'])
        qs = SpaceAvailable.objects.filter(space__residence__city__id=city, avail_from__lte=from_date,
                                           avail_to__gte=to_date, space__space_type__person=person_n).exclude(space__residence__user_detail__user=user)
        return qs

    def process_context(self, avail_space_qs, space_n):
        space_type_id_count = {}
        space_type_id = []
        for ob in avail_space_qs:
            if space_type_id_count.get(ob.space.space_type.id, None):
                space_type_id_count[ob.space.space_type.id] += 1
            else:
                space_type_id_count[ob.space.space_type.id] = 1

        for k in space_type_id_count:
            if space_type_id_count[k] >= space_n:
                space_type_id += [int(k)]

        space_type_qs = SpaceType.objects.filter(
            id__in=space_type_id).order_by('residence')
        residence_qs = Residence.objects.filter(
            spacetype__id__in=space_type_id)

        # stores SpaceType residence_id, pk, name, count accordingly
        space_types_ri_p_n_c_r = []
        for i in space_type_qs:
            space_types_ri_p_n_c_r += [(i.residence.id, i.id,
                                        i.name, space_type_id_count[i.id], i.rent)]
        # print(space_types_ri_p_n_c)
        context = {
            "space_types_ri_p_n_c_r": space_types_ri_p_n_c_r,
            'residence_qs': residence_qs,
        }
        return context

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            # print("search space valid")
            space_avail_qs = self.search_by_essentials(form, request.user)
            space_avail_qs = self.search_by_optionals(form, space_avail_qs)
            space_n = int(form.cleaned_data['space_n'])
            context = self.process_context(space_avail_qs, space_n)
            context['form'] = form
            return render(request, self.template_name, context)

        else:
            print(form.as_table())
            return render(request, self.template_name, {'form': form})
