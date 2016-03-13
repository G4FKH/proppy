import numpy as np
import os
import subprocess

from math import log10
from flask import request, current_app, jsonify
from tempfile import NamedTemporaryFile

from proppy.rec533Out import REC533Out

from . import ajax

@ajax.route('/predict', methods=['POST'])
def predict():
    #fault_id = request.form['fault_id'].strip()
    print(request.form)
    tx_name = request.form['tx_name'].strip()
    tx_lat = float(request.form['tx_lat'])
    tx_lon = float(request.form['tx_lon'])
    tx_pwr = 10 * log10(float(request.form['tx_pwr'])/1000.0)

    rx_name = request.form['rx_name'].strip()
    rx_lat = float(request.form['rx_lat'])
    rx_lon = float(request.form['rx_lon'])

    input_file = NamedTemporaryFile(mode='w+t', prefix="proppy_", suffix='.in', delete=False)
    input_file.write('PathName "Proppy Plot"\n')
    input_file.write('PathTXName "{:s}"\n'.format(tx_name))
    input_file.write('Path.L_tx.lat {:.2f}\n'.format(tx_lat))
    input_file.write('Path.L_tx.lng {:.2f}\n'.format(tx_lon))
    input_file.write('TXAntFilePath "ISOTROPIC"\n')
    input_file.write('TXGOS 2.16\n')

    input_file.write('PathRXName "{:s}"\n'.format(rx_name))
    input_file.write('Path.L_rx.lat {:.2f}\n'.format(rx_lat))
    input_file.write('Path.L_rx.lon {:.2f}\n'.format(rx_lon))
    input_file.write('RXAntFilePath "ISOTROPIC"\n')
    input_file.write('RXGOS 2.16\n')

    input_file.write('AntennaOrientation "TX2RX"\n')
    input_file.write('Path.year {:d}\n'.format(2016))
    input_file.write('Path.month  {:d}\n'.format(3))
    input_file.write('Path.hour 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\n')
    input_file.write('Path.SSN {:d}\n'.format(42))
    input_file.write('Path.frequency 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30\n')
    input_file.write('Path.txpower {:.2f}\n'.format(tx_pwr))
    input_file.write('Path.BW 3000.0\n')
    input_file.write('Path.SNRr 18.0\n')
    input_file.write('Path.Relr 90\n')
    input_file.write('Path.ManMadeNoise "RURAL"\n')
    input_file.write('Path.Modulation "ANALOG"\n')
    input_file.write('Path.SorL "SHORTPATH"\n')
    input_file.write('RptFileFormat "RPT_BCR | RPT_OPMUF"\n')
    input_file.write('LL.lat {:.2f}\n'.format(min(tx_lat, rx_lat)))
    input_file.write('LL.lng {:.2f}\n'.format(min(tx_lon, rx_lon)))
    input_file.write('LR.lat {:.2f}\n'.format(min(tx_lat, rx_lat)))
    input_file.write('LR.lng {:.2f}\n'.format(max(tx_lon, rx_lon)))
    input_file.write('UL.lat {:.2f}\n'.format(max(tx_lat, rx_lat)))
    input_file.write('UL.lng {:.2f}\n'.format(min(tx_lon, rx_lon)))
    input_file.write('UR.lat {:.2f}\n'.format(max(tx_lat, rx_lat)))
    input_file.write('UR.lng {:.2f}\n'.format(max(tx_lon, rx_lon)))
    #todo read from options
    input_file.write('DataFilePath "{:s}"\n'.format(current_app.config['ITURHFPROP_DATA_PATH']))
    input_file.close()


    FNULL = open(os.devnull, 'w')
    output_file = NamedTemporaryFile(prefix="proppy_", suffix='.out')
    subprocess.call(["wine",
        current_app.config['ITURHFPROP_APPLICATION_PATH'],
        input_file.name,
        output_file.name],
        stdout=FNULL,
        stderr=subprocess.STDOUT)
    print(output_file.name)
    prediction = REC533Out(output_file.name)
    muf, mesh_grid, params = prediction.get_p2p_plot_data('REL')
    mesh_grid = np.flipud(np.rot90(mesh_grid))

    m = {'x':list(range(0,25)),
        'y':list(muf),
        'name':'MUF',
        'mode':'lines',
        'max':30,
        'line':{'width':4,'color':'rgb(77, 0, 204)'},
        'type':'scatter'}

    print(mesh_grid)
    p = {'z':mesh_grid.tolist(),
        'x':list(range(0,25)),
        'y':list(range(2,31)),
        'type':'contour',
        'colorscale': 'Jet', 
        'autocolorscale': False,
        'zmax':100,
        'zmin':0,
        'colorbar':{'ticksuffix':'%',
                'title':'Reliability',
                'tickmode':'array',
                'tickvals':[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            }
        }

    response = {'m':m, 'p':p}
    return jsonify(**response)
