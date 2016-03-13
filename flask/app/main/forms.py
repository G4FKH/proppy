from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField, IntegerField, DecimalField, TextField
from wtforms.validators import Required, Length, NumberRange
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class P2PForm(Form):
    tx_lat = DecimalField("Latitude", validators=[Required(), NumberRange(-90, 90)])
    tx_lon = DecimalField("Longitude", validators=[Required(), NumberRange(-180, 180)])

    submit = SubmitField("Submit")

    """
    rma = TextField("RMA", validators=[Length(0, 30)])
    cust_ref = StringField("Customer Ref", validators=[Length(0, 50)])
    project_code = IntegerField("Project Code", validators=[NumberRange(min=400, message="Invalid Project Code"), Required()])
    eq_manufacturer = StringField("Manufacturer", validators=[Required(), Length(1, 30)])
    eq_description = StringField("Description", validators=[Required(), Length(1, 30)])
    eq_part_no = StringField("Part Number", validators=[Required(), Length(1, 30)])
    eq_ser_no = StringField("Serial Number", validators=[Required(), Length(1, 30)])
    fault_description = TextAreaField("Description of Fault", validators=[Required()])
    fault_configuration = TextAreaField("Equipment Configuration")
    notes = TextAreaField("Notes")
    """
