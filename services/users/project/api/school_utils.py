from datetime import datetime, timedelta
from project.api.constants import DATE_FORMAT, START, END


def check_in_term(date, term_dates):
    try:
        date = try_convert_to_datetime(date)
    except ValueError as e:
        raise ValueError(e)

    for i, half_term in enumerate(term_dates):
        if (half_term[START] <= date) and (half_term[END] >= date):
            return (True, i)

    return False, -1


def convert_dates_strings_to_datetime(term_dates):

    term_dates_datetime = []

    for half_term in term_dates:
        try:
            h1 = datetime.strptime(half_term[0], DATE_FORMAT)
            h2 = datetime.strptime(half_term[1], DATE_FORMAT)
        except ValueError as e:
            raise ValueError(e)
        term_dates_datetime.append([h1, h2])

    return term_dates_datetime


def check_term_dates_sequential(term_dates):

    if not isinstance(term_dates[0][0], datetime):
        raise ValueError('You must pass preferences with datetime objects')

    for half_term in term_dates:
        if half_term[END] < half_term[START]:
            return False

    for i in range(1, 6):
        if term_dates[i][START] < term_dates[i-1][END]:
            return False

    return True


def ensure_term_dates_are_weekdays(term_dates):

    if not isinstance(term_dates[0][0], datetime):
        term_dates = convert_dates_strings_to_datetime(term_dates)

    for half_term in term_dates:

        iso_start_day = half_term[START].isoweekday()
        iso_end_day = half_term[END].isoweekday()

        if iso_start_day in [6, 7]:
            # if start of term is set on a weekend, set it to the Monday
            half_term[START] += timedelta(days=(8-iso_start_day))
        if iso_end_day in [6, 7]:
            half_term[END] -= timedelta(days=(iso_end_day-5))


def try_convert_to_datetime(date):
    if not isinstance(date, datetime):
        try:
            date = datetime.strptime(date, DATE_FORMAT)
        except ValueError as e:
            raise ValueError(e)
    return date


def get_week_number(date, preferences):

    if not isinstance(date, datetime):
        date = try_convert_to_datetime(date)

    if date.isoweekday() in [6, 7]:
        raise ValueError('Date was weekend. Only submit weekday values')

    if preferences['weeks_timetable'] is 1:
        return 1

    if not preferences['dates_processed']:
        try:
            process_preferences(preferences)
        except ValueError as e:
            raise ValueError(e)

    try:
        term_dates = convert_dates_strings_to_datetime(
            preferences['term_dates'])
    except ValueError as e:
        raise ValueError(e)

    in_term, term_index = check_in_term(date, term_dates)

    if not in_term:
        return False, "Date outside term-time."

    ''' find number of "whole" weeks elapsed between current week and
    week at the start of term. If this number is even, then the current
    week is the same week number as that of the start of term. Otherwise,
    the week will be different. Toggle x between 1 and 2 by calculating 3 - x.
    '''

    monday_of_week = get_week_beginning_date(date)
    start_of_term = term_dates[term_index][START]

    monday_of_start_of_term = get_week_beginning_date(start_of_term)

    print('Monday of test: {}, Monday of term start: {}'.format(
        monday_of_week, monday_of_start_of_term))

    if ((monday_of_week - monday_of_start_of_term).days // 7) % 2 == 0:
        return int(preferences['week_number_start'][term_index])
    else:
        return int(3 - preferences['week_number_start'][term_index])


def process_preferences(preferences):

    """ if date is weekday and school has 2-week timetable,
    return the week number. If weekend, return week number of following week.
    If weeks_timetable is 1, return 1 """

    ''' find date of the Monday of the week that term starts. Then find date
    of the Monday of the last week of term. If number of weeks between the two
    dates is even, then the last week number is the same as the first week
    number, otherwise it is different.

    Assume that week number always changes on return from a holiday or half-
    term break. Give user option to switch starting week number from the
    client.

    Store beginning weeks in array in preferences, automatically populated
    when user enters term dates and weeks_timetable flag. If needed, array
    can be updated by user as needed. '''

    ''' CHECKS TO IMPLEMENT:
        * ensure that no term dates are in weekends
        * ensure no term dates are before earlier'''

    # convert all date strings to date objects for ease of manipulating
    try:
        term_dates = convert_dates_strings_to_datetime(
            preferences['term_dates'])
    except ValueError:
        raise ValueError("Could not convert dates string to datetime.")

    week_number_start = []

    # assume first week of autumn term is week 1
    week_number_start.append(1)

    """ loop through the terms. Find date of Monday of starting week, e.g.
    if term starts on Wednesday 5/9/18, will find Monday 3/9/18.

    Do the same for final week of term, returning Monday of ending week.

    Find out if number of weeks between the two Mondays is even - if so, the
    *following* term will switch timetable week numbers (as last and first
    week numbers must be the same). Otherwise, following term will begin
    on a *different* week than current term."""

    for i in range(5):
        monday_start = get_week_beginning_date(term_dates[i][START])
        monday_end = get_week_beginning_date(term_dates[i][END])

        if ((monday_end - monday_start).days // 7) % 2 == 0:
            """ 3-(old week number) will toggle week number between 1 and 2 """
            week_number_start.append(3 - week_number_start[i])

        else:
            week_number_start.append(week_number_start[i])

    preferences['week_number_start'] = week_number_start
    preferences['dates_processed'] = True

    return {
        'status': 'success',
        'message': 'Term dates successfully processed.'
        }


def get_week_beginning_date(date):

    if not isinstance(date, datetime):
        try:
            date = datetime.strptime(date, DATE_FORMAT)
        except ValueError as e:
            raise ValueError(e)

    return date - timedelta(days=(-1 + date.isoweekday()))
