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
        cursor.execute('SELECT p.patient_id, p.first_name, p.last_name, a.city, a.street, a.number, p.date_of_birth, '
                       'p.telephone, p.mobile, v1.vaccine_date, v1.manufacturer '
                       'FROM Patient p '
                       'JOIN Address a ON p.address_id = a.address_id '
                       'LEFT JOIN Vaccine v1 ON p.patient_id = v1.patient_id AND v1.vaccine_id = '
                       '    (SELECT MAX(v2.vaccine_id) FROM Vaccine v2 WHERE v2.patient_id = p.patient_id) '
                       'ORDER BY p.patient_id')
        rows = cursor.fetchall()

        patients = []
        current_patient_id = None
        current_patient = None

        for row in rows:
            patient_id, first_name, last_name, city, street, number, date_of_birth, telephone, mobile, vaccine_date, manufacturer = row

            if patient_id != current_patient_id:
                current_patient_id = patient_id
                current_patient = {
                    "patient_id": str(patient_id),
                    "first_name": first_name,
                    "last_name": last_name,
                    "city": city,
                    "street": street,
                    "number": number,
                    "date_of_birth": str(date_of_birth),
                    "telephone": telephone,
                    "mobile": mobile,
                    "vaccine_date_1": None,
                    "manufacturer_1": None,
                    "positive_date": None,
                    "recovery_date": None
                }
                patients.append(current_patient)

            if vaccine_date is not None:
                current_patient["vaccine_date_1"] = str(vaccine_date)
                current_patient["manufacturer_1"] = manufacturer

        return jsonify(patients)
    except pyodbc.Error as e:
        raise ValueError(str(e))


def add_patient(json_data):
    try:
        # Extract data
        personal_details = extract_personal_details(json_data)
        vaccine_data = extract_vaccine_data(json_data)
        infection_date = extract_infection_data(json_data)

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
                insert_infection(personal_details[0], positive_date, recovery_date)

        return "Customer added successfully"
    except ValueError as e:
        raise ValueError(str(e))


def insert_address(city, street, build_number):
    try:
        # Check if the address already exists in the database
        select_query = "SELECT address_id FROM Address WHERE city = ? AND street = ? AND number = ?"
        values = (city, street, build_number)
        cursor.execute(select_query, values)
        row = cursor.fetchone()
        if row:
            address_id = int(row[0])  # Address already exists, return the address_id
        else:
            # Address does not exist, create a new row and return the new address_id
            insert_query = "INSERT INTO Address (city, street, number) VALUES (?, ?, ?)"

            values = (city, street, build_number)
            cursor.execute(insert_query, values)
            conn.commit()
            # Get the newly created address_id
            cursor.execute(select_query, values)
            row = cursor.fetchone()
            address_id = int(row[0])
        return address_id
    except ValueError as e:
        raise ValueError(str(e))


def insert_patient(patient_id, first_name, last_name, date_of_birth, telephone, mobile, address_id):
    try:
        # Set IDENTITY_INSERT ON for Patient table
        cursor.execute("SET IDENTITY_INSERT Patient ON")
        insert_query = "INSERT INTO Patient (patient_id, first_name, last_name, date_of_birth, telephone, mobile," \
                       "address_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (int(patient_id), first_name, last_name, date_of_birth, telephone, mobile, address_id)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        conn.commit()
    except pyodbc.IntegrityError as e:
        if 'duplicate key' in str(e):
            raise ValueError("Patient with ID {} already exists in the system".format(patient_id))
        else:
            raise e
    except ValueError as e:
        raise ValueError(str(e))


def insert_vaccine(patient_id, vaccine_date, manufacturer):
    try:
        insert_query = "INSERT INTO Vaccine (patient_id, vaccine_date, manufacturer) VALUES (?, ?, ?)"
        values = (int(patient_id), vaccine_date, manufacturer)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        conn.commit()
    except ValueError as e:
        raise ValueError(str(e))


def insert_infection(patient_id, positive_date, recovery_date):
    try:
        insert_query = "INSERT INTO Infection (patient_id, positive_date, recovery_date) VALUES (?, ?, ?)"
        values = (int(patient_id), positive_date, recovery_date)
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
