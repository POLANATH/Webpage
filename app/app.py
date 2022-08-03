from flask import Flask
from flask import redirect, render_template, url_for, request, session, abort

# Import from packages
from packages.__API import FIREBASE
import os


# Initialize Template Path
__TEMPLATE_PATH = "templates"

# Initialize App
app = Flask(__name__, template_folder=__TEMPLATE_PATH)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config['SECRET_KEY'] = "thisismykjklsrkjl3k4324i9034903493849032843j"


firebase = FIREBASE()


# Initialize debug = True
__DEBUG = True

# Initialize methods
__METHODS = ["POST", "GET"]

# Initialize Routes
__HOME_ROUTE = "/"
__SIGNUP_ROUTE = '/signup'
__LOGIN_ROUTE = "/login"
__OTP_VERIFY_ROUTER = "/verifyOTP"
__DASHBOARD_ROUTE = "/dashboard"
__ORDER_ROUTE = "/order"
__LOGOUT_ROUTE = "/logout"



# Home route
@app.route(__HOME_ROUTE)
def home():
    print("home called")
    if session.get('completeProfile')==False:
        return redirect(url_for('completeProfile'))
    if 'email' in session:#and 'otpVerified' in session:
        print("HOME: SESSION: ",session.get('email'))
        print("HOME sesision")
        return render_template("components/home.html", session=session, context={"status":False})
    print("home called Get")
    return render_template("components/home.html", session=None, context={"status":False})


@app.route(__SIGNUP_ROUTE, methods=__METHODS)
def signup():

    if 'email' in session and session.get('completeProfile') == False:
        return redirect(url_for('completeProfile'))
    if request.method == "POST":
        signupData = request.form.to_dict()
        print(signupData)
        
        print('passed++')
        print(signupData['response[user_data][email]'], signupData['response[user_data][displayName]'], firebase.getFromFirestore('completeProfile', signupData['response[user_data][email]']))
        session['username'] =None# signupData['response[session_data][username]']
        session['email'] = signupData['response[user_data][email]']
        session['completeProfile'] = firebase.getFromFirestore('completeProfile', signupData['response[user_data][email]'])
        print(signupData['response[user_data][email]'], signupData['response[user_data][displayName]'])
        
        print('passed++')
        
        return render_template('components/profile.html',context={"status":False}, email=signupData['response[user_data][email]'] ,
                                   phoneno= "", 
                                   dispname=signupData["response[user_data][displayName]"], 
                                   fullname=signupData["response[user_data][displayName]"])

    return render_template("auth/signup.html", session=None, context={"status":False}, msg=None)


 
@app.route(__LOGIN_ROUTE, methods=__METHODS)
def login():
    if 'email' in session and session.get('completeProfile') == False:
        return redirect(url_for('completeProfile'))
    if request.method == "POST":
        loginData = request.form.to_dict()
        print(loginData)
        print('passed++signup')
        try:
            print("google login")
            session['username'] = firebase.getFromFirestore('fullname', loginData['response[user_data][email]'])
            session['email'] =loginData['response[user_data][email]']
            session['completeProfile'] = firebase.getFromFirestore('completeProfile',loginData['response[user_data][email]'])
            print(session.get('email'), session.get('completeProfile'), session.get('username'))
            print("This is google\a")
            if session['email'] == None and session['completedProfile'] == None:
                return redirect(url_for('completeProfile'))
            return redirect(url_for('home'))
        except Exception as e:
            print("normal login",e)
            isUser, username = firebase.singin(loginData['email'], loginData['password'])
            print("ISUSER< USERNAME: ", isUser,username)
            if isUser == True:
                session['username'] = username#firebase.getFromFirestore('fullname', loginData['response[session_data][email]'])
                session['email'] = loginData['email']
                session['completeProfile'] = firebase.getFromFirestore('completeProfile',loginData['email'])
                print(session.get('email'), session.get('completeProfile'), session.get('username'))
                return redirect(url_for('home'))
            else:
                return render_template("auth/login.html", session=None, context={"status":True}, msg={"status":True,"error":"User doesn't found.."})
            
    return render_template("auth/login.html", session=None, context={"status":False}, msg=None)


@app.route("/completeProfile", methods=__METHODS)  
def completeProfile():

    if 'email' in session:# and 'otpVerified' in session:
        print("completeProfioe SESSION ERMIAL: ",session.get('emali'))
        if request.method == "POST":
            print(request.form.to_dict())
            userDetails = request.form.to_dict()
            print(userDetails)
            session['completeProfile'] = True
            userDetails['completeProfile'] = True
            firebase.setDocument('users', str(userDetails['email']), userDetails)
            
            return redirect(url_for('home'))
    return render_template('components/profile.html', context={"status":False}, email=session.get('email'), phoneno="", dispname="")
    #return redirect(url_for('home'))  
 
@app.route('/form', methods=__METHODS)
def form():
    if 'email' in session:
        return render_template('components/tutor_register.html')
    return redirect(url_for('home'))

@app.route(__LOGOUT_ROUTE)
def logout():
    if 'email' in session :#and 'otpVerified' in session:
        try:
            del session['email']
            del session['username']
            del session['completeProfile']
        except:pass
        return redirect(url_for('home')) 
    return redirect(url_for('home')) 

# Run the App
if __name__ == "__main__":
    app.secret_key = 'akdfjldskfjldkfjdlkfjdlkfjdslkfjdskljflkdjfkld'
    app.run(debug=__DEBUG)