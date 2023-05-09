"""
An explanation of how I based the correctness of the inputs:
The first COVID-19 patient in Israel was identified on February 21, 2020.
israel began its COVID-19 vaccination campaign on December 20, 2020, with the Pfizer-BioNTech vaccine being the first
vaccine to be administered.
Since then, Israel has administered several other COVID-19 vaccines, including Moderna, Oxford, Sinovac, Bharat and
Sinopharm.
"""
import datetime


def is_valid_corona_date(corona_date_str):
    """
    The function checks if the date of as to do with with corona is valid
    :param corona_date_str: Corona date like infection or recovery
    :return:True if the date is greater than the start date of the corona epidemic and less than today,
    or raises a ValueError with an appropriate error message otherwise
    """
    try:
        corona_date = datetime.datetime.strptime(corona_date_str, "%d/%m/%Y")
        # The first COVID-19 patient in Israel was identified on February 21, 2020.
        corona_starting_date = datetime.datetime(2020, 2, 21)
        if corona_starting_date <= corona_date <= datetime.datetime.now():
            return True
        else:
            raise ValueError("The date should be during the Corona period between February 21, 2020 and today.")
    except ValueError:
        raise ValueError("Invalid date format. Please use the format dd/mm/yyyy.")


def is_valid_infection_and_recovery_date(infection_date, recovery_date):
    """
    The function checks if the date of infection and recovery match the Corona period and if the date of infection is
    before the date of recovery
    :param infection_date: Date of receiving a positive answer
    :param recovery_date: Date of recovery from corona
    :return: True if the dates are valid for the Corona period and if the infection date is before the recovery
    date, or raises a ValueError with an appropriate error message otherwise
    """
    try:
        if is_valid_corona_date(infection_date) <= is_valid_corona_date(recovery_date):
            return True
        else:
            raise ValueError("The infection date must be before the recovery date")
    except ValueError as e:
        raise ValueError(str(e))


def is_valid_vaccine_date(vaccine_date, manufacturer):
    """
    The function checks if the date of receipt of the vaccine is correct. the function checks if the date of receiving
    the vaccine is after the manufacturer started producing the vaccines.
    :param vaccine_date: The vaccination date
    :param manufacturer: The company that manufactured the vaccine
    :return: True if the vaccination date is greater than the manufacturer production date and less than today,
     or raises a ValueError with an appropriate error message otherwise.
    """
    try:
        manufacturing_date = datetime.datetime.strptime(vaccine_date, "%d/%m/%Y")
    except ValueError:
        raise ValueError("The vaccination date must be in the format of 'dd/mm/yyyy'")
    if manufacturer.lower() not in ['sinovac', 'sinopharm', 'pfizer', 'moderna', 'oxford', 'bharat']:
        raise ValueError(f"Unknown manufacturer {manufacturer}")
    if manufacturer.lower() in ['sinovac', 'sinopharm']:
        beginning_manufacturing_date = datetime.datetime(2020, 11, 1)
    elif manufacturer.lower() in ['pfizer', 'moderna']:
        beginning_manufacturing_date = datetime.datetime(2020, 12, 1)
    elif manufacturer.lower() in ['oxford', 'bharat']:
        beginning_manufacturing_date = datetime.datetime(2021, 1, 1)
    else:
        raise ValueError("Incorrect manufacturing date")
    if beginning_manufacturing_date <= manufacturing_date <= datetime.datetime.now():
        return True
    raise ValueError("Incorrect manufacturing date")
