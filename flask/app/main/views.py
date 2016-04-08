from datetime import datetime, timedelta
from flask import render_template, current_app, make_response
import json

from . import main

from .forms import P2PForm, AreaForm

@main.route('/')
@main.route('/p2p')
def p2p_predict():
    p2p_form = P2PForm()

    min_year = current_app.config['MIN_YEAR']
    min_month = current_app.config['MIN_MONTH']
    max_year = current_app.config['MAX_YEAR']
    max_month = current_app.config['MAX_MONTH']

    return render_template('p2p.html', p2p_form=p2p_form, min_month=min_month, min_year=min_year, max_month=max_month, max_year=max_year)

@main.route('/area')
def area_predict():
    area_form = AreaForm()
    min_year = current_app.config['MIN_YEAR']
    min_month = current_app.config['MIN_MONTH']
    max_year = current_app.config['MAX_YEAR']
    max_month = current_app.config['MAX_MONTH']

    return render_template('area.html', form=area_form, min_month=min_month, min_year=min_year, max_month=max_month, max_year=max_year)


@main.route('/areatest')
def area_predict_test():
    area_form = AreaForm()
    min_year = current_app.config['MIN_YEAR']
    min_month = current_app.config['MIN_MONTH']
    max_year = current_app.config['MAX_YEAR']
    max_month = current_app.config['MAX_MONTH']

    return render_template('areatest.html', form=area_form, min_month=min_month, min_year=min_year, max_month=max_month, max_year=max_year)


@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
      """Generate sitemap.xml. Makes a list of urls and date modified."""
      pages=[]
      ten_days_ago=(datetime.now() - timedelta(days=7)).date().isoformat()
      # static pages
      for rule in current_app.url_map.iter_rules():
          print(rule)
          if "GET" in rule.methods and len(rule.arguments)==0:
             print(rule)
             pages.append(["http://139.162.54.202"+str(rule.rule),ten_days_ago])

      sitemap_xml = render_template('sitemap_template.xml', pages=pages)
      response=make_response(sitemap_xml)
      response.headers["Content-Type"] = "application/xml"

      return response
    except Exception as e:
        return(str(e))
