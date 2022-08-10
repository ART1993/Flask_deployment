import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import pickle
import os
HOUSE_FOLDER=os.path.join('static', 'img')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = HOUSE_FOLDER

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'black_home.png')
    return render_template('index.html',user_image = full_filename)


@app.route('/',methods=['POST'])
def predict():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'black_home.png')
    int_features=[int(x) for x in request.form.values()]
    final_features=[np.array(int_features)]
    prediction=model.predict(final_features)


    output = round(prediction[0],2)
    if output < 0:
        return render_template('index.html', prediction_text = "Predicted Price is negative, values entered not reasonable")
    elif output >= 0:
        return render_template('index.html', prediction_text = 'Predicted Price of the house is: ${}'.format(output))

if __name__ == '__main__':
    app.run(port=5000, debug=True)

