import pandas as pd
import os
import folium
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import numpy as np

def save_Blood_bank_data(blood_b_name,contact_Person_Name,Bb_email,Bb_password,Bb_phone):
    row = {'Blood Bank Name': blood_b_name,'Contact Person Name': contact_Person_Name,'Email': Bb_email, 'Mobile': Bb_phone,
                    'Bb Password': Bb_password}
    if os.path.exists('static/documents/BB_Registation_data.xlsx'):
        df = pd.read_excel('static/documents/BB_Registation_data.xlsx')
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('static/documents/BB_Registation_data.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Blood Bank Name','Contact Person Name','Email','Mobile','Bb Password'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('static/documents/BB_Registation_data.xlsx',index=False)

def save_hospital_data(hostpital_name,contact_Person_Name,hosp_email,hosp_password,hosp_phone,hosp_lat,hosp_long):
    row = {'Hospital Name': hostpital_name,'Contact Person Name': contact_Person_Name,'Email': hosp_email, 'Mobile': hosp_phone,
                    'Hosp Password': hosp_password,'latitude':hosp_lat,'longitude':hosp_long}
    if os.path.exists('static/documents/Hosp_Registation_data.xlsx'):
        df = pd.read_excel('static/documents/Hosp_Registation_data.xlsx')
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('static/documents/Hosp_Registation_data.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Hospital Name','Contact Person Name','Email','Mobile','Hosp Password','latitude','longitude'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('static/documents/Hosp_Registation_data.xlsx',index=False)

def show_on_map(bllod_grp,new_df,qtt,lat,long):
    avail = new_df[new_df[bllod_grp] >= qtt]
    avail['distance(KM)'] = haversine(lat,long,avail['latitude'],avail['longitude'])
    avail = avail.sort_values(by='distance(KM)')
    save_excel = avail[['name','full_address','phone','email','distance(KM)']]
    save_excel.to_excel('static/documents/available_data_for_hospital.xlsx',index=False)
    initial_latitude = 18.5204
    initial_longitude = 73.8567
    # map with an initial view centered at a specific location
    mymap = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=11)
    # markers for each location
    for index, row in avail.iterrows():
        latitude = row['latitude']  
        longitude = row['longitude']  
        location_name = row['name'] 
        folium.Marker(location=[latitude, longitude], popup=location_name).add_to(mymap)
    mymap.save("static/maps/map.html")


def send_email(to_email,name,blood_type,order_mobile,qtt,blood_bank):
    from_email = 'esparktest@hotmail.com'
    password = 'Espark@123'
    current_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
    body = f"""Dear {name},

                We are pleased to inform you that your blood order has been successfully processed and confirmed.

                Order Details:
                - Order Date: {formatted_time}
                - Hospital Name: {name}
                - Contact Number: {order_mobile}
                - Blood Type: {blood_type}
                - Quantity: {qtt} bags

                Your order will be processed promptly, and you will be notified once the blood is ready for pickup or delivery.

                If you have any questions or need further assistance, please don't hesitate to contact us.

                Thank you for choosing our blood bank services.

                Best regards,
                {blood_bank}
                """

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Blood Order Confirmation"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    print("Email sent successfully!")
    server.quit()

def qtt_update(name,b_type,qtt,action=None):
    df = pd.read_excel(r'static\documents\available_data_for_blood_bank.xlsx')
    if action == 'add':
        df.loc[df['name'] == name, b_type] += qtt
    else:
        df.loc[df['name'] == name, b_type] -= qtt
    df.to_excel(r'static\documents\available_data_for_blood_bank.xlsx',index=False)

def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    radius_of_earth = 6371  
    distance = radius_of_earth * c

    return distance
