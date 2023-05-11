def extract_personal_details(json_data):
    required_fields = ['patient_id', 'first_name', 'last_name', 'city', 'street', 'number', 'date_of_birth',
                       'telephone', 'mobile']
    for field in required_fields:
        if field not in json_data:
            raise ValueError(f"Missing required field: {field}")
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
    vaccine_data = []
    for i in range(1, 5):
        vaccine_date = json_data.get(f"vaccine_date_{i}", None)
        manufacturer = json_data.get(f"manufacturer_{i}", None)
        if vaccine_date is not None and manufacturer is None:
            raise ValueError(f"Missing manufacturer for vaccine dose {i}")
        if vaccine_date is None and manufacturer is not None:
            raise ValueError(f"Missing date for vaccine dose {i}")
        vaccine_data.append((vaccine_date, manufacturer))
    return vaccine_data


def extract_positive_and_recovery_data(json_data):
    positive_date = json_data.get('positive_date', None)
    recovery_data = json_data.get('recovery_date', None)
    if (recovery_data is not None and positive_date is None) or (recovery_data is None and positive_date is not None):
        raise ValueError("Enter positive date and recovery data")
    return positive_date, recovery_data
