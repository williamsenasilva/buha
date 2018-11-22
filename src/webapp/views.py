from flask import Flask, request, render_template, redirect, url_for, flash, Markup, session, send_file, json, jsonify
import os
import glob
import calendar
import time
from datetime import datetime
from models import *
from random import randint
from dht import Node, DHT
from helper import *
import ast 

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
    # remove caminho do diretório
    tree = tree.replace(base_path,'')
    # converte novamente para tipo dict
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
        # for i in range(10):
        #     os.makedirs(new_folder+'/'+str(i))
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

@app.route('/update-student',methods=['POST'])
def update_student():
    if not student:
        message = Markup('produto de código <b>%s</b> não foi encontrado.'%(request.form['code'].upper()))
        flash(message,'danger')
        return redirect(url_for('list_students'))
    student.description = request.form['description'].upper()
    student.price = request.form['price']
    student.quantity = request.form['quantity']
    message = Markup('produto de código <b>%s</b> foi atualizado.'%(request.form['code'].upper()))
    flash(message,'info')
    return redirect(url_for('list_students'))

@app.route('/delete-student/<code>',methods=['GET'])
def delete_student(code):
    if not student:
        message = Markup('produto de código <b>%s</b> não foi encontrado.'%(code.upper()))
        flash(message,'danger')
        return redirect(url_for('list_students'))
    Student.query.filter_by(code=code).delete()
    message = Markup('produto de código <b>%s</b> foi removido.'%(code.upper()))
    flash(message,'warning')
    return redirect(url_for('list_students'))

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
    dht.store(dht.start_node, student.academic_id, student)

    new_file = app.root_path + '/static/dht/' + session.get('moment') + '/' + str(dht.find_node(dht.start_node, student.academic_id)._id) + '/' + str(student.academic_id) + '.txt'
    create_file(new_file, str(student.__dict__))

    message = Markup("Aluno <b>" + student.name + "</b> foi inserido")
    flash(message,'success')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/insert-server',methods=['POST'])
def insert_server():
    new_folder = app.root_path + '/static/dht/' + session.get('moment') + '/' + str(int(time.time()))
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    
    dht = create_dht(session)

    message = Markup("Um novo servidor foi adicionado")
    flash(message,'success')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

def create_dht(session):
    dht = DHT(5)
    path = app.root_path + '/static/dht/' + str(session.get('moment'))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dht.join(Node(int(name)))
    dht.update_all_tables()
    return dht