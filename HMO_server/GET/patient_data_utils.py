import pyodbc
from HMO_server.connect_to_database import cursor


def fetch_patient_data():
    cursor.execute('SELECT p.patient_id, p.first_name, p.last_name, a.city, a.street, a.number, p.date_of_birth, '
                   'p.telephone, p.mobile, v1.vaccine_date, v1.manufacturer '
                   'FROM Patient p '
                   'JOIN Address a ON p.address_id = a.address_id '
                   'LEFT JOIN Vaccine v1 ON p.patient_id = v1.patient_id AND v1.vaccine_id = '
                   '    (SELECT MAX(v2.vaccine_id) FROM Vaccine v2 WHERE v2.patient_id = p.patient_id) '
                   'ORDER BY p.patient_id')
    rows = cursor.fetchall()
    return rows


def parse_patient_data(rows):
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
                "vaccine_dates": [],
                "manufacturers": [],
                "positive_date": None,
                "recovery_date": None
            }
            patients.append(current_patient)

        if vaccine_date is not None:
            current_patient["vaccine_dates"].append(str(vaccine_date))
            current_patient["manufacturers"].append(manufacturer)

    return patients
