def extract_personal_details(json_data):
    personal_details = [
        json_data.get('patient_id'),
        json_data.get('first_name'),
        json_data.get('last_name'),
        json_data.get('city'),
        json_data.get('street'),
        json_data.get('number'),
        json_data.get('date_of_birth'),
        json_data.get('telephone'),
        json_data.get('mobile')]
    return personal_details


def extract_vaccine_data(json_data):
    vaccine_data = [(json_data.get(f"vaccine_date_{i}", None), json_data.get(f"manufacturer_{i}", None))
                    for i in range(1, 5)]
    return vaccine_data


def extract_infection_data(json_data):
    infection_data = [
        json_data.get('positive_date', None),
        json_data.get('recovery_date', None)]
    return infection_data
