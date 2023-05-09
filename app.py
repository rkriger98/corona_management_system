from flask import Flask

from HMO_server.actions import get_patients, add_patient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    try:
        return get_patients()
    except ValueError as e:
        return str(e)


# Add a new member
@app.route('/add_patient', methods=['POST'])
def add():
    try:
        return add_patient()
    except ValueError as e:
        return str(e)
