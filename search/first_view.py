from homepage.base import *


#######################################          Complementary methods          ######################################


month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']


# makes space unavailable through the entire proposed time span
def make_space_unavailable(SpaceAvailable, space, from_date, to_date):

    # proposed time span entirely included into available time span
    qs = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=from_date, avail_to__gte=to_date)

    if qs.exists():
        ob = qs[0]
        pre_date = from_date - timedelta(1)
        post_date = to_date + timedelta(1)
        ob1 = None
        ob2 = None
        if ob.avail_from < from_date:
            ob1 = SpaceAvailable(
                space=space, avail_from=ob.avail_from, avail_to=pre_date)
        if ob.avail_to > to_date:
            ob2 = SpaceAvailable(
                space=space, avail_from=post_date, avail_to=ob.avail_to)
        ob.delete()
        if ob1:
            ob1.save()
        if ob2:
            ob2.save()
        return

    # available time spans entirely included in the proposed time span
    SpaceAvailable.objects.filter(
        space=space, avail_from__gte=from_date, avail_to__lte=to_date).delete()

    # proposed time span starts in between available time span
    qs = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=from_date, avail_to__gte=from_date)
    if qs.exists():
        ob = qs[0]
        pre_date = from_date - timedelta(1)
        ob_1 = SpaceAvailable(
            space=space, avail_from=ob.avail_from, avail_to=pre_date)
        ob.delete()
        ob_1.save()

    # proposed time span ends in between avaiable time span
    qs = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=to_date, avail_to__gte=to_date)
    if qs.exists():
        ob = qs[0]
        post_date = to_date+timedelta(1)
        ob_1 = SpaceAvailable(space=space, avail_from=post_date,
                              avail_to=ob.avail_to)
        ob.delete()
        ob_1.save()


# returns TRUE even a part of the proposed time span is booked,otherwise returns FALSE
def is_space_booked(SpaceBooking, space, from_date, to_date):
    if from_date > to_date:
        return True
    # proposed time span atarts within booked time span
    dec1 = SpaceBooking.objects.filter(
        space=space, book_from__lte=from_date, book_to__gte=from_date).exists()
    # proposed time span ends within booked time span
    dec2 = SpaceBooking.objects.filter(
        space=space, book_from__lte=to_date, book_to__gte=to_date).exists()
    # proposed time span includes booked time span
    dec3 = SpaceBooking.objects.filter(
        space=space, book_from__gte=from_date, book_to__lte=to_date).exists()
    if dec1 or dec2 or dec3:
        return True
    else:
        return False


# make a space available which is not booked at all within proposed time span
def make_space_available_not_booked(SpaceAvailable, space, from_date, to_date):
    if from_date > to_date:
        return
    # proposed time span entirely included in old time span
    if SpaceAvailable.objects.filter(space=space, avail_from__lte=from_date, avail_to__gte=to_date).exists():
        return
    flag = False

    # old time spans entirely included in proposed time span
    SpaceAvailable.objects.filter(
        space=space, avail_from__gte=from_date, avail_to__lte=to_date).delete()

    # proposed time span starts within an available time span
    qs2 = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=from_date, avail_to__gte=from_date)
    if qs2.exists():
        ob1 = qs2[0]
        from_date = ob1.avail_from
        ob1.delete()

    # proposed time span ends within an available time span
    qs3 = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=to_date, avail_to__gte=to_date)
    if qs3.exists():
        ob2 = qs3[0]
        to_date = ob2.avail_to
        ob2.delete()

    pre_date = ob.from_date - timedelta(1)
    post_date = ob.to_date + timedelta(1)

    # adjacent time span preceeding proposed time span be unified
    qs4 = SpaceAvailable.objects.filter(space, avail_to=pre_date)
    if qs4.exists():
        from_date = qs4[0].avail_from
        qs4[0].delete()

    # adjacent time span following proposed time span be unified
    qs5 = SpaceAvailable(space=space, avail_from=post_date)
    if qs5.exists():
        to_date = qs5[0].avail_to
        qs5[0].delete()

    ob = SpaceAvailable(space=space, avail_from=from_date, avail_to=to_date)
    ob.save()


# make space available as much as possible(as much is not booked)
def create_avail_space(SpaceAvailable, SpaceBooking, space, from_date, to_date):

    # entire proposed time span benn booked
    if SpaceBooking.objects.filter(space=space, book_from__lte=from_date, book_to__gte=to_date).exists() or from_date > to_date:
        return

    # skip the time booked span preceeding the proposed time span
    qs = SpaceBooking.objects.filter(
        space=space, book_from__lte=from_date, book_to__gte=from_date)
    if qs.exists():
        ob = qs[0]
        from_date = ob.book_to+timedelta(1)

    # skip the booked time span following the proposed time span
    qs = SpaceBooking.objects.filter(
        space=space, book_from__lte=to_date, book_to__gte=to_date)
    if qs.exists():
        ob = qs[0]
        to_date = ob.book_from-timedelta(1)

    if from_date > to_date:
        return
    # skip the booked time span entirely included in proposed time span
    qs = SpaceBooking.objects.filter(
        space=space, book_from__gte=from_date, book_to__lte=to_date)
    if qs.exists():
        make_space_available_not_booked(
            SpaceAvailable, space, from_date, qs[0].book_from - timedelta(1))
        i = 0
        for ob in qs:
            if i == 0:
                continue
            else:
                make_space_available_not_booked(
                    SpaceAvailable, space, qs[i-1].book_to+timedelta(1), qs[i].book_from-timedelta(1))
            i = i+1
        make_space_available_not_booked(
            SpaceAvailable, space, qs[i-1].book_to+timedelta(1), to_date)


# returns true if the space is available through the entire propsed time span
def is_space_available(SpaceAvailable, space, from_date, to_date):
    if SpaceAvailable.objects.filter(space=space, avail_from__lte=from_date, avail_to__gte=to_date).exists():
        return True
    return False

###########################################       Load dependent date     ###################################################


def load_flw_from_month(year):
    month = [("", "------------")]
    today_ = datetime.today()
    this_month = today_.month
    this_year = today_.year
    if year == this_year:
        for i in range(today_.month, 13):
            month += [(i, month_array[i])]
    else:
        for i in range(1, 13):
            month += [(i, month_array[i])]

    return month


def load_flw_from_day(year, month):
    day_arr = [("", "------------")]
    lb = 0
    ub = 0
    td = datetime.today()
    if month in [1, 3, 5, 7, 8, 10, 12]:
        ub = 31
    elif month in [4, 6, 9, 11]:
        ub = 30
    else:
        if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
            ub = 29
        else:
            ub = 28
    if year == td.year and month == td.month:
        lb = td.day
    else:
        lb = 1
    for i in range(lb, ub+1):
        day_arr += [(i, str(i))]
    return day_arr


def load_flw_to_year(from_year):
    year_choice = [("", "------------")]
    for i in range(from_year, from_year+5):
        year_choice += [(i, str(i))]
    return year_choice


def load_flw_to_month(from_year, to_year, from_month):
    month_choice = [("", "------------")]
    lb = 0
    ub = -1
    if from_year == to_year:
        lb = from_month
    else:
        lb = 1
    ub = 12
    for i in range(lb, ub+1):
        month_choice += [(i, month_array[i])]
    return month_choice


def load_flw_to_day(from_year, to_year, from_month, to_month, from_day):
    days = [("", "------------")]
    lb = 0
    ub = -1
    if from_year == to_year and from_month == to_month:
        lb = from_day
    else:
        lb = 1
    if to_month in [1, 3, 5, 7, 8, 10, 12]:
        ub = 31
    elif to_month in [4, 6, 9, 11]:
        ub = 30
    else:
        if to_year % 400 == 0 or (to_year % 100 != 0 and to_year % 4 == 0):
            ub = 29
        else:
            ub = 28
    for i in range(lb, ub+1):
        days += [(i, str(i))]
    return days


def load_city_choice(City, country_id):
    city_choice = [("", "------------")]

    for ob in City.objects.filter(country_id=country_id):
        city_choice += [(ob.id, str(ob.city))]

    return city_choice
