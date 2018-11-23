from flask import Flask, request, render_template, redirect, url_for, flash, Markup, session, send_file, json, jsonify
import os
import glob
import calendar
import time
from models import *
from random import randint
from dht import Node, DHT
from helper import *
import ast 
import random

app = Flask(__name__)
app.config.from_object('config')

unixtime = int(time.time())
    
@app.route('/')
def home():
    if not session.get('logged'):
        return render_template('home.html',unixtime=unixtime)
    dht = create_dht(session)
    base_path = app.root_path + '/static/dht/'
    session_path = base_path + session.get('moment')
    tree = str(make_tree(session_path))
    tree = tree.replace(base_path,'')
    tree = ast.literal_eval(tree)
    return render_template('home.html',session=session, tree=tree,unixtime=unixtime)

@app.route('/login')
def login():
    dht = create_dht(session)
    session['logged'] = True
    session['moment'] = str(int(time.time()))
    new_folder = app.root_path + '/static/dht/' + session.get('moment')
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        os.makedirs(new_folder+'/'+str(0))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    path_to_exclude = app.root_path + '/static/dht/' + session.get('moment')
    for root, dirs, files in os.walk(path_to_exclude, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path_to_exclude)
    session.clear()
    return redirect(url_for('home'))

@app.route('/insert-students')
def insert_students():
    students = random.sample(app.config['STUDENTS'], 100)
    for student in students:
        student = Student(student)
        dht = create_dht(session)
        student.buha_id = dht.get_hash_id(student.academic_id)
        dht.store(dht.start_node, student.academic_id, student)
        new_file = app.root_path + '/static/dht/' + session.get('moment') + '/' + str(dht.find_node(dht.start_node, student.academic_id)._id) + '/' + str(student.academic_id) + '.txt'
        create_file(new_file, str(student.__dict__).upper())
    message = Markup("Mais 100 alunos foram inseridos automaticamente")
    flash(message,'success')
    return redirect(url_for('home'))

@app.route('/insert-server')
def insert_server():
    new_folder = app.root_path + '/static/dht/' + session.get('moment') + '/' + str(randint(0,1024))
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    dht = create_dht(session)
    message = Markup("Um novo servidor foi adicionado")
    flash(message,'success')
    return redirect(url_for('home'))

@app.route('/files/', defaults={'request_path': ''})
@app.route('/files/<path:request_path>')
def files(request_path):
    unixtime = calendar.timegm(time.gmtime())
    dht_path = app.root_path + '/static/dht/'
    full_path = dht_path + request_path
    if not os.path.exists(full_path):
        session['user_message'] = 'caminho %s não existe'%(str(full_path).replace(dht_path,''))
        message = Markup(session.get('user_message'))
        flash(message,'danger')
        return render_template('home.html',session=session,unixtime=unixtime)
    if os.path.isfile(full_path):
        return send_file(full_path)

# API
@app.route('/api/insert-student',methods=['POST'])
def insert_student():
    data = request.get_json(force=True, silent=False, cache=False)
    student = Student(data)
    dht = create_dht(session)
    student.buha_id = dht.get_hash_id(student.academic_id)
    dht.store(dht.start_node, student.academic_id, student)
    new_file = app.root_path + '/static/dht/' + session.get('moment') + '/' + str(dht.find_node(dht.start_node, student.academic_id)._id) + '/' + str(student.academic_id) + '.txt'
    create_file(new_file, str(student.__dict__).upper())
    message = Markup("Aluno <b>" + student.name + "</b> foi inserido")
    flash(message,'success')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# todo: mover para helper.py
def create_dht(session):
    dht = DHT(10)
    path = app.root_path + '/static/dht/' + str(session.get('moment'))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dht.join(Node(int(name)))
    dht.update_all_tables()
    return dht