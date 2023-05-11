CREATE TABLE Address (
    address_id INT IDENTITY(1,1) PRIMARY KEY,
    city NVARCHAR(50) NOT NULL,
    street NVARCHAR(50) NOT NULL,
    number NVARCHAR(10) NOT NULL,
    CONSTRAINT UNQ_Address UNIQUE(city, street, number)
);

CREATE TABLE Patient (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    telephone NVARCHAR(20) NOT NULL,
    mobile NVARCHAR(20) NOT NULL,
    address_id INT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES Address(address_id)
);

CREATE TABLE Vaccine (
    vaccine_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    vaccine_date DATE NOT NULL,
    manufacturer NVARCHAR(80) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE Infection (
    infection_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    positive_date DATE NOT NULL,
    recovery_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);