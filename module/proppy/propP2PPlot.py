#! /usr/bin/env python
#
# File: propP2PPlot.py
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

import datetime
import sys
import imp
import os

import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import ListedColormap, BoundaryNorm

from mpl_toolkits.basemap import Basemap

from rec533Out import REC533Out

from cmap.plotlyAlt import PlotlyAlt

MainModule = "__init__"

class PropP2PPlot:

    IMG_TYPE_DICT  = { \
        'MUF':{'title':('MUF'), 'vmin':2, 'vmax':30, 'y_labels':(2, 5, 10, 15, 20, 25, 30), 'formatter':'frequency_format'}, \
        'REL':{'title':('Reliability'), 'vmin':0, 'vmax':100, 'y_labels':(0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100), 'formatter':'percent_format'}, \
        'SNR':{'title':('SNR'), 'vmin':-10, 'vmax':70, 'y_labels':(-10, 0, 10, 20, 30, 40, 50, 60, 70), 'formatter':'SNR_format' }}

    def __init__(self, data_file):
        self.r533 = REC533Out(data_file)
        self.plot_params = self.IMG_TYPE_DICT['REL']

    def do_polar_bar_plot(self, plot_type, dpi=150, cmap='jet', file_format='png'):
        '''
        A doodle to look at different ways of presenting data.
        '''
        try:
            muf_data, im_data, global_params = self.r533.get_p2p_plot_data(plot_type)
        except LookupError:
            return
        #points, plot_type, lons, lats, num_pts_lon, num_pts_lat, global_params, params = dataset
        #plot_dt, ssn, freq = params
        # EDIT THE LINE BELOW TO MODIFY COLOURS IN THE COLORMAP
        #g4fkh = ListedColormap(['#EFFBFB', '#CCFFFF', '#0080FF', '#99FF99', '#00FF00', '#CCFFCC', '#FFFF00', '#FFCC99', '#FF7800', '#FF0000'])
        plt.clf() #Clear any existing plot data, specifically nightshade
        #plt.register_cmap(name='g4fkh', cmap=g4fkh)

        plt.register_cmap(name='PlotlyAlt', cmap=PlotlyAlt)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')

        palette=plt.get_cmap(cmap)

        rad_hour = (2 * np.pi) / 24.0
        start_theta = (np.pi / 2.0) + rad_hour/2.0
        theta = np.arange(start_theta, (-2.0*np.pi) + (np.pi/2.0) + (rad_hour/2.0), -rad_hour)
        radii = [0.5, 0.8, .6, .3, .2, .4, .8, 1.0 ,0.5, 0.8, .6, .3, .2, .4, .8, 1.0 ,0.5, 0.8, .6, .3, .2, .4, .8, 1.0]
        radii = []
        indexes = []
        for hour in range(0,24):
            idx = np.argmax(im_data[hour,:])
            radii.append(im_data[hour,idx])
            indexes.append(idx)
        bars = ax.bar(theta, radii, width=-rad_hour, bottom=0.0)
        for r, bar, idx in zip(radii, bars, indexes):
            c = palette(int((256/28)*idx))
            bar.set_facecolor(c)
            bar.set_edgecolor(c)
            bar.set_alpha(0.75)


        main_title = "{:s}".format(global_params.title)
        tx_ant_str = "{:s} ({:.1f}dB)".format(global_params.tx_ant_type, global_params.tx_ant_gain)

        #pythonProp subtitle
        #sub_title = "{:s} - {:s} - SSN:{:.1f} - {:.3f}MHz - {:s} - {:.0f}W".format(plot_params['title'], plot_dt.strftime(ds_fmt_str), ssn, float(freq), tx_ant_str, global_params.tx_pwr)
        #RSGB subtitle
        sub_title = "{:s} {:s} {:.0f}W".format(self.plot_params['title'], tx_ant_str, global_params.tx_pwr)

        #plt.figtext(0.5, 0.8, main_title, fontsize=18, ha='center')
        #plt.figtext(0.5, 0.76,sub_title,fontsize=10, fontstyle='normal', ha='center')

        #todo if we're using voacap files we can include the year in the filename
        #plot_fn = "p2p_{:s}_{:s}_{:s}.{:s}".format(plot_type, "d".join(str(freq).split('.')), file_format)
        plot_fn = 'test.svg'
        print ("Saving file ", plot_fn)
        plt.savefig(plot_fn, dpi=float(dpi), bbox_inches='tight')



    def do_plot(self, plot_type, dpi=150, cmap='jet', out_file=None, file_format='png'):

        try:
            muf_data, im_data, global_params = self.r533.get_p2p_plot_data(plot_type)
        except LookupError:
            print(muf_data)
            print(im_data)
            print(global_params)
            return

        #points, plot_type, lons, lats, num_pts_lon, num_pts_lat, global_params, params = dataset
        #plot_dt, ssn, freq = params
        plot_fn = out_file
        # EDIT THE LINE BELOW TO MODIFY COLOURS IN THE COLORMAP
        g4fkh = ListedColormap(['#EFFBFB', '#CCFFFF', '#0080FF', '#99FF99', '#00FF00', '#CCFFCC', '#FFFF00', '#FFCC99', '#FF7800', '#FF0000'])
        plt.clf() #Clear any existing plot data, specifically nightshade
        plt.register_cmap(name='g4fkh', cmap=g4fkh)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_ylim([2, 30])
        ax.set_yticks([2, 5] + list(range(10, 31, 5)))
        ax.set_ylabel('Frequency / MHz')

        ax.set_xlim([0, 24])
        x_ticks = list(range(0, 25, 2))
        ax.set_xticks(x_ticks)
        ax.set_xlabel('Time / UTC')

        ax.plot(range(0, 25), muf_data,'g-', linewidth=3)

        X,Y = np.meshgrid(range(2, 31), range(0, 25))
        im_data = np.clip(im_data, 0, 100)

        palette=plt.get_cmap(cmap)

        ct = ax.contour(Y, X, im_data, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    latlon=True,
                    linewidths=0.5,
                    colors='k',
                    vmin=0,
                    vmax=100 )

        ctf = ax.contourf(Y, X, im_data, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    latlon=True,
                    cmap=palette,
                    vmin=0,
                    max=100)

        main_title = "{:s}".format(global_params.title)
        tx_ant_str = "{:s} ({:.1f}dB)".format(global_params.tx_ant_type, global_params.tx_ant_gain)

        #pythonProp subtitle
        #sub_title = "{:s} - {:s} - SSN:{:.1f} - {:.3f}MHz - {:s} - {:.0f}W".format(plot_params['title'], plot_dt.strftime(ds_fmt_str), ssn, float(freq), tx_ant_str, global_params.tx_pwr)
        #RSGB subtitle
        sub_title = "{:s} {:s} {:.0f}W".format(self.plot_params['title'], tx_ant_str, global_params.tx_pwr)

        #plt.figtext(0.5, 0.8, main_title, fontsize=18, ha='center')
        #plt.figtext(0.5, 0.76,sub_title,fontsize=10, fontstyle='normal', ha='center')

        #todo if we're using voacap files we can include the year in the filename
        if not plot_fn:
            plot_fn = "p2p_{:s}.{:s}".format(plot_type, file_format)
        print ("Saving file ", plot_fn)
        plt.savefig(plot_fn, dpi=float(dpi), bbox_inches='tight')


    def get_datasets(self):
        ''' Returns a list of datasets found in the out file.'''
        return self.r533.get_datasets()


    def dump_datasets(self):
        ''' Dumps a list of datasets to the screen.'''
        ds_list = self.get_datasets()
        print("ID\tUTC Title Frequency")
        for ctr, ds in enumerate(ds_list):
            plot_dt, title, freq = ds
            # Don't display the year if year = datetime.MINYEAR
            print('{: 4d}  {:s}\t{:6.3f}\t{:}'.format(ctr, plot_dt.strftime("%H:%M %b"), float(freq), title))


    def get_metadata(self):
        '''Returns metadata about the file.'''
        return 'Not implemented yet.'

    def dump_metadata(self):
        '''Dumps metadata to the screen'''
        print (self.get_metadata())

    ###############################
    # COLORBAR FORMATTERS
    ###############################

    def percent_format(self, x, pos):
        #return '%(percent)3d%%' % {'percent':x*100}
        return "{:3d}%".format(x)

    def SNR_format(self, x, pos):
        #return '%3ddB' % x
        return "{:3d}dB".format(x)


def main(data_file):
    parser = argparse.ArgumentParser(description="Plot HF Area Predictions.")
    subparsers = parser.add_subparsers()

    query_mode_parser = subparsers.add_parser('query', help="Query mode commands")
    plot_mode_parser = subparsers.add_parser('plot', help="Plot mode commands")

    plot_mode_parser.add_argument("-d", "--datatype",
        dest = "data_opt",
        choices = ['SNR', 'REL'],
        default = 'SNR',
        help = "DATATYPE - a string representation of the data to plot. Valid values are 'SNR' and 'REL'. Default value is 'SNR'." )

    query_mode_parser.add_argument("-l", "--list",
        dest = "list",
        action = "store_true",
        default = False,
        help = "List files and quit." )

    query_mode_parser.add_argument("-a", "--about",
        dest = "about",
        action = "store_true",
        default = False,
        help = "Dump file information to the screen." )

    plot_mode_parser.add_argument('--file-format',
        dest = "file_format",
        default = 'png',
        choices = ['png', 'svg'],
        help="Specify format of the output file."
        )

    plot_mode_parser.add_argument("-m", "--cmap",
        dest = "cmap",
        default = 'jet',
        choices = ['Oranges', 'Blues', 'YlOrRd_r', 'Set3', 'seismic_r',
                'ocean', 'Accent', 'copper_r', 'bone', 'RdGy', 'PuBuGn',
                'Greens', 'BrBG_r', 'Purples_r', 'RdBu_r', 'PuOr_r', 'YlGn',
                'autumn', 'gist_gray', 'nipy_spectral', 'gist_gray_r',
                'terrain', 'YlOrBr_r', 'binary', 'Reds_r', 'spectral_r',
                'RdYlGn', 'summer', 'gist_earth', 'RdYlBu', 'Set1', 'afmhot_r',
                'Pastel1_r', 'YlOrBr', 'gist_stern_r', 'prism_r', 'Greys_r',
                'brg_r', 'spring_r', 'YlGnBu_r', 'terrain_r', 'Oranges_r',
                'hot', 'cubehelix', 'PuOr', 'jet', 'Dark2', 'PRGn_r', 'gray',
                'hot_r', 'pink_r', 'Spectral', 'Reds', 'Wistia', 'YlOrRd',
                'RdGy_r', 'bwr_r', 'brg', 'Paired', 'cool_r', 'gnuplot_r',
                'gist_ncar', 'Dark2_r', 'RdYlBu_r', 'RdBu', 'PRGn', 'flag_r',
                'gist_stern', 'OrRd_r', 'BuGn', 'OrRd', 'Greys', 'BuGn_r',
                'PuBu_r', 'seismic', 'YlGn_r', 'PuRd', 'Pastel2_r', 'bwr',
                'gist_earth_r', 'gist_rainbow', 'gnuplot', 'Greens_r', 'BrBG',
                'nipy_spectral_r', 'binary_r', 'gnuplot2', 'Set2', 'Blues_r',
                'PuBuGn_r', 'Paired_r', 'gist_heat_r', 'coolwarm_r', 'CMRmap',
                'afmhot', 'prism', 'cool', 'jet_r', 'CMRmap_r', 'PuRd_r',
                'coolwarm', 'ocean_r', 'spectral', 'summer_r', 'gnuplot2_r',
                'gist_ncar_r', 'gist_yarg_r', 'gist_heat', 'PiYG_r', 'copper',
                'spring', 'Set1_r', 'Spectral_r', 'Set3_r', 'Set2_r', 'winter',
                'PiYG', 'gray_r', 'flag', 'hsv_r', 'GnBu_r', 'Purples',
                'RdYlGn_r', 'BuPu_r', 'Pastel1', 'RdPu_r', 'GnBu', 'gist_yarg',
                'Wistia_r', 'rainbow', 'autumn_r', 'bone_r', 'cubehelix_r',
                'pink', 'hsv', 'Pastel2', 'RdPu', 'BuPu', 'PuBu', 'Accent_r',
                'rainbow_r', 'YlGnBu', 'gist_rainbow_r', 'winter_r', 'g4fkh',
                'PlotlyAlt'],
        help="Specify the colour map to use.  Default = 'jet'"
        )

    plot_mode_parser.add_argument("-o", "--outfile",
        dest="out_file",
        default=None,
        help="Name of file to save plot to.")

    plot_mode_parser.add_argument("-p", "--plots",
        dest = "plot_files",
        default = '0',
        help = "Plots to print, e.g '-v 1,3,5,6' or use '-v a' to print all plots." )

    plot_mode_parser.add_argument("-r", "--resolution",
        dest = "dpi",
        type = int,
        default = 150,
        help = ("Dots per inch (dpi)."))

    parser.add_argument(dest = "data_file",
        help = "Name of the file containing the prediction data.")

    args = parser.parse_args()

    plot_files = []
    if hasattr(args, 'plot_files'):
        args.plot_files.strip()
        if args.plot_files == 'a':
            plot_files = 'a'
        # todo if not defined
        else:
            try:
                plot_files = hyphen_range(args.plot_files)
            except:
                print ("Error reading plot datasets; resetting to '1'")
                plot_files = [0]

        print ("The following {:d} files have been selected {:s}: ".format(len(plot_files), str(plot_files)))

    pp = PropP2PPlot(args.data_file)
    if hasattr(args, 'list'):
        if args.list:
            pp.dump_datasets()
    if hasattr(args, 'about'):
        if args.about:
            pp.dump_metadata()
    else:
        pp.do_plot(args.data_opt,
            cmap = args.cmap,
            file_format = args.file_format,
            out_file = args.out_file,
            dpi = args.dpi)

def hyphen_range(s):
    """ Takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.
    Also accepts comma separated ranges like "a-b,c-d,f" will build a list which will include
    Numbers from a to b, a to d and f

    The following function was taken from;
    http://code.activestate.com/recipes/577279-generate-list-of-numbers-from-hyphenated-and-comma/
    """
    s="".join(s.split())#removes white space
    r=set()
    for x in s.split(','):
        t=x.split('-')
        if len(t) not in [1,2]: raise SyntaxError("Error parsing",s)
        r.add(int(t[0])) if len(t)==1 else r.update(set(range(int(t[0]),int(t[1])+1)))
    l=list(r)
    l.sort()
    return l


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[-1])
    else:
        print ('propAreaPlot error: No data file specified')
        print ('propAreaPlot [options] filename')
        sys.exit(1)
