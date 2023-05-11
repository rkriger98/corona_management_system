# corona_management_system

The system to handle a Corona database for a significant health fund contains server-side and database components.
The project includes an API that makes the server-side accessible to the client-side.
Patients can be entered into the HMO database, and all patients that are present in the HMO can be seen.
The accuracy of user input is highly valued in this project.

## Installation
To run this program, you will need to have the following programs installed on your machine:

- Python 3.8
- SQL Server with SQL Server Management Studio (SMSS)
- Postman

Additionally, you will need to install the required libraries for the program. You can find the list of required libraries in the requirements.txt file. To install the required libraries, run the following command in your terminal:


'pip install -r requirements.txt'


Next, you will need to set up the database. The database is included in the patients_database.bak file. You can restore the database using SMSS by following these steps:

1. Open SMSS and connect to your SQL Server instance.
2. Right-click on the "Databases" folder and select "Restore Database".
3. In the "General" tab, select "Device" and click on the "..." button.
4. In the "Select backup devices" dialog box, click on "Add" and select the patients_database.bak file.
5. Click "OK" to close the "Select backup devices" dialog box.
6. In the "General" tab, select "PatientsDatabase" as the destination database.
7. Click "OK" to restore the database.


Finally, you can use Postman to interact with the program as a client.

## How to Use
To use this program, follow the steps below:
1. Open your terminal and run the following command to start the server:

'flask run'


2. Connect to the server from Postman using the following commands:
**To see the patients in the database:**
- Choose the GET option with the following URL: http://127.0.0.1:5000
- Choose the JSON format
- Click on SEND
- Click on body
![image](https://github.com/rkriger98/corona_management_system/assets/73111633/73ac7e95-05e9-4c38-8bb1-d45ceb681caa)

**To add a patient to the database:**
- Choose the POST option with the following URL: http://127.0.0.1:5000/add_patient
- Insert the following patient details in the body:
'
{
    "patient_id": "345678908",
    "first_name": "Maya",
    "last_name": "Cohen",
    "city": "Haifa",
    "street": "HaNassi",
    "number": 8,
    "date_of_birth": "1985-09-20",
    "telephone": "048888888",
    "mobile": "0529876543",
    "vaccine_date_1": "2021-02-14",
    "manufacturer_1": "Pfizer",
    "positive_date": "2021-03-14",
    "recovery_date": "2021-03-22"
}
'
- Click on SEND
You will see below tha massage "Patient added successfully"
![image](https://github.com/rkriger98/corona_management_system/assets/73111633/98d0412c-ae7c-4b6d-a6b2-eaa5bd8a3c43)

## Input Integrity
This program checks for input integrity to ensure that the user enters valid data. Here's what is being checked:

- Proper ID number.
- Telephone and cell phone numbers are correct.
- Reasonable dates: for date of birth, date of infection and recovery from corona, date of vaccination.
- Correct names for vaccine manufacturers.

If the user inputs invalid data, the program will issue an appropriate message.

![image](https://github.com/rkriger98/corona_management_system/assets/73111633/23a5bc1b-a7dd-4a2c-990e-0c8633e01caa)

## Assumptions:

- To add a vaccine to a patient's record, both the vaccine manufacturer and the date of vaccination must be provided. 
- When adding a positive COVID-19 test result to a patient's record, both the date of infection and the date of recovery must be provided.


