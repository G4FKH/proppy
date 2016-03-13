import cgi
import math
import os
import re
import sys

from flask import Flask, render_template, url_for, redirect, request, send_from_directory, flash

from collections import OrderedDict

from app.util import htmlspecialchars_decode

from . import main

from .forms import P2PForm

@main.route('/')
@main.route('/p2p')
def p2p_predict():
    p2p_form = P2PForm
    return render_template('p2p.html', p2p_form=p2p_form)
