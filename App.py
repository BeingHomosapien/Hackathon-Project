from flask import Flask,render_template,redirect , url_for,request,session,logging,flash
from flask_mysqldb import MySQL
from functools import wraps


app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='rohanraj@123'
app.config['MYSQL_DB']='Web'
app.config['MYSQL_CURSORCLASS']='DictCursor' # the row data is stored as dictionary
mysql = MySQL(app)
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/employee')
def employee():
	return render_template('employee.html')

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		app.logger.info(username)
		app.logger.info(password)
		cur = mysql.connection.cursor()
		result = cur.execute('Select * from admini where username = %s',[username])
		if result > 0:
			data = cur.fetchone()
			if username == 'admin' or username == 'admini1':
				if password == data['password']:
					session['logged_in'] = True
					session['useranme'] = username # Session is something which stores data in cookies.
					flash("You are now Logged in.",'success')
					return redirect(url_for('admin', username = username)) # These are the request parameter not template params
				else:
					flash('Incorrect User-Password','danger')
					app.logger.info('Invalid Password')
			elif username=='employee':
				if password == data['password']:
					session['logged_in'] = True
					session['username'] = username
					
					flash("You are now Logged in.",'success')
					return redirect(url_for('employee'))
				else:
					app.logger.info('Invalid Password')
			else:
				if password==data['password']:
					session['logged_in'] = True;
					session['username'] = username;
					flash('Yau have logged into Complaint Section','success')

					return redirect(url_for('complaint_dashboard'))

		else:
			flash('No such User exists','danger')
		        
	return render_template('index.html')
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You have to login first','danger')
            return redirect(url_for('login'))
    return wrap# indentation is to take care otherwise decorator return none type producing Assertion Error


# @app.route('/complaint')
# def complaint():
# 	return render_template('complaint.html')
@app.route('/complaint_dashboard')
@is_logged_in
def complaint_dashboard():
	cur = mysql.connection.cursor()
	result = cur.execute("Select*from comaplaint")

	data = cur.fetchall()
	if result>0:
		return render_template('complaint_dashboard.html',data = data,username = request.args.get('username')) # data is a tuple with its elements as the rows of the result got.
		
	else:
		flash('No Data Found','danger')
	return render_template('complaint_dashboard.html')

@app.route('/admin')
@is_logged_in
def admin():
	cur = mysql.connection.cursor()
	result = cur.execute("Select*from admini")

	data = cur.fetchall()
	if result>0:
		app.logger.info(request.args.get('username'))
		return render_template('admin.html', data= data , username = request.args.get('username') ) # this is the way to access request params
	else:
		flash('No Data Found','danger')
	return render_template('admin.html')


@app.route('/about')
def about():
	
	return render_template('about.html')

@app.route('/admin/Affidavit1')
@is_logged_in
def admin_affi1():
	cur = mysql.connection.cursor()
	result = cur.execute("Select*from affi1")

	data = cur.fetchall()
	if result>0:
		return render_template('admin_affi1.html',data= data)
	else:
		flash('No Data Found','danger')
	return render_template('admin_affi1.html')


@app.route('/employee/Affidavit1')
@is_logged_in
def employee_affi():
	cur = mysql.connection.cursor()
	result = cur.execute("Select*from affi1")

	data = cur.fetchall()
	if result>0:
		return render_template('employee_affi.html',data= data)
	else:
		flash('No Data Found','danger')
	return render_template('employee_affi.html')



@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out",'success')
    return redirect(url_for('login'))

@app.route('/delete/<string:id>',methods=['POST'])
@is_logged_in
def delete_row(id):
	cur = mysql.connection.cursor()

	cur.execute("Delete from affi1 where ID=%s",[id])

	mysql.connection.commit()
	flash('Deleted Successfully','danger')
	cur.close()
	return redirect(url_for('admin_affi1'))

@app.route('/complaint',methods=['POST','GET'])
def complaint():
	if request.method=='POST':
		complaint = request.form['complaint']
		address = request.form['address']
		category = request.form['type']
		cur = mysql.connection.cursor()
		cur.execute('Insert into comaplaint(complaint,address,category) values(%s,%s,%s)',(complaint,address,category))
		mysql.connection.commit()
		flash('Complaint Registered Successfully','success')
		cur.close()
	return render_template('complaint1.html')


@app.route('/Affidavit1' ,methods=['GET','POST'])
def afffi1():
	if request.method=='POST':
		name = request.form['name']
		fathername = request.form['fathername']
		address = request.form['address']
		newname = request.form['newname']
		oldname = request.form['oldname']
		phonenumber = request.form['phonenumber']
		cur = mysql.connection.cursor()
		cur.execute('Insert Into affi1(Name,FatherName,OldName,NewName,Address,Phone_Number) values(%s,%s,%s,%s,%s,%s)',(name,fathername,oldname,newname,address,phonenumber))
		mysql.connection.commit()
		flash('Request Registered Successfully','success')
		cur.close()
	return render_template('Affi1.html')

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)