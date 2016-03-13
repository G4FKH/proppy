import numpy as np
import subprocess
from tempfile import NamedTemporaryFile
import os
#import os.path
from flask import request, current_app, jsonify
#from werkzeug import secure_filename

from proppy.rec533Out import REC533Out

from . import ajax

@ajax.route('/predict', methods=['POST'])
def predict():
    FNULL = open(os.devnull, 'w')
    output_file = NamedTemporaryFile(prefix="proppy_")
    subprocess.call(["wine",
        current_app.config['ITURHFPROP_APPLICATION_PATH'],
        "/home/jwatson/github/proppy/bin/test.in",
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
        'type':'scatter'}

    p = {'z':mesh_grid.tolist(),
        'x':list(range(0,25)),
        'y':list(range(2,31)),
        'type':'contour'}

    response = {'m':m, 'p':p}
    return jsonify(**response)
