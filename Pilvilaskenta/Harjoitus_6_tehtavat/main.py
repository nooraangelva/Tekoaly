from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image, ImageOps
import numpy as np
import time
import requests
import json
import firebase_admin
from firebase_admin import firestore

storage_client = storage.Client()
firebase_admin.initialize_app()

def hello_gcs(event, context):
    t = time.time()

    # ladataan kuva Google Storagesta "temp"-kansioon, josta saadaan se numpyn käsiteltäväksi
    bucket = storage_client.get_bucket(event['bucket'])
    AWS_address = "http://3.88.131.58:8501/v1/models/tensorflow:predict"
    AWS_header = {"Content-Type": "application/json"}
    blob = bucket.blob(event['name'])
    temp_location = "/tmp/"

    # jos kuvat ovat jossain alikansiossa, siivotaan ne pois
    # tässä oletus että tämä kansio on nimeltä "images"
    temp_file = event['name'].replace("images/", "")

    # Download file from bucket.
    blob.download_to_filename(temp_location + temp_file)

    image = Image.open(temp_location + temp_file)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    img_array = np.array(image)
    img_batch = np.expand_dims(img_array, axis=0)
    img_final = np.array(img_batch).astype(int)

    # TensorFlow Docker Image vaatii tässä formaatissa sisääntulevan datan (input = valokuva)
    request_body = {'instances': img_final.tolist()}
    print(request_body)
    sender = requests.post(AWS_address, data=json.dumps(request_body), headers=AWS_header)

    response = sender.text
    data = json.loads(response)
    prediction = np.array(data['predictions'])
    highest_index = prediction.argmax(axis=-1)[0]

    if highest_index == 0:
        print("auto")
    else:
        print("rekka")

    highest_index=int(highest_index)

    if highest_index == 1:
        db = firestore.client()

        doc_ref = db.collection(u'rekkatunnistus').document()
        doc_ref.set({
            u'imagename': event['name'],
            u'category': highest_index,
            u'time': firestore.SERVER_TIMESTAMP
        })

    # tulostetaan kellotukset
    elapsed_time = time.time() - t
    print(f"{elapsed_time} sekuntia.")

    data = db.child("rekkatunnistus").get()
    for temp in data.each():
        print(temp.key())

        print(temp.val())   