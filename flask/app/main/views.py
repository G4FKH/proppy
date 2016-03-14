from flask import render_template

from . import main

from .forms import P2PForm, AreaForm

@main.route('/')
@main.route('/p2p')
def p2p_predict():
    p2p_form = P2PForm()
    return render_template('p2p.html', p2p_form=p2p_form)

@main.route('/area')
def area_predict():
    area_form = AreaForm()
    return render_template('area.html', area_form=area_form)
