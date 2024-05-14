from flask import Flask, render_template, redirect, url_for, request, flash
import csv
from utills import select_ROI
from utills import park_Model
import ast
import time




app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string

# Function to read credentials from CSV
def read_credentials():
    with open('credentials.csv', 'r') as file:
        reader = csv.DictReader(file)
        credentials = {row['username']: row['password'] for row in reader}
    return credentials

# Function to read cameras from CSV
def read_cameras():
    with open('cameras.csv', 'r') as file:
        reader = csv.DictReader(file)
        cameras = [row for row in reader]
    return cameras

# Function to write cameras to CSV
def write_cameras(cameras):
    with open('cameras.csv', 'w', newline='') as file:
        fieldnames = ['location', 'ip', 'roi','capacity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cameras)

# function to calculate available space
def calc_Available_Space(cameras):
    for camera in cameras:
        spaceList = park_Model.getAvailableSpace(camera['ip'], ast.literal_eval(camera['roi']), int(camera['capacity']))
        camera['free_spaces'] = spaceList[0]
        camera['percent_available'] = spaceList[1]
    


# Index page
@app.route('/')
def index():
    cameras = read_cameras()
    calc_Available_Space(cameras)
    return render_template('index.html', cameras=cameras)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        credentials = read_credentials()
        if credentials.get(username) == password:
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

# Logout functionality
@app.route('/logout')
def logout():
    # Here you can clear any session variables if needed
    return redirect(url_for('login'))

# Admin home page
@app.route('/adminHome')
def admin_home():
    cameras = read_cameras()
    return render_template('admin_home.html', cameras=cameras)

# Add camera functionality
@app.route('/addCamera', methods=['GET', 'POST'])
def add_camera():
    if request.method == 'POST':
        location = request.form['location']
        ip = request.form['ip']
        capacity = request.form['capacity']
        cameras = read_cameras()
        # Check if same IP already exists
        if any(camera['ip'] == ip for camera in cameras):
            flash('IP camera already exists.', 'error')
        else:
            time.sleep(2)
            roi = select_ROI.getCoordinates(ip)
            cameras.append({'location': location, 'ip': ip,'roi': roi, 'capacity': capacity})
            write_cameras(cameras)
            flash('Camera added successfully.', 'success')
            return redirect(url_for('admin_home'))
    return render_template('add_camera.html')

# Delete camera functionality
@app.route('/deleteCamera/<int:camera_id>')
def delete_camera(camera_id):
    cameras = read_cameras()
    del cameras[camera_id]
    write_cameras(cameras)
    flash('Camera deleted successfully.', 'success')
    return redirect(url_for('admin_home'))

if __name__ == '__main__':
    app.run(debug=True)
    
