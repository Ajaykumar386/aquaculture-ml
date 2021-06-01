from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField,TextAreaField,RadioField,SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

class PredictForm(FlaskForm):
   Dissolved_Oxygen = StringField('Dissolved Oxygen')
   pH = StringField('pH')
   Total_Dissolved_Solids = StringField('TDS')
   Temperature = StringField('Temperature')
   Turbidity = StringField('Turbidity')
   Conductivity = StringField('Conductivity')
   submit = SubmitField('Predict')
   abc = "" # this variable is used to send information back to the front page
