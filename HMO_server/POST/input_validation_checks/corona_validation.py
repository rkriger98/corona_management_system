"""
An explanation of how I based the correctness of the inputs:
The first COVID-19 patient in Israel was identified on February 21, 2020.
israel began its COVID-19 vaccination campaign on December 20, 2020, with the Pfizer-BioNTech vaccine being the first
vaccine to be administered.
Since then, Israel has administered several other COVID-19 vaccines, including Moderna, Oxford, Sinovac, Bharat and
Sinopharm.
"""
import datetime

manufacturer_dates = {
        'sinovac': datetime.datetime(2020, 11, 1),
        'sinopharm': datetime.datetime(2020, 11, 1),
        'pfizer': datetime.datetime(2020, 12, 1),
        'moderna': datetime.datetime(2020, 12, 1),
        'oxford': datetime.datetime(2021, 1, 1),
        'bharat': datetime.datetime(2021, 1, 1),
    }


def parse_date(date):
    try:
        return datetime.datetime.strptime(str(date), "%Y-%m-%d")
    except ValueError:
        raise ValueError("The date must be in the format of 'yyyy-mm-dd'")


def is_valid_corona_date(corona_date):
    try:
        converted_corona_date = parse_date(corona_date)
    except ValueError:
        raise ValueError("The dates must be in the format of 'yyyy-mm-dd'")
    # The first COVID-19 patient in Israel was identified on February 21, 2020.
    corona_starting_date = datetime.datetime(2020, 2, 21)
    if corona_starting_date <= converted_corona_date <= datetime.datetime.now():
        return True
    else:
        raise ValueError("The date should be during the Corona period between February 21, 2020 and today.")


def is_valid_infection_and_recovery_date(infection_date, recovery_date):
    try:
        if infection_date and not recovery_date:
            if is_valid_corona_date(infection_date):
                return True
        if is_valid_corona_date(infection_date) and is_valid_corona_date(recovery_date):
            if infection_date <= recovery_date:
                return True
            else:
                raise ValueError("The infection date must be before the recovery date")
    except ValueError as e:
        raise ValueError(str(e))


def validate_manufacturer(manufacturer):
    if manufacturer.lower() not in manufacturer_dates.keys():
        raise ValueError(f"Unknown manufacturer {manufacturer}, choose only from: {', '.join(manufacturer_dates.keys())}")


def get_manufacturer_beginning_date(manufacturer):
    if manufacturer.lower() not in manufacturer_dates:
        raise ValueError("Incorrect vaccine date")
    return manufacturer_dates[manufacturer.lower()]


def is_valid_vaccine_date(vaccine_date_str, manufacturer):
    manufacturing_date = parse_date(vaccine_date_str)
    validate_manufacturer(manufacturer)
    beginning_manufacturing_date = get_manufacturer_beginning_date(manufacturer)
    current_date = datetime.datetime.now()
    if beginning_manufacturing_date <= manufacturing_date <= current_date:
        return True
    raise ValueError("Incorrect vaccine date")
