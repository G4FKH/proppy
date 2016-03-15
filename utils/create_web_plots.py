#! /usr/bin/env python

from datetime import datetime, timedelta
import json
import glob
import os
import subprocess # for testing only - remove on production system

from propplot.propAreaPlot import PropAreaPlot

'''
Short script to automate the plotting of RSGB files.

'''

'''
Define the location of the ITURHFProp.exe executable.
'''
bin_path = "/opt/rec533/Bin/ITURHFProp.exe"

'''
Location of the working directory (where the .in and .out files will be stored)
'''
working_dir = "/home/proppy/tmp/"
'''
Define the location of the directory to write the plots to.
The string must end with the '/' character.
'''
out_dir = "/var/www/html/img/prediction/"
'''
List of the frequencies to plot.
'''
freq_list = [3.525, 5.528, 7.025, 10.110, 14.025, 18.080, 21.025, 24.895, 28.025]

'''
Location of the file containing the json formatted ssn data.
'''
ssn_path = "/opt/rec533/ssn.json"

with open(ssn_path) as data_file:
    ssn_data = json.load(data_file)

current_dt = datetime.utcnow() + timedelta(hours=1)
current_month = current_dt.month
current_year = current_dt.year
current_ssn = ssn_data[current_dt.strftime("%Y")][current_dt.strftime("%m")]

for current_hour in range(1,25):
    for idx, freq in enumerate(freq_list):
        with open(working_dir+"web_plots.in", "w") as r533_in_file:
            r533_in_file.write('PathName "Mid U.K. - Area Coverage"\n')
            r533_in_file.write('PathTXName "G4FKH"\n')
            r533_in_file.write('Path.L_tx.lat   54.50\n')
            r533_in_file.write('Path.L_tx.lng   -2.00\n')
            r533_in_file.write('TXAntFilePath "ISOTROPIC"\n')
            r533_in_file.write('TXGOS 2.16\n')
            r533_in_file.write('PathRXName "World"\n')
            r533_in_file.write('RXAntFilePath "ISOTROPIC"\n')
            r533_in_file.write('RXGOS 2.16\n')
            r533_in_file.write('AntennaOrientation "TX2RX"\n')
            r533_in_file.write('Path.year {:d}\n'.format(current_year))
            r533_in_file.write('Path.month  {:d}\n'.format(current_month))
            r533_in_file.write('Path.hour {:d}\n'.format(current_hour))
            r533_in_file.write('Path.SSN {:d}\n'.format(current_ssn))
            r533_in_file.write('Path.frequency {:.2f}\n'.format(freq))
            r533_in_file.write('Path.txpower -10.0\n')
            r533_in_file.write('Path.BW 2800.0\n')
            r533_in_file.write('Path.SNRr 18.0\n')
            r533_in_file.write('Path.Relr 90\n')
            r533_in_file.write('Path.ManMadeNoise "RURAL"\n')
            r533_in_file.write('Path.Modulation "ANALOG"\n')
            r533_in_file.write('Path.SorL "SHORTPATH"\n')
            r533_in_file.write('RptFileFormat "RPT_RXLOCATION | RPT_SNR | RPT_BCR | RPT_E | RPT_OPMUFD"\n')
            r533_in_file.write('LL.lat    -90.0\n')
            r533_in_file.write('LL.lng   -180.0\n')
            r533_in_file.write('LR.lat    -90.0\n')
            r533_in_file.write('LR.lng    180.0\n')
            r533_in_file.write('UL.lat     90.0\n')
            r533_in_file.write('UL.lng   -180.0\n')
            r533_in_file.write('UR.lat     90.0\n')
            r533_in_file.write('UR.lng    180.0\n')
            r533_in_file.write('latinc  2.0\n')
            r533_in_file.write('lnginc  2.0\n')
            r533_in_file.write('DataFilePath "/opt/rec533/Data/"\n')

        # The following is just a mock-up until a Linux compatible binary
        # becomes available.
        #FNULL = open(os.devnull, 'w')
        subprocess.call(["wine", bin_path, working_dir+"web_plots.in", working_dir+"web_plots.out"])
        pap = PropAreaPlot(working_dir+"web_plots.out")
        if current_hour == 24:
            hour_dir = out_dir + str(0) + os.sep
        else:
            hour_dir = out_dir + str(current_hour) + os.sep
        pap.plot_datasets([0], 'REL', plot_nightshade=True, pre_filter='LFFilter', cmap='g4fkh', out_dir=hour_dir, out_file="rel_{:d}".format(idx+1))
        pap.plot_datasets([0], 'SNR', plot_nightshade=True, vmin=0, vmax=100, pre_filter='LFFilter', cmap='g4fkh', out_dir=hour_dir, out_file="snr_{:d}".format(idx+1))
        pap.plot_datasets([0], 'E', plot_nightshade=True, cmap='g4fkh', out_dir=hour_dir, out_file="e_{:d}".format(idx+1))
    subprocess.call(["mogrify", "-format", "jpg", hour_dir+"*.png"])
    png_files = glob.glob(hour_dir+"*.png")
    for png_file in png_files:
        os.remove(png_file)
