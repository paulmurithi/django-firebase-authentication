import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.certificate('/home/programmer/Downloads/grodigi-d809f-firebase-adminsdk-bgxm4-61f5bf15b9.json')

# firebaseConfig = {
#     "apiKey": "AIzaSyBGrLERNsFEqXUp77ikonHeHnXvPGlI3fo",
#     "authDomain": "grodigi-d809f.firebaseapp.com",
#     "projectId": "grodigi-d809f",
#     "storageBucket": "grodigi-d809f.appspot.com",
#     "messagingSenderId": "836251291368",
#     "appId": "1:836251291368:web:c3b740c208cdb93030435d",
#     "measurementId": "G-17BYP9PPT0"
#   }
  
default_app = firebase_admin.initialize_app(cred)
