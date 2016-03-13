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
#sys.path.insert(1, '/usr/local/lib/python3.4/site-packages')
from pythonprop.voaAreaRect import VOAAreaRect

class PredictionParams:

    def __init__(self):
        self.plot_rect = VOAAreaRect()
        self.lat_step_size = 0
        self.lon_step_size = 0
        self.title = ''
        self.tx_pwr = 0.0
        self.tx_ant_type = ''
        self.tx_ant_gain = 0.0
        self.year = 1900
