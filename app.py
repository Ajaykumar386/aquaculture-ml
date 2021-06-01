from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key'

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)


@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():
        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        API_KEY = "iLXV738U436OPtjd9-J78fcxs8KuatpnmoZvQ570us74"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
                                       "apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + mltoken}

        if(form.Dissolved_Oxygen.data == None):
            python_object = []
        else:
            python_object = [float(form.Dissolved_Oxygen.data), float(form.pH.data), int(form.Total_Dissolved_Solids.data),
                             float(form.Temperature.data), int(form.Turbidity.data), float(form.Conductivity.data)]
        # Transform python objects to  Json

        userInput = []
        userInput.append(python_object)
        print(userInput)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": [
            "DO", "PH", "TDS", "Temperature", "Turbidity", "Conductivity"], "values": userInput}]}
        print(payload_scoring)
        response_scoring = requests.post('https://jp-tok.ml.cloud.ibm.com/ml/v4/deployments/b9b18f62-5a51-426d-a15d-61743b8e3760/predictions?version=2021-05-29',
                                         json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
            ab = output[key]

        for key in ab[0]:
            bc = ab[0][key]

        roundedCharge = round(bc[0][0], 2)
        per = (bc[0][1][1])

        form.abc = roundedCharge  # this returns the response back to the front page
        form.perc = per*100
        return render_template('index.html', form=form)
