
def extract_personal_details(form_data):
    patient_id = form_data.pop('patient_id')
    first_name = form_data.pop('first_name')
    last_name = form_data.pop('last_name')
    city = form_data.pop('address_id')
    street = form_data.pop('street')
    build_number = form_data.pop('number')
    date_of_birth = form_data.pop('date_of_birth')
    telephone = form_data.pop('telephone')
    mobile = form_data.pop('mobile')
    return patient_id, first_name, last_name, city, street, build_number, date_of_birth, telephone, mobile


def extract_vaccine_data(form_data):
    vaccine_data = [(form_data.pop(f"vaccine_date_{i}", None), form_data.pop(f"manufacturer_{i}", None))
                    for i in range(1, 5)]
    return vaccine_data


def extract_infection_data(form_data):
    positive_date = form_data.pop('positive_date', None)
    recovery_date = form_data.pop('recovery_date', None)
    return positive_date, recovery_date
