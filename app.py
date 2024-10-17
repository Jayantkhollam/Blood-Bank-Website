from flask import Flask, render_template, request, jsonify
import pandas as pd
from functions import save_Blood_bank_data, save_hospital_data,show_on_map,send_email,qtt_update

app = Flask(__name__)

global blood_bank,blood_bank_address,order_name,order_address,order_mobile,order_email,lat,longi

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login.html')
def sign_in():
    return render_template('login.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/register.html')
def register_route():
    return render_template('register.html')

@app.route('/placeorder.html')
def order_route():
    return render_template('placeorder.html')

@app.route('/register', methods=['GET','POST'])
def register():
    hosp_data_base = pd.read_excel('static/documents/Hosp_Registation_data.xlsx')
    bb_data_base = pd.read_excel('static/documents/BB_Registation_data.xlsx')
    BB_name = request.form.get('bloodBankName')
    BB_contact_p_name = request.form.get('contactPersonName')
    BB_email = request.form.get('bloodBankEmail')
    BB_pass = request.form.get('bloodBankPassword')
    BB_phone = request.form.get('phoneNumber')
    if BB_name != None:
        if BB_email in bb_data_base['Email'].values:
            return jsonify({'status': "Email Already Registered!"})
        else:
            save_Blood_bank_data(BB_name,BB_contact_p_name,BB_email,BB_pass,BB_phone)
            return jsonify({'status': "Registration Successful!"})
    
    hosp_name = request.form.get('hospitalName')
    hosp_contact_p_name = request.form.get('hospitalContactPersonName')
    hosp_email = request.form.get('hospitalEmail')
    hosp_pass = request.form.get('hospitalPassword')
    hosp_phone = request.form.get('hospitalPhoneNumber')
    hosp_lat = request.form.get('hospitalLatitude')
    hosp_long = request.form.get('hospitalLongitude')
    if hosp_name != None:
        if hosp_email in hosp_data_base['Email'].values:
            return jsonify({'status': "Email Already Registered!"})
        else:
            save_hospital_data(hosp_name,hosp_contact_p_name,hosp_email,hosp_pass,hosp_phone,hosp_lat,hosp_long)
            return jsonify({'status': "Registration Successful!"})
    return render_template('register.html')
        

@app.route('/log in', methods = ['GET','POST'])
def login():
    global lat,longi
    hosp_data_base = pd.read_excel('static/documents/Hosp_Registation_data.xlsx')
    bb_data_base = pd.read_excel('static/documents/BB_Registation_data.xlsx')
    login_type = request.form.get('user_type')
    email = request.form.get('email')
    password = request.form.get('password')
    print(login_type,email,password)
    if login_type == 'hospital':
        idx = hosp_data_base[hosp_data_base['Email'] == email]['Hosp Password'].index
        if email in hosp_data_base['Email'].values and password == hosp_data_base[hosp_data_base['Email'] == email]['Hosp Password'][idx[0]]:
            lat = float(hosp_data_base[hosp_data_base['Email'] == email]['latitude'])
            longi = float(hosp_data_base[hosp_data_base['Email'] == email]['longitude'])
            return render_template('inner_hosp_avail.html')
    else:
        idx = bb_data_base[bb_data_base['Email'] == email]['Bb Password'].index
        if email in bb_data_base['Email'].values and password == bb_data_base[bb_data_base['Email'] == email]['Bb Password'][idx[0]]:
            return render_template('inner_bank.html')

@app.route('/hospital login', methods = ['GET','POST'])
def hosp_login():
    global blood_type,qtt
    main_blood_b_data = pd.read_excel('static/documents/main_blood_bank_data.xlsx')
    blood_type = request.form.get('blood_type')
    qtt = request.form.get('qtt')
    # print(blood_type)
    print(lat,longi)
    show_on_map(blood_type,main_blood_b_data,qtt,lat,longi)
    return render_template('inner_hosp2.html')

@app.route('/process_selected_data', methods = ['GET','POST'])
def data_for_order():
    global blood_bank,blood_bank_address
    selected_data = request.json.get('selectedData')
    blood_bank = selected_data[0][0]
    blood_bank_address = selected_data[0][1]
    print(blood_bank,blood_bank_address)
    return render_template('placeorder.html')

@app.route('/order_details', methods = ['GET','POST'])
def order_details():
    global order_name,order_address,order_mobile,order_email
    order_name = request.form.get('name')
    order_address = request.form.get('address')
    order_mobile = request.form.get('mobile')
    order_email = request.form.get('email')
    print(order_name,order_address,order_mobile,order_email)
    return render_template('gateway.html')

@app.route('/recipt', methods = ['GET','POST'])
def receipt():
    send_email(order_email,order_name,blood_type,order_mobile,qtt,blood_bank)
    qtt_update(blood_bank,blood_type,int(qtt))
    return render_template('recipt.html',blood_type=blood_type,
                                        qtt=qtt,
                                        hsp_name=order_name,
                                        hsp_add=order_address,
                                        hsp_phone=order_mobile,
                                        hsp_email=order_email,
                                        bnk_nm=blood_bank)

@app.route('/update_qtt', methods = ['GET','POST'])
def quantity_update():
    name = request.form.get('bank_name')
    b_type = request.form.get('blood_type')
    qtt = request.form.get('qtt')
    qtt_update(name,b_type,int(qtt),'add')
    return render_template('inner_bank.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')