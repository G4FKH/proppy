import numpy as np
import json
import os
import subprocess

from math import log10
from flask import request, current_app, jsonify, url_for, abort
from tempfile import NamedTemporaryFile

from proppy.rec533Out import REC533Out
from proppy.propAreaPlot import PropAreaPlot

from ..main.forms import P2PForm, AreaForm
from .validation_error import ValidationError
from .iturhfprop_error import ITURHFPropError

from . import ajax

@ajax.route('/predict', methods=['POST'])
def predict():
    #print(request.form)
    form = P2PForm(request.form)
    if request.method == 'POST' and form.validate():
        sys_pwr = 10 * log10(float(request.form['sys_pwr'])/1000.0)
        try:
            sys_year = int(request.form['year'])
        except:
            raise ValidationError("Invalid value for year.")
        sys_month = int(request.form['month'])
        sys_plot_type = request.form['sys_plot_type']

        tx_name = request.form['tx_name'].strip()
        tx_lat = float(request.form['tx_lat_field'])
        tx_lon = float(request.form['tx_lng_field'])
        tx_gain = float(request.form['tx_gain'])

        rx_name = request.form['rx_name'].strip()
        rx_lat = float(request.form['rx_lat_field'])
        rx_lon = float(request.form['rx_lng_field'])
        rx_gain = float(request.form['rx_gain'])

        try:
            ssn = current_app.config['SSN_DATA'][str(sys_year)]['{:d}'.format(sys_month)]
        except:
            raise ValidationError("Error retreiving SSN data for year/month.")

        if request.form['sys_traffic'] == 'cw':
            traffic = {'bw':1000, 'snr':0}
        else:
            traffic = {'bw':3000, 'snr':13}
        input_file = NamedTemporaryFile(mode='w+t', prefix="proppy_", suffix='.in', delete=False)
        input_file.write('PathName "Proppy Plot"\n')
        input_file.write('PathTXName "{:s}"\n'.format(tx_name))
        input_file.write('Path.L_tx.lat {:.2f}\n'.format(tx_lat))
        input_file.write('Path.L_tx.lng {:.2f}\n'.format(tx_lon))
        input_file.write('TXAntFilePath "ISOTROPIC"\n')
        input_file.write('TXGOS {:.2f}\n'.format(tx_gain))

        input_file.write('PathRXName "{:s}"\n'.format(rx_name))
        #The following values are not actually required.
        #input_file.write('Path.L_rx.lat {:.2f}\n'.format(rx_lat))
        #input_file.write('Path.L_rx.lon {:.2f}\n'.format(rx_lon))
        input_file.write('RXAntFilePath "ISOTROPIC"\n')
        input_file.write('RXGOS {:.2f}\n'.format(rx_gain))

        input_file.write('AntennaOrientation "TX2RX"\n')
        input_file.write('Path.year {:d}\n'.format(sys_year))
        input_file.write('Path.month  {:d}\n'.format(sys_month))
        input_file.write('Path.hour 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\n')
        input_file.write('Path.SSN {:.2f}\n'.format(float(ssn)))
        input_file.write('Path.frequency 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30\n')
        input_file.write('Path.txpower {:.2f}\n'.format(sys_pwr))
        input_file.write('Path.BW {:.1f}\n'.format(traffic['bw']))
        input_file.write('Path.SNRr {:.1f}\n'.format(traffic['snr']))
        input_file.write('Path.Relr 90\n')
        input_file.write('Path.ManMadeNoise "RURAL"\n')
        input_file.write('Path.Modulation "ANALOG"\n')
        input_file.write('Path.SorL "SHORTPATH"\n')
        input_file.write('RptFileFormat "RPT_OPMUF | RPT_{:s}"\n'.format(sys_plot_type))
        input_file.write('LL.lat {:.2f}\n'.format(rx_lat))
        input_file.write('LL.lng {:.2f}\n'.format(rx_lon))
        input_file.write('LR.lat {:.2f}\n'.format(rx_lat))
        input_file.write('LR.lng {:.2f}\n'.format(rx_lon))
        input_file.write('UL.lat {:.2f}\n'.format(rx_lat))
        input_file.write('UL.lng {:.2f}\n'.format(rx_lon))
        input_file.write('UR.lat {:.2f}\n'.format(rx_lat))
        input_file.write('UR.lng {:.2f}\n'.format(rx_lon))
        input_file.write('DataFilePath "{:s}"\n'.format(current_app.config['ITURHFPROP_DATA_PATH']))
        input_file.close()

        FNULL = open(os.devnull, 'w')
        output_file = NamedTemporaryFile(prefix="proppy_", suffix='.out', delete=True)
        subprocess.call(["wine",
            current_app.config['ITURHFPROP_APPLICATION_PATH'],
            input_file.name,
            output_file.name],
            stdout=FNULL,
            stderr=subprocess.STDOUT)
        #print(input_file.name)
        #print(output_file.name)
        prediction = REC533Out(output_file.name)
        muf, mesh_grid, params = prediction.get_p2p_plot_data(sys_plot_type)
        #print(params.title)
        mesh_grid = np.flipud(np.rot90(mesh_grid))

        m = {'x':list(range(0,25)),
            'y':list(muf),
            'name':'MUF',
            'mode':'lines',
            'max':30,
            'line':{'width':4,'color':'rgb(77, 0, 204)'},
            'type':'scatter'}

        #print(mesh_grid)
        if sys_plot_type == 'BCR':
            zmax = 100
            zmin = 0
            rel_cb_dict = {'tickvals' : [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                        'title' : 'Reliability (%)',
                        'ticksuffix' : '%'}
        elif sys_plot_type == 'E':
            zmax = 60
            zmin = -40
            rel_cb_dict = {'tickvals' : [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60],
                        'title': 'Signal Strength dB(1uV/m)'}

        elif sys_plot_type == 'SNR':
            zmax = 50
            zmin = -30
            rel_cb_dict = {'tickvals' : [-30, -20, -10, 0, 10, 20, 30, 40, 50],
                        'title': 'SNR (dB)'}

        p = {'z':mesh_grid.tolist(),
            'x':list(range(0,25)),
            'y':list(range(2,31)),
            'type':'contour',
            'colorscale': 'Jet',
            'autocolorscale': False,
            'zmax':zmax,
            'zmin':zmin,
            'colorbar': rel_cb_dict
        }
        #print(p)
        response = {'m':m, 'p':p}
        os.remove(input_file.name)
        return jsonify(**response)
    """
    print('Failed to validate p2p form;')
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)
    """
    error_msg = ""
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            error_msg += "["+fieldName+"] "+err
    raise ValidationError("Validation Error: "+error_msg)


@ajax.route('/areapredict', methods=['POST'])
def areapredict():
    #print(request.form)
    form = AreaForm(request.form)
    if request.method == 'POST' and form.validate():
        sys_pwr = 10 * log10(float(request.form['sys_pwr'])/1000.0)
        sys_year = int(request.form['year'])
        sys_month = int(request.form['month'])
        sys_plot_type = request.form['sys_plot_type']
        sys_hour = int(request.form['hour'])
        if sys_hour == 0:
            sys_hour = 24
        sys_freq = float(request.form['sys_freq'])

        tx_name = request.form['tx_name'].strip()
        tx_lat = float(request.form['tx_lat_field'])
        tx_lon = float(request.form['tx_lng_field'])
        tx_gain = float(request.form['tx_gain'])

        ssn = current_app.config['SSN_DATA'][str(sys_year)]['{:d}'.format(sys_month)]

        if request.form['sys_traffic'] == 'cw':
            traffic = {'bw':1000, 'snr':0}
        else:
            traffic = {'bw':3000, 'snr':13}

        input_file = NamedTemporaryFile(mode='w+t', prefix="proppy_", suffix='.in', delete=False)
        input_file.write('PathName "Proppy Plot"\n')
        input_file.write('PathTXName "{:s}"\n'.format(tx_name))
        input_file.write('Path.L_tx.lat {:.2f}\n'.format(tx_lat))
        input_file.write('Path.L_tx.lng {:.2f}\n'.format(tx_lon))
        input_file.write('TXAntFilePath "ISOTROPIC"\n')
        input_file.write('TXGOS {:.2f}\n'.format(tx_gain))

        input_file.write('PathRXName "World"\n')
        input_file.write('RXAntFilePath "ISOTROPIC"\n')
        input_file.write('RXGOS {:.2f}\n'.format(2.12))

        input_file.write('AntennaOrientation "TX2RX"\n')
        input_file.write('Path.year {:d}\n'.format(sys_year))
        input_file.write('Path.month  {:d}\n'.format(sys_month))
        input_file.write('Path.hour {:d}\n'.format(sys_hour))
        input_file.write('Path.SSN {:.2f}\n'.format(float(ssn)))
        input_file.write('Path.frequency {:.2f}\n'.format(sys_freq))
        input_file.write('Path.txpower {:.2f}\n'.format(sys_pwr))
        input_file.write('Path.BW {:.1f}\n'.format(traffic['bw']))
        input_file.write('Path.SNRr {:.1f}\n'.format(traffic['snr']))
        input_file.write('Path.Relr 90\n')
        input_file.write('Path.ManMadeNoise "RURAL"\n')
        input_file.write('Path.Modulation "ANALOG"\n')
        input_file.write('Path.SorL "SHORTPATH"\n')
        input_file.write('RptFileFormat "RPT_RXLOCATION | RPT_{:s}"\n'.format(sys_plot_type))
        input_file.write('LL.lat -90.0\n')
        input_file.write('LL.lng -180.0\n')
        input_file.write('LR.lat -90.0\n')
        input_file.write('LR.lng 180.0\n')
        input_file.write('UL.lat 90.0\n')
        input_file.write('UL.lng -180.0\n')
        input_file.write('UR.lat 90.0\n')
        input_file.write('UR.lng 180.0\n')
        input_file.write('latinc  10.0\n')
        input_file.write('lnginc  10.0\n')

        input_file.write('DataFilePath "{:s}"\n'.format(current_app.config['ITURHFPROP_DATA_PATH']))
        input_file.close()
        #print(input_file.name)

        FNULL = open(os.devnull, 'w')
        output_file = NamedTemporaryFile(prefix="proppy_", suffix='.out', delete=False)
        return_code = subprocess.call(["wine",
            current_app.config['ITURHFPROP_APPLICATION_PATH'],
            input_file.name,
            output_file.name],
            stdout=FNULL,
            stderr=subprocess.STDOUT)
        if return_code != 15:
            raise ITURHFPropError("Internal Server Error: Return Code {:d}".format(return_code))
        pap = PropAreaPlot(output_file.name)
        png_file = NamedTemporaryFile(mode='w+t', prefix="proppy_", suffix=".png", dir=current_app.config['AREA_PLOT_DIR_PATH'], delete=False)
        png_file_base = os.path.splitext(png_file.name)[0]
        #print(png_file_base)

        pap.plot_datasets([0], sys_plot_type, plot_nightshade=True, out_file=os.path.splitext(png_file.name)[0])
        #print(input_file.name)
        #os.remove(input_file.name)
        #print(output_file.name)
        #os.remove(output_file.name)
        img_url = url_for('static', filename='img/area/'+os.path.basename(png_file.name))
        response = {'img_url':img_url}
        return jsonify(**response)
    """
    print('Failed to validate area form;')
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)
    """
    error_msg = ""
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            error_msg += "["+fieldName+"] "+err
    raise ValidationError("Validation Error: "+error_msg)


@ajax.route('/areapredicttest', methods=['POST'])
def areapredicttest():
    #print(request.form)
    sys_pwr = 10 * log10(float(request.form['sys_pwr'])/1000.0)
    sys_year = int(request.form['year'])
    sys_month = int(request.form['month'])
    sys_plot_type = request.form['sys_plot_type']
    sys_hour = int(request.form['hour'])
    if sys_hour == 0:
        sys_hour = 24
    sys_freq = float(request.form['sys_freq'])

    tx_name = request.form['tx_name'].strip()
    tx_lat = float(request.form['tx_lat'])
    tx_lon = float(request.form['tx_lon'])
    tx_gain = float(request.form['tx_gain'])

    ssn = current_app.config['SSN_DATA'][str(sys_year)]['{:d}'.format(sys_month)]

    if request.form['sys_traffic'] == 'cw':
        traffic = {'bw':1000, 'snr':0}
    else:
        traffic = {'bw':3000, 'snr':13}

    input_file = NamedTemporaryFile(mode='w+t', prefix="proppy_", suffix='.in', delete=False)
    input_file.write('PathName "Proppy Plot"\n')
    input_file.write('PathTXName "{:s}"\n'.format(tx_name))
    input_file.write('Path.L_tx.lat {:.2f}\n'.format(tx_lat))
    input_file.write('Path.L_tx.lng {:.2f}\n'.format(tx_lon))
    input_file.write('TXAntFilePath "ISOTROPIC"\n')
    input_file.write('TXGOS {:.2f}\n'.format(tx_gain))

    input_file.write('PathRXName "World"\n')
    input_file.write('RXAntFilePath "ISOTROPIC"\n')
    input_file.write('RXGOS {:.2f}\n'.format(2.12))

    input_file.write('AntennaOrientation "TX2RX"\n')
    input_file.write('Path.year {:d}\n'.format(sys_year))
    input_file.write('Path.month  {:d}\n'.format(sys_month))
    input_file.write('Path.hour {:d}\n'.format(sys_hour))
    input_file.write('Path.SSN {:.2f}\n'.format(float(ssn)))
    input_file.write('Path.frequency {:.2f}\n'.format(sys_freq))
    input_file.write('Path.txpower {:.2f}\n'.format(sys_pwr))
    input_file.write('Path.BW {:.1f}\n'.format(traffic['bw']))
    input_file.write('Path.SNRr {:.1f}\n'.format(traffic['snr']))
    input_file.write('Path.Relr 90\n')
    input_file.write('Path.ManMadeNoise "RURAL"\n')
    input_file.write('Path.Modulation "ANALOG"\n')
    input_file.write('Path.SorL "SHORTPATH"\n')
    input_file.write('RptFileFormat "RPT_RXLOCATION | RPT_{:s}"\n'.format(sys_plot_type))
    input_file.write('LL.lat -90.0\n')
    input_file.write('LL.lng -180.0\n')
    input_file.write('LR.lat -90.0\n')
    input_file.write('LR.lng 180.0\n')
    input_file.write('UL.lat 90.0\n')
    input_file.write('UL.lng -180.0\n')
    input_file.write('UR.lat 90.0\n')
    input_file.write('UR.lng 180.0\n')
    input_file.write('latinc  10.0\n')
    input_file.write('lnginc  10.0\n')

    input_file.write('DataFilePath "{:s}"\n'.format(current_app.config['ITURHFPROP_DATA_PATH']))
    input_file.close()
    #print(input_file.name)

    FNULL = open(os.devnull, 'w')
    output_file = NamedTemporaryFile(prefix="proppy_", suffix='.out', delete=False)
    subprocess.call(["wine",
        current_app.config['ITURHFPROP_APPLICATION_PATH'],
        input_file.name,
        output_file.name],
        stdout=FNULL,
        stderr=subprocess.STDOUT)
    prediction = REC533Out(output_file.name)
    mesh_grid, plot_type, lons, lats, num_pts_lon, num_pts_lat, pp, (plot_dt, ssn, freq) = prediction.get_plot_data(0, sys_plot_type)
    #print(params.title)
    #mesh_grid = np.flipud(np.rot90(mesh_grid))

    p = {'z':mesh_grid.tolist(),
        'x':lons.tolist(),
        'y':lats.tolist(),
        'type':'contour',
        'colorscale': 'Jet',
        'autocolorscale': False
    }
    print(p)
    response = {'p':p}
    os.remove(input_file.name)
    return jsonify(**response)


@ajax.errorhandler(ValidationError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@ajax.errorhandler(ITURHFPropError)
def handle_iturhfprop_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
