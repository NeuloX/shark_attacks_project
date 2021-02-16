from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Database Setup
#################################################

# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy as sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table
#################################################
# Predict Setup
#################################################
import matplotlib.pyplot as plt
#%matplotlib inline

import os
import numpy as np
import tensorflow as tf

from PIL import Image
import requests
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import (
    VGG19, 
    preprocess_input, 
    decode_predictions
)

# DATABASE_URL will contain the database connection string:
app.config['postgres://roiwimyplsisvt:7a68b737557eb6182ab100fabbf6e4e8e080b5132ca425d81b9fbaf9eb737c0b@ec2-52-205-61-60.compute-1.amazonaws.com:5432/d5ug7elorgd6et'] = os.environ.get('heroku pg:psql postgresql-curly-06176 --app shark-attacks', '')
# Connects to the database using the app config
db = sqlalchemy(app)


#test

engine = create_engine('postgres://roiwimyplsisvt:7a68b737557eb6182ab100fabbf6e4e8e080b5132ca425d81b9fbaf9eb737c0b@ec2-52-205-61-60.compute-1.amazonaws.com:5432/d5ug7elorgd6et')

Base = automap_base()
Base.prepare(engine, reflect=True)

#Pdf = Base.classes.pdf_scrape
Attacks = Base.classes.shark_attacks



# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    session = Session(engine)

    results = session.query(Attacks.case_number,  Attacks.year, Attacks.country, Attacks.type, Attacks.species, Attacks.fatal, Attacks.sex)
    #filter(Pdf.case_number == Attacks.case_number).all()

    case_number = [result[0] for result in results]
    #moonphase = [result[1] for result in results]
    year = [result[1] for result in results]
    country = [result[2] for result in results]
    attack_type = [result[3] for result in results]
    species = [result[4] for result in results]
    fatal = [result[5] for result in results]
    sex = [result[6] for result in results]
    
    


    attack_data = [{
        "case_number": case_number,
        "year": year,
        "country": country,
        "type": attack_type,
        "species": species,
        "fatal": fatal,
        "sex": sex
        #"moonphase": moonphase
    }]

    return jsonify(attack_data)

@app.route("/", methods=['post', 'get'])
def getshark():
    # Load the VGG19 model
    # https://keras.io/api/applications/vgg/#vgg19-function
    model = VGG19(include_top=True, weights='imagenet')
    # Load the image and resize to default image size
    url = request.form.get('url_field')
    #url = "https://images.theconversation.com/files/43861/original/6gqj734n-1394723838.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip"
    im = Image.open(requests.get(url, stream=True).raw)
    new_image = im.resize((224, 224))
    #plt.imshow(new_image)
    # Preprocess image for model prediction
    # This step handles scaling and normalization for VGG19
    x = image.img_to_array(new_image)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # Make predictions
    predictions = model.predict(x)
    test = decode_predictions(predictions, top=1)
    for m in test[0]:
        c,w,d = m
        print(w)
    w = w.replace("_"," ")


    #return url_for(redirect("home"),w=w)
    return render_template('index.html', w=w)






if __name__ == "__main__":
    app.run(debug=True)