from flask import render_template, current_app
import json

from . import main

from .forms import P2PForm, AreaForm

@main.route('/')
@main.route('/p2p')
def p2p_predict():
    p2p_form = P2PForm()
    with open(current_app.config['SSN_DATA_PATH']) as ssn_data_file:
        ssn = json.load(ssn_data_file)
    min_year = min(ssn.keys())
    min_month = min(ssn[min_year].keys())
    max_year = max(ssn.keys())
    max_month = max(ssn[max_year].keys())
    return render_template('p2p.html', p2p_form=p2p_form, min_month=min_month, min_year=min_year, max_month=max_month, max_year=max_year)

@main.route('/area')
def area_predict():
    area_form = AreaForm()
    return render_template('area.html', area_form=area_form)
