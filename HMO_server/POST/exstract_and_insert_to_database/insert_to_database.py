import pyodbc

from HMO_server.connect_to_database import cursor, conn


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
            # conn.commit()
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
        # conn.commit()
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
        # conn.commit()
    except ValueError as e:
        raise ValueError(str(e))


def insert_infection(patient_id, positive_date, recovery_date):
    try:
        insert_query = "INSERT INTO Infection (patient_id, positive_date, recovery_date) VALUES (?, ?, ?)"
        values = (int(patient_id), positive_date, recovery_date)
        # Execute the INSERT query
        cursor.execute(insert_query, values)
        # Commit the changes to the database
        # conn.commit()
    except ValueError as e:
        raise ValueError(str(e))
