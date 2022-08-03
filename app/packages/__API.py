import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase
import os



__SIGN_API_URL = "https://paperinsert.herokuapp.com/api/paperinsert/account/signup"

__VERIFY_OTP_URL = "https://paperinsert.herokuapp.com/api/paperinsert/account/codeVerification"

__UPLOAD_FORM_URL = 'https://paperinsert.herokuapp.com/api/paperinsert/form/create'

__LOGIN_API_URL = "https://paperinsert.herokuapp.com/api/paperinsert/account/login"

def postSignup(data) -> dict:
    r = requests.post(__SIGN_API_URL, json=data, headers={'Content-Type':"application/json"})
    return r.json()

def verifyOtp(otpData) -> dict:
    r = requests.post(__VERIFY_OTP_URL, json=otpData, headers={'Content-Type':"application/json"})
    return r.json()

def uploadForm(formData):
    r = requests.post(__VERIFY_OTP_URL, json=formData, headers={'Content-Type':"application/json"})
    print(r.json())
    
def postLogin(loginData):
    r = requests.post(__VERIFY_OTP_URL, loginData, headers={'Content-Type':"application/json"})
    print(r.text)
    
class FIREBASE:
    
    __API_KEY = "AIzaSyD4mrtArsE6Ct5mwvlsFRvd7ivM54wHhxI"
    firebaseConfig = {
        'apiKey': "AIzaSyD4mrtArsE6Ct5mwvlsFRvd7ivM54wHhxI",
        'authDomain': "paperinsert-728e5.firebaseapp.com",
        'projectId': "paperinsert-728e5",
        'storageBucket': "paperinsert-728e5.appspot.com",
        'messagingSenderId': "1011858617668",
        'appId': "1:1011858617668:web:a921d7bbc22753ff9b5311",
        'measurementId': "G-BWH2F522PJ",
        'databaseURL':''
        }
    server_json_path = os.path.join('packages', 'serviceAccount.json')
    def __init__(self) -> None:
        cred = credentials.Certificate(self.server_json_path)
        firebase_admin.initialize_app(cred)
        try:
            self.db = firestore.client()
            self.userRef = self.db.collection(u'users')
        except:pass

    
    def singin(self, email, password):
        print("email, password: ",email, password)
        firebase = pyrebase.initialize_app(self.firebaseConfig)
        auth = firebase.auth()
        try:
            auth.sign_in_with_email_and_password(email, password)
            username = self.getFromFirestore('fullname',email)
            print("username: ",username)
            return True, username
        except:
            return False, None
        
    def getFromFirestore(self, dataToGet,documentEmail):
        #print("FROM GET FROME FIRESTORE: ",self.userRef.document('nbxmvyjskwf@arxxwalls.com').get().to_dict())
        doc = self.userRef.document(documentEmail).get()  
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
            print("/n/tFinal value: ",doc.to_dict()[dataToGet])
            return doc.to_dict()[dataToGet]
        else:
            print(u'No such document!')
            return None
        #return self.userRef.document(documentEmail).get(dataToGet).to_dict()  
    
    
    def setDocument(self, collection_name, doc_name, setData):
        self.db.collection(collection_name).document(doc_name).set(setData)

    def newUser(self, details):
        details['returnSecureToken'] = True
        # send post request
        r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(self.__API_KEY),data=details)
        #check for errors in result
        if 'error' in r.json().keys():
            return {'status':True,'error':r.json()['error']['message']}
        #if the registration succeeded
        if 'idToken' in r.json().keys() :
            self.userRef.document(details['email']).set({"username":details['username']})
            return {'status':False,'idToken':r.json()['idToken'], "email":details['email'], "username":details['username']}
        
    def firestorePostFormdata(self, email, data):
        self.db.collection('form').document(email).set(data)
        
        
        
        """
        const firebaseConfig = {
            apiKey: "AIzaSyD4mrtArsE6Ct5mwvlsFRvd7ivM54wHhxI",
            authDomain: "paperinsert-728e5.firebaseapp.com",
            projectId: "paperinsert-728e5",
            storageBucket: "paperinsert-728e5.appspot.com",
            messagingSenderId: "1011858617668",
            appId: "1:1011858617668:web:a921d7bbc22753ff9b5311",
            measurementId: "G-BWH2F522PJ"
          };
        
        """