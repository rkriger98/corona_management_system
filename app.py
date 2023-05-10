from flask import Flask, request

from HMO_server.actions import get_patients, add_patient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    try:
        return get_patients()
    except ValueError as e:
        return str(e)


# Add a new patient
@app.route('/add_patient', methods=['POST'])
def add():
    try:
        return add_patient(request.json)
    except ValueError as e:
        return str(e)
