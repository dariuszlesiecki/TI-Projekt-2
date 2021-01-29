from app import app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.auth import login_required
from app.db import *
import datetime
import json

@app.route('/')
def index():
    return render_template('base.html')

    

@app.route('/add',methods=('GET', 'POST'))
@login_required
def add(): 
    
    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
        
        print(f"{g.user['id']}, {datetime.datetime.now()}, {title},{body}")
        insert(
                f"INSERT INTO post (author_id, created, title, body) VALUES ('{g.user['id']}', '{datetime.datetime.now()}', '{title}', '{body}')"
            )
        flash('Pomyślnie dodano!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/posts',methods=('GET', 'POST'))
@app.route('/posts/<int:id>',methods=('GET', 'POST'))
def posts(id = None):
    
    if id == None:
        
        records= execute_fetchall(
                "SELECT users.username, post.created as t, post.title, post.body, users.id FROM post JOIN users on users.id=post.author_id ORDER BY t DESC"
                )
    else:
        records= execute_fetchall(
                f"SELECT users.username, post.created as t, post.title, post.body, users.id FROM post JOIN users on users.id=post.author_id WHERE users.id='{id}' ORDER BY t DESC"
                )

    return render_template('posts.html',records=records)

@app.route('/myposts',methods=('GET', 'POST'))
def myposts():
    
    records= execute_fetchall(
            'SELECT users.username, post.created, post.title, post.body FROM post JOIN users on users.id=post.author_id'
            )
    return render_template('posts.html',records=records)

@app.route('/synchronize', methods=('POST',))
@login_required
def synchronize():
    if request.method == 'POST':
        data = json.loads(request.form['javascript_data'])
        
        print(f"{g.user['id']}, {data['created']}, { data['title']},{data['body']}")
        insert(
                f"INSERT INTO post (author_id, created, title, body) VALUES ('{g.user['id']}', '{data['created']}', '{data['title']}', '{data['body']}')"
            )
        flash('Pomyślnie dodano dane z bazy indexedDB!')
        return redirect(url_for('index'))
    
