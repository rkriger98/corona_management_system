from flask import request, jsonify
import pyodbc

from HMO_server.extract_data import *
from HMO_server.input_handling.corona_details_propriety import *
from HMO_server.input_handling.personal_details_propriety import is_valid_personal_details

with pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-ROECGEC\MSSQLSERVER01;'
                      'Database=Patient_Records_HMO_DB;'
                      'Trusted_Connection=yes;') as conn:
    cursor = conn.cursor()


def get_patients():
    try:
        cursor.execute('SELECT * FROM Patient')
        patients = cursor.fetchall()
        return jsonify(patients)
    except pyodbc.Error as e:
        raise ValueError(str(e))


def add_patient():
    try:
        # Get the customer information from the request object
        form_data = request.form.to_dict()

        # Extract personal details, validate and insert
        patient_id, first_name, last_name, city, street, build_number, date_of_birth, telephone, mobile = \
            extract_personal_details(form_data)
        if is_valid_personal_details(patient_id, date_of_birth, telephone, mobile):
            address_id = insert_address(city, street, build_number)
            insert_patient(patient_id, first_name, last_name, date_of_birth, telephone, mobile, address_id)

            # Extract vaccine data, validate and insert
            vaccine_data = extract_vaccine_data(form_data)
            for vaccine_date, manufacturer in vaccine_data:
                if vaccine_date and manufacturer:
                    is_valid_vaccine_date(vaccine_date, manufacturer)
                    insert_vaccine(patient_id, vaccine_date, manufacturer)

            # Extract infection data, validate and insert
            positive_date, recovery_date = extract_infection_data(form_data)
            if positive_date and recovery_date:
                is_valid_infection_and_recovery_date(positive_date, recovery_date)
                insert_infection(patient_id, positive_date, recovery_date)

        return "Customer added successfully"
    except ValueError as e:
        raise ValueError(str(e))


def insert_address(city, street, build_number):
    try:
        # Check if the address already exists in the database
        select_query = "SELECT address_id FROM addresses WHERE city = ? AND street = ? AND number = ?"
        values = (city, street, build_number)
        cursor.execute(select_query, values)
        row = cursor.fetchone()
        if row:
            address_id = row[0]  # Address already exists, return the address_id
        else:
            # Address does not exist, create a new row and return the new address_id
            insert_query = "INSERT INTO Address (city, street, number) VALUES (?, ?, ?)"
            values = (city, street, build_number)
            cursor.execute(insert_query, values)
            conn.commit()
            # Get the newly created address_id
            select_query = "SELECT SCOPE_IDENTITY()"
            cursor.execute(select_query)
            row = cursor.fetchone()
            address_id = row[0]
        return address_id
    except ValueError as e:
        raise ValueError(str(e))


def insert_patient(patient_id, first_name, last_name, date_of_birth, telephone, mobile, address_id):
    try:
        insert_query = "INSERT INTO Patient (patient_id, first_name, last_name, date_of_birth, telephone, mobile," \
                       "address_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (patient_id, first_name, last_name, date_of_birth, telephone, mobile, address_id)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        conn.commit()
    except ValueError as e:
        raise ValueError(str(e))


def insert_vaccine(patient_id, vaccine_date, manufacturer):
    try:
        insert_query = "INSERT INTO Vaccine (patient_id, vaccine_date, manufacturer) VALUES (?, ?, ?)"
        values = (patient_id, vaccine_date, manufacturer)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        conn.commit()
    except ValueError as e:
        raise ValueError(str(e))


def insert_infection(patient_id, positive_date, recovery_date):
    try:
        insert_query = "INSERT INTO Infection (patient_id, positive_date, recovery_date) VALUES (?, ?, ?)"
        values = (patient_id, positive_date, recovery_date)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        conn.commit()
    except ValueError as e:
        raise ValueError(str(e))


def main():
    return


if __name__ == "__main__":
    main()
