from flask import render_template

from . import main

from .forms import P2PForm

@main.route('/')
@main.route('/p2p')
def p2p_predict():
    p2p_form = P2PForm()
    return render_template('p2p.html', p2p_form=p2p_form)
