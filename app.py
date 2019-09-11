import os
import sys
import subprocess
import webbrowser
from flask import Flask, flash, redirect, url_for,render_template, request, session
from flask_script import Manager
from multiprocessing import Process
from echo import main,stop,set_server_start_time
from datetime import datetime
from threading import Timer

app = Flask(__name__)
manager=Manager(app)
p=None
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/startserver', methods=['GET', 'POST'])
def starts():
    global p
    p=Process(target=main)
    set_server_start_time(datetime.now())    
    p.start()
    return render_template('start.html')

@app.route('/stopserver', methods=['GET', 'POST'])
def stops():
    global p
    p.terminate()
    return render_template('stop.html')    

def open_browser():
    webbrowser.get("firefox").open_new_tab("http://localhost:5000/")

@manager.command
def runserver():
    open_browser()
    app.run()

if __name__ == "__main__":
    #t=Timer(2,open_browser)
    #t.start()
    manager.run()
    
