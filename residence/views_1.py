from homepage.base import *


#######################################          Complementary methods          ######################################
month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']

# returns true even a part is booked


def is_space_booked(SpaceBooking, space, from_date, to_date):
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


def get_aggregated_avail_space(space, from_date, to_date):

    # proposed time span entirely included in old time span
    if SpaceAvailable.objects.filter(space=space, avail_from__lte=from_date, avail_to__gte=to_date).exists():
        return (None, None, None)
    flag = False

    # old time spans entirely included in proposed time span
    qs1 = SpaceAvailable.objects.filter(
        space=space, avail_from__gte=from_date, avail_to__lte=to_date)
    if qs1.exists():
        for ob in qs1:
            ob.delete()

    # proposed time span starts within a old time span
    qs2 = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=from_date, avail_to__gte=from_date)
    if qs2.exists():
        ob1 = qs2[0]
        from_date = ob1.avail_from
        ob1.delete()
        flag = True

    # proposed time span ends within a old time span
    qs3 = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=to_date, avail_to__gte=to_date)
    if qs3.exists():
        ob2 = qs3[0]
        to_date = ob2.avail_to
        ob2.delete()
        flag = True

    if flag:
        return (from_date, to_date, "Availability been merged with old ones")
    else:
        return (from_date, to_date, None)


def is_space_available(SpaceAvailable, space, from_date, to_date):

    dec1 = SpaceAvailable.objects.filter(
        space=space, avail_from__lte=from_date, avail_to__gte=to_date).exists()

    if dec1:
        return True
    return False

######################################       Load dependent date     ###################################


def load_flw_from_month(year):
    month = []
    today_ = datetime.today()
    this_month = today_.month
    this_year = today_.year
    if year == this_year:
        month = [(i, month_array[i]) for i in range(this_month, 13)]
    else:
        month = [(i, month_array[i]) for i in range(1, 13)]
    return month


def load_flw_from_day(year, month):
    day_arr = []
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
    day_arr = [(i, str(i)) for i in range(lb, ub+1)]
    return day_arr


def load_flw_to_year(from_year):
    year_choice = []
    for i in range(from_year, from_year+5):
        year_choice += [(i, str(i))]
    return year_choice


def load_flw_to_month(from_year, to_year, from_month):
    month_choice = []
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
    days = []
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
