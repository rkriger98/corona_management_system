from flask import jsonify
from HMO_server.GET.patient_data_utils import parse_patient_data, fetch_patient_data
from HMO_server.POST.exstract_and_insert_to_database.extract_input import *
from HMO_server.POST.exstract_and_insert_to_database.insert_to_database import *
from HMO_server.POST.input_validation_checks.input_validation import *


def get_patients():
    try:
        rows = fetch_patient_data()
        patients = parse_patient_data(rows)
        return jsonify(patients)
    except pyodbc.Error as e:
        raise ValueError(str(e))


def add_patient(json_data):
    try:
        # Extract data
        personal_details = extract_personal_details(json_data)
        vaccine_data = extract_vaccine_data(json_data)
        infection_date = extract_positive_and_recovery_data(json_data)

        # validate and insert
        if is_valid_personal_details(personal_details) and is_valid_corona_details(vaccine_data, infection_date):
            address_id = insert_address(*personal_details[3:6])  # city, street, number
            # patient_id, first_name, last_name, date_of_birth, telephone, mobile, address_id
            insert_patient(*personal_details[:3], *personal_details[6:], address_id)

            for vaccine_date, manufacturer in vaccine_data:
                if vaccine_date and manufacturer:
                    insert_vaccine(personal_details[0], vaccine_date, manufacturer)

            positive_date, recovery_date = infection_date
            if positive_date and recovery_date:
                print(positive_date, recovery_date)
                insert_infection(personal_details[0], positive_date, recovery_date)

        return "Patient added successfully"
    except ValueError as e:
        raise ValueError(str(e))
