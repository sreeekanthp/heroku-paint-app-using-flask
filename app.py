
from __future__ import with_statement
from flask import Flask,request,session,g,redirect,url_for,abort,flash
from flask import render_template,jsonify
import pickle


from contextlib import closing
import json
import sqlite3

app=Flask(__name__)

#connect database
def connect_db():
    	return sqlite3.connect(DATABASE)

#initialize database
def init_db():
	db=sqlite3.connect('image.db')
	db.cursor().executescript("""drop table if exists entries;
				create table entries(
				filename string not null,
				imagedata string not null);""")
	db.commit()
	
#Our main program	
	
@app.route("/")
def hello():
	filename=[]
	wholedata=[]
	f= request.args.get('f')
	db=sqlite3.connect('image.db')
	cur=db.cursor().execute('select * from entries')
	for row in cur.fetchall():
		filename.append(row[0])
	return render_template("paint.html",lis=filename,imagedata=wholedata) 


@app.route("/h/",methods=['POST'])
def h():
	fname=request.form['f']
	imagedata=request.form['parameter']
	imagedata=pickle.dumps(imagedata)
	db=sqlite3.connect('image.db')	
	db.cursor().execute('insert into entries (filename,imagedata) values (?,?)',[fname,imagedata])
	db.commit()
	db.close()
	return redirect(url_for('hello'))
	
@app.route("/<filename>")
def draw(filename):
	wholedata=[]
	fname=[]
	db=sqlite3.connect('image.db')
	cur=db.cursor().execute('select * from entries')
	for row in cur.fetchall():
		fname.append(row[0])
		if filename==row[0]:
			wholedata=pickle.loads(row[1])
	return render_template("paint.html",lis=fname,imagedata=wholedata)
	
	
if __name__=="__main__":
	init_db()
	app.debug=True
	app.run()
