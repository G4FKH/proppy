#! /usr/bin/env python
#
# File: rec533Out.py
#
# Copyright (c) 2015 J.Watson (jimwatson@mac.com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import csv
import datetime
import itertools
import math
import re
import sys

import numpy as np

sys.path.insert(1, '/usr/local/lib/python3.4/site-packages')
from pythonprop.voaAreaRect import VOAAreaRect

from proppy.predictionParams import PredictionParams

class REC533Out:
    '''
    A small class to encapsulate files produced by the ITURHFProp
    application.  These file may contain a number of sets of plot data.
    These may be accessed directly or via an iterator.

    Plots sets for different values of hour and frequency may be contained
    in a single REC533 Out file.

    Each entry starts with the month, hour, frequency.  User defined values
    follow.
    '''

    filename = ""

    def __init__(self, filename):
        self.filename = filename
        self.prediction_type = '' # 'AREA' or 'P2P'
        self.pp, self.ssn, self.data_format_dict = self.parse_global_params()
        if self.prediction_type == 'AREA':
            self.datasets = self.build_dataset_list()
        self.itr_ctr = -1


    def consume(self, iterator, n):
        "Advance the iterator n-steps ahead. If n is none, consume entirely."
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            collections.deque(iterator, maxlen=0)
        else:
            # advance to the empty slice starting at position n
            next(itertools.islice(iterator, n, n), None)


    def parse_global_params(self):
        '''
        The method used to extract the file data is a little long winded and
        not very efficient but we're not sure how the file format will change
        over time or with different input files.
        '''
        pp = PredictionParams()

        data_format_dict = {'MONTH':0, 'HOUR':1, 'FREQ':2}
        title = ""
        input_param_start_pattern = re.compile("\** P533 Input Parameters")

        year_pattern = re.compile("^\s*Year = ([\d]+)")
        ssn_pattern = re.compile("^\s*SSN \(R12\) = ([\d.]+)")
        tx_pwr_pattern = re.compile("^\s*Tx power = ([-\d.]+)")
        tx_ant_type_pattern = re.compile("^\s*Transmit antenna ([\w]+)\s*$")
        tx_ant_gain_pattern = re.compile("^\s*Transmit antenna gain offset = ([-\d.]+)")

        ul_lat_pattern = re.compile("^\s*Upper left latitude   =\s*([\d.]+) ([NS])")
        ul_lon_pattern = re.compile("^\s*Upper left longitude  =\s*([\d.]+) ([WE])")
        lr_lat_pattern = re.compile("^\s*Lower right latitude  =\s*([\d.]+) ([NS])")
        lr_lon_pattern = re.compile("^\s*Lower right longitude =\s*([\d.]+) ([WE])")

        lat_inc_pattern = re.compile("^\s*Latitude increment\s*= ([\d.]+) \(deg\)")
        lon_inc_pattern = re.compile("^\s*Longitude increment\s*= ([\d.]+) \(deg\)")

        col_bcr_pattern = re.compile("Column (\d+): B[SC]R - Basic circuit reliability")
        col_e_pattern = re.compile("Column (\d+): E - Path Field Strength \(dB\(1uV/m\)\)")
        col_rx_location_lat_pattern = re.compile("Column (\d+): Receiver latitude \(deg\)")
        col_rx_location_lon_pattern = re.compile("Column (\d+): Receiver longitude \(deg\)")
        col_snr_pattern = re.compile("Column (\d+): SNR - Median signal-to-noise ratio")
        col_opmuf_pattern = re.compile("Column (\d+): OPMUF - Operation MUF \(MHz\)")
        col_opmuf10_pattern = re.compile("Column (\d+): OPMUF10 - 10% Operation MUF \(MHz\)")

        title_line_ptr = False
        with open(self.filename) as f:
            for line in f:
                m = input_param_start_pattern.match(line)
                if m:
                    self.consume(f,1)
                    title_line_ptr = True
                    continue
                if title_line_ptr:
                    pp.title = line.strip()
                    title_line_ptr = False
                    continue

                m = tx_pwr_pattern.match(line)
                if m:
                    p = float(m.group(1))
                    pp.tx_pwr = 1000 * math.pow(10.0, p/10.0)
                    continue
                m = tx_ant_type_pattern.match(line)
                if m:
                    pp.tx_ant_type = m.group(1)
                    continue
                m = tx_ant_gain_pattern.match(line)
                if m:
                    pp.tx_ant_gain = float(m.group(1))
                    continue
                m = year_pattern.match(line)
                if m:
                    pp.year = int(m.group(1))
                    continue
                m = ssn_pattern.match(line)
                if m:
                    ssn = float(m.group(1))
                    continue
                m = ul_lat_pattern.match(line)
                if m:
                    ul_lat = float(m.group(1))
                    if m.group(2) == 'S':
                        ul_lat = -ul_lat
                    continue
                m = ul_lon_pattern.match(line)
                if m:
                    ul_lon = float(m.group(1))
                    if m.group(2) == 'W':
                        ul_lon = -ul_lon
                    continue
                m = lr_lat_pattern.match(line)
                if m:
                    lr_lat = float(m.group(1))
                    if m.group(2) == 'S':
                        lr_lat = -lr_lat
                    continue
                m = lr_lon_pattern.match(line)
                if m:
                    lr_lon = float(m.group(1))
                    if m.group(2) == 'W':
                        lr_lon = -lr_lon
                    continue

                m = lat_inc_pattern.match(line)
                if m:
                    pp.lat_step_size = float(m.group(1))
                    continue
                m = lon_inc_pattern.match(line)
                if m:
                    pp.lon_step_size = float(m.group(1))
                    continue
                m = col_bcr_pattern.match(line)
                if m:
                    data_format_dict['REL'] = int(m.group(1)) - 1
                    continue
                m = col_e_pattern.match(line)
                if m:
                    data_format_dict['E'] = int(m.group(1)) - 1
                    continue
                m = col_rx_location_lat_pattern.match(line)
                if m:
                    data_format_dict['RX_LAT'] = int(m.group(1)) - 1
                    continue
                m = col_rx_location_lon_pattern.match(line)
                if m:
                    data_format_dict['RX_LON'] = int(m.group(1)) - 1
                    continue
                m = col_snr_pattern.match(line)
                if m:
                    data_format_dict['SNR'] = int(m.group(1)) - 1
                    continue
                m = col_opmuf10_pattern.match(line)
                if m:
                    data_format_dict['OPMUF10'] = int(m.group(1)) - 1
                    continue
                m = col_opmuf_pattern.match(line)
                if m:
                    data_format_dict['OPMUF'] = int(m.group(1)) - 1
                    continue
                if '*** Calculated Parameters ***' in line:
                    break
        #print (data_format_dict)
        if (lr_lat == ul_lat) and (ul_lon == lr_lon):
            self.prediction_type = 'P2P'
        else:
            self.prediction_type = 'AREA'
        extent = VOAAreaRect(sw_lat=lr_lat, sw_lon=ul_lon, ne_lat=ul_lat, ne_lon=lr_lon)
        #print(extent.get_formatted_string())
        pp.plot_rect = extent
        return (pp, ssn, data_format_dict)


    def get_datasets(self):
        return [(plot_dt, self.pp.title, freq) for plot_dt, freq, idx in self.datasets]

    def build_dataset_list(self):
        datasets = []
        # The year information is not included in the out file
        month = ''
        hour = ''
        freq = ''
        idx = 0
        calculated_parameters_section = False
        with open(self.filename) as f:
            for line in f:
                if "**** Calculated Parameters ****" in line:
                    calculated_parameters_section = True
                elif calculated_parameters_section:
                    params = line.split(',')
                    if len(params) > 3:
                        if (month != params[0]) or (hour != params[1]) or (freq != params[2]):
                            month = params[0]
                            hour = params[1]
                            freq =params[2]
                            h = int(hour) if (int(hour) < 24) else int(hour) % 24
                            # todo use datetime.MINYEAR when we move to P3
                            plot_dt = datetime.datetime(self.pp.year, int(month), 15, hour=h)
                            datasets.append((plot_dt, freq.strip(), idx))
                            #print (month, hour, freq, idx)
                idx += len(line)+1
        return datasets


    def __iter__(self):
        return self


    def __next__(self):
        self.itr_ctr += 1
        if self.itr_ctr < (len(self.datasets)):
            return self.get_plot_data(self.datasets[self.itr_ctr])
        else:
            raise StopIteration


    def get_p2p_plot_data(self, plot_type):
        muf_dict = {}
        OPMUF = np.zeros(25, float)
        mg = np.zeros([25, 29], float) # meshgrid (0-24) hours x num_freqs (2-30)
        try:
            data_column = self.data_format_dict[plot_type]
            muf_column = self.data_format_dict['OPMUF']
        except KeyError:
            print("Error: Specified data set {:s} not found in file {:s}".format(plot_type, self.filename))
            raise LookupError
        f = open(self.filename, 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 3:
                    # todo remove hard coded values below
                    OPMUF[int(row[1])] = float(row[3])
                    #todo do a check that our array indexes are not out of range
                    # [hours][freq]
                    mg[int(float(row[1]))][int(float(row[2]))-2] = float(row[data_column])
        finally:
            f.close()
        # rec533 hours are in the range 1-24, copy 24 -> 0
        OPMUF[0] = OPMUF[24]
        mg[0,:] = mg[24,:]
        return (OPMUF, mg, self.pp)

    def get_plot_data(self, dataset_id, plot_type):
        '''
        plot_type REL or SNR
        '''
        try:
            data_column = self.data_format_dict[plot_type]
        except KeyError:
            print("Error: Specified data set {:s} not found in file {:s}".format(plot_type, self.filename))
            raise LookupError
        plot_dt, freq, idx = self.datasets[dataset_id]
        num_pts_lat = ((self.pp.plot_rect.get_ne_lat() - self.pp.plot_rect.get_sw_lat()) / self.pp.lat_step_size) + 1
        num_pts_lon = ((self.pp.plot_rect.get_ne_lon() - self.pp.plot_rect.get_sw_lon()) / self.pp.lon_step_size) + 1
        points = np.zeros([num_pts_lat, num_pts_lon], float)

        lons = np.arange(self.pp.plot_rect.get_sw_lon(),
                    self.pp.plot_rect.get_ne_lon()+1,
                    self.pp.lon_step_size)
        lats = np.arange(self.pp.plot_rect.get_sw_lat(),
                    self.pp.plot_rect.get_ne_lat()+1,
                    self.pp.lat_step_size)
        f = open(self.filename, 'rt')
        freq=freq.strip()
        if plot_dt.hour == 0:
            formatted_hour_str = '24'
        else:
            formatted_hour_str = '{0:02d}'.format(plot_dt.hour)
        try:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 3:
                    #print("looking in +", row[1].strip(), "+ for +", formatted_hour_str, ": looking in +", row[2].strip(), "+ for +", freq,"+")
                    if row[1].strip()==formatted_hour_str and row[2].strip()==freq:
                        #print (row)
                        lat_grid_pos = (int(float(row[3])-self.pp.plot_rect.get_sw_lat()) / self.pp.lat_step_size)
                        lon_grid_pos = (int(float(row[4])-self.pp.plot_rect.get_sw_lon()) / self.pp.lon_step_size)
                        points[lat_grid_pos][lon_grid_pos] = float(row[data_column])
        finally:
            f.close()
        plot_dt, freq, idx = self.datasets[dataset_id]
        return (points, plot_type, lons, lats, num_pts_lon, num_pts_lat, self.pp, (plot_dt, self.ssn, freq))
