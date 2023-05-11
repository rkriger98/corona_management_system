from HMO_server.POST.input_validation_checks.corona_validation import *
from HMO_server.POST.input_validation_checks.personal_details_validation import *


def is_valid_corona_details(vaccine_data, infection_date):
    try:
        for vaccine_date, manufacturer in vaccine_data:
            if vaccine_date and manufacturer:
                is_valid_vaccine_date(vaccine_date, manufacturer)
        (positive_date, recovery_date) = infection_date
        if not positive_date and not recovery_date:
            return True
        is_valid_infection_and_recovery_date(positive_date, recovery_date)
        return True
    except ValueError as e:
        raise ValueError(str(e))


def is_valid_personal_details(personal_details):
    pid, first, last, city, street, number, dob, tel, mob = personal_details
    validation_funcs = [
        lambda: is_validate_id_number(pid),
        lambda: is_only_letters([first, last, city, street]),
        lambda: str(number).isdigit(),
        lambda: is_valid_dob(dob),
        lambda: is_valid_landline_phone_number(tel),
        lambda: is_valid_mobile_phone_number(mob)
    ]
    try:
        return all(func() for func in validation_funcs)
    except ValueError as e:
        raise ValueError(str(e))
