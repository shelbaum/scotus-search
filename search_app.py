from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date, datetime
import searchopinions

app = Flask(__name__)

app.config['SECRET_KEY'] = '498deafffad03e9adc2900f80314f687'

search_terms = ['Ablavsky', 'Alexander', 'Anderson', 'Babcock', 'Bankman', 'Banks', 'Belt', 'Brest', 
'Brodie', 'Callahan', 'Casper', 'Cohen', '\\bCole\\b', 'Craswell', 'Daines', 'Dauber', 'Dickson', 
'Donohue', 'Dwyer', 'Engstrom', 'Fisher\\b', 'Fletcher', 'Ford\\b', 'Franklin', 'Fried\\b', 'Friedman', 'Gilson', 
'Goldin\\b', 'Goldstein', 'Gordon', 'Gould', 'Greely', 'Grey', 'Grundfest', 'Guttentag', 'Heller\\b', 
'Hensler', '\\bHo\\b', 'Honigsberg', 'Humphreys', 'Jensen', 'Karlan', 'Kelman', 'Kessler', 'Klausner', 'Koski', 
'Lemley', 'MacCoun', 'Magill', 'Malone', 'Marshall', 'Martinez', 'McConnell', 'Melamed', 'Mello\\b', 'Meyler', 'Milhaupt', 
'Mills', 'Mitchell', 'Morantz', 'Nyarko', 'O’Connell', 'Ouellette', 'Persily', 'Polinsky', 'Rabin', 'Rhode', 'Schacter', 
'Simon', 'Sinnar', 'Sivas', 'Sklansky', 'Sonne', 'Spaulding', 'Srikantiah', 'Strnad', 'Studdert', 'Sykes', 
'Thompson', 'Triantis', 'Tyler', 'Schewick', 'Wald\\b', 'Weiner', 'Weisberg', 'Williams\\b', 'Zambrano', 'Berman', 
'Cu[ée]llar', 'Fadel', '\\bFina\\b', 'Hodrick', 'Perdomo', 'Schaack', 'Welton', 'Stanford', 'Stan\.', 'Reply', 
'Response\\b', 'Amicus', 'Brief\\b', 'CA10']

class DateForm(FlaskForm):
	start_date = DateField("From: ", format='%Y-%m-%d', validators=[DataRequired()])
	end_date = DateField("To: ", format='%Y-%m-%d', default=date.today())
	submit = SubmitField('Search')

	# def validate_dates(start_date, end_date):
	# 	start_date_obj=strptime(start_date, '%Y-%m-%d')
	# 	end_date_obj=strptime(end_date, '%Y-%m-%d')
	# 	date_range=end_date_obj-start_date_obj

	# 	if start_date_obj > end_date_obj:
	# 		raise ValidationError('Start date must be before end date.')
	# 	if date_range.days > 14:
	# 		raise ValidationError('Please search no more than 14 days at a time.')

@app.route('/', methods = ['POST', 'GET'])
def home(): 
	form = DateForm()
	
	try:
		results = request.form
		start_date = str(results.get("start_date"))
		end_date = str(results.get("end_date"))
		cases = searchopinions.searchopinions(search_terms, start_date, end_date)

		return render_template('home.html', form=form, cases=cases, search_terms=search_terms)
	except:
		return render_template('home.html', form=form, cases=[], search_terms=search_terms)
