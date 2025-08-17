from flask import Flask , session , request , redirect , url_for , render_template , jsonify
from pymongo import MongoClient
from firebase_admin import credentials , auth
import firebase_admin



app = Flask(__name__)
app.secret_key = "hmi_class"

client = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ai']
GOOGLE_AUTH = db['GOOGLE_AUTH']
PUBLISH = db['PUBLISH']
cred = credentials.Certificate("fir-c24bc-firebase-adminsdk-olzh6-5d58acd2ef.json")
firebase_admin.initialize_app(cred)


@app.route("/")
def Continue_Hmi():
    return render_template("index.html")

@app.route("/get-user")
def Get_user():
    user_email = request.args.get("user")
    if user_email:
        session['hmi_community_email'] = user_email
        return jsonify({"Sucess":True , "data":"User Logged Suessfully..."})
    else:
        return jsonify({"Sucess":False , "data":"Something Went Wrong..."})
    

@app.route("/auth/google-login" , methods=['POST'])
def Google_login():
    try:
        User_token = request.json.get("token")
         
        decode_token = auth.verify_id_token(User_token)

        email = decode_token['email']
        name = decode_token.get("name" , "unknow")

        user = GOOGLE_AUTH.find_one({"email":email})

        if user:
            session['hmi_community_email'] = email
            return jsonify({"Sucess":True , "data":"Login Sucessfull"})
        else:
            data = {
                "name":name,
                "email":email
            }
            GOOGLE_AUTH.insert_one(data)
            session['hmi_community_email'] = email
            return jsonify({"Sucess":True , "data":"Login Sucessfull"})
    except:
        return jsonify({"Sucess":False , "data":"internal Server Error"})

@app.route("/hmi-community/dashboard")
def dashboard():
    email = session.get("hmi_community_email")
    if email:
       pub = PUBLISH.find({}).sort("_id" , -1)
       return render_template("dashboard.html" , email=email , pub=pub)
    else:
        return redirect("/")

@app.route("/profile")
def profile():
    email = session.get("email")
    if email:
        pub = PUBLISH.find({"user":email})
        return render_template("Uprojects.html" , pub=pub)

if __name__ == "__main__":
    app.run(debug=True , port=3000)