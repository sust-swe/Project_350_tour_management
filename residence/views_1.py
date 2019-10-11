from homepage.base import *


#######################################          Complementary methods          ######################################

# returns true even a part is booked
def is_space_ordered(SpaceBooking, space, from_date, to_date):
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
