#! /usr/bin/env python
#
# File: propAreaPlot.py
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

from propplot.rec533Out import REC533Out

MainModule = "__init__"

class PropAreaPlot:

    IMG_TYPE_DICT  = { \
        'MUF':{'title':('MUF'), 'vmin':2, 'vmax':30, 'step':5, 'formatter':'frequency_format'}, \
        'REL':{'title':('Reliability'), 'vmin':0, 'vmax':100, 'step':10, 'formatter':'percent_format'}, \
        'E':{'title':'S-Meter', 'y_labels':[-14.0, -8.18, -2.16, 3.86, 9.1, 15.92, 21.94, 27.96, 33.98], 'formatter':'smtr_format'}, \
        'SNR':{'title':('SNR'), 'vmin':-10, 'vmax':70, 'step':10,'formatter':'SNR_format' }}

    def __init__(self, data_file):
        self.r533 = REC533Out(data_file)


    def plot_datasets(self, ds_list, data_opt, dpi = 150,
                cmap='jet',
                out_dir = None,
                out_file = None,
                file_format='png',
                vmin = None,
                vmax = None,
                plot_nightshade=False):
        plot_counter = 1
        for dataset_id in ds_list:
            try:
                plot_params = self.IMG_TYPE_DICT[data_opt]
            except KeyError:
                print("Error: Undefined plot type, {:s}".format(data_opt))
                return
            if dataset_id < len(self.r533.datasets):
                try:
                    print("out_file = {:s} ".format(out_file))
                    if out_file and len(ds_list) > 1:
                        fn = "{:s}_{:d}".format(out_file, plot_counter)
                    elif out_file and len(ds_list) == 1:
                        fn = out_file
                    else:
                        fn = None
                    self.do_plot(self.r533.get_plot_data(dataset_id, data_opt),
                        plot_params,
                        cmap = cmap,
                        dpi = dpi,
                        file_format = file_format,
                        out_dir = out_dir,
                        out_file = fn,
                        vmin = vmin,
                        vmax = vmax,
                        plot_nightshade = plot_nightshade)
                    plot_counter += 1
                except LookupError as e:
                    print("Error retrieving data for ID {:d}/{:s}.".format(dataset_id, data_opt))
                    print(e)
            else:
                print ("Invalid index:", dataset_id)

    def do_plot(self, dataset, plot_params, dpi=150,
                cmap='jet',
                out_dir = None,
                out_file = None,
                vmin = None,
                vmax = None,
                plot_nightshade=False,
                file_format='png'):
        points, plot_type, lons, lats, num_pts_lon, num_pts_lat, global_params, params = dataset
        plot_dt, ssn, freq = params
        if not 'y_labels' in plot_params:
            vmin = plot_params['vmin'] if vmin is None else vmin
            vmax = plot_params['vmax'] if vmax is None else vmax
            y_labels = range(vmin, vmax+1, plot_params['step'])
        else:
            y_labels = plot_params['y_labels']
            vmin = y_labels[0] if vmin is None else vmin
            vmax = y_labels[-1] if vmax is None else vmax


        '''
        if vmin is None:
            vmin = plot_params['vmin']
        if vmax is None:
            vmax = plot_params['vmax']
        '''
        # EDIT THE LINE BELOW TO MODIFY COLOURS IN THE COLORMAP
        g4fkh = ListedColormap(['#EFFBFB', '#CCFFFF', '#0080FF', '#99FF99', '#00FF00', '#CCFFCC', '#FFFF00', '#FFCC99', '#FF7800', '#FF0000'])
        plt.clf() #Clear any existing plot data, specifically nightshade
        plt.register_cmap(name='g4fkh', cmap=g4fkh)
		# resolution can be c crude l low
        m = Basemap(projection='cyl', resolution='c')
        m.drawcoastlines(color='black', linewidth=0.75)
        m.drawcountries(color='grey')
        m.drawmapboundary(color='black', linewidth=1.0)
        m.drawmeridians(np.arange(0,360,30))
        m.drawparallels(np.arange(-90,90,30))

        X,Y = np.meshgrid(lons, lats)
        points = np.clip(points, vmin, vmax)

        palette=plt.get_cmap(cmap)

        ct = m.contour(X, Y, points, y_labels[1:],
                    latlon=True,
                    linestyles='solid',
                    linewidths=0.5,
                    colors='k',
                    vmin=vmin,
                    vmax=vmax )

        ctf = m.contourf(X, Y, points, y_labels,
                    latlon=True,
                    cmap=palette,
                    vmin=vmin,
                    max=vmax)

        if plot_nightshade:
            m.nightshade(plot_dt)

        cb = m.colorbar(ctf,"right",
            size="5%",
            pad="2%",
            ticks=y_labels,
            format = FuncFormatter(eval('self.'+plot_params['formatter'])))

        main_title = "{:s}".format(global_params.title)
        tx_ant_str = "{:s} ({:.1f}dB)".format(global_params.tx_ant_type, global_params.tx_ant_gain)
        if plot_dt.year == 1900:
            ds_fmt_str = "%H:%MUTC %b"
        else:
            ds_fmt_str = "%H:%MUTC %b %Y"
        #pythonProp subtitle
        #sub_title = "{:s} - {:s} - SSN:{:.1f} - {:.3f}MHz - {:s} - {:.0f}W".format(plot_params['title'], plot_dt.strftime(ds_fmt_str), ssn, float(freq), tx_ant_str, global_params.tx_pwr)
        #RSGB subtitle
        sub_title = "{:s} {:.0f}MHz {:s} SIDC ($\mathregular{{R_{{12}}}}$): {:.1f} {:s} {:.0f}W".format(plot_params['title'], float(freq), plot_dt.strftime(ds_fmt_str), ssn, tx_ant_str, global_params.tx_pwr)

        plt.figtext(0.5, 0.8, main_title, fontsize=18, ha='center')
        plt.figtext(0.5, 0.76,sub_title,fontsize=10, fontstyle='normal', ha='center')
        #todo if we're using voacap files we can include the year in the filename
        if not out_file:
            plot_fn = "area_{:s}_{:s}_{:s}.{:s}".format(plot_type, plot_dt.strftime("%H%M_%b"), "d".join(str(freq).split('.')), file_format)
        else:
            plot_fn = "{:s}.{:s}".format(out_file, file_format)
        if out_dir:
            plot_fn = out_dir + plot_fn
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

    def smtr_format(self, x, pos):
        S_DICT = {-14:'S1', -8.18:'S2', -2.16:'S3', 3.86:'S4', 9.1:'S5', \
                    15.92:'S6', 21.94:'S7', 27.96:'S8', 33.98:'S9'}
        if x in S_DICT:
        	return "{:s}".format(S_DICT[x])
            #return _('%(value)ddBW (%(s_value)s)') %{'value':x, 's_value':S_DICT[x]}
        else : return "{:.2f}".format(x)

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
        choices = ['SNR', 'REL', 'E'],
        default = 'REL',
        help = "DATATYPE - a string representation of the data to plot. Default value is 'REL'." )

    plot_mode_parser.add_argument("--nightshade",
        dest = "plot_nightshade",
        action = "store_true",
        default = False,
        help = "Plot day/night regions on map")

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
        choices = ['png', 'svg', 'jpg'],
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
                'rainbow_r', 'YlGnBu', 'gist_rainbow_r', 'winter_r', 'g4fkh'],
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

    pp = PropAreaPlot(args.data_file)
    if hasattr(args, 'list'):
        if args.list:
            pp.dump_datasets()
    if hasattr(args, 'about'):
        if args.about:
            pp.dump_metadata()
    else:
        pp.plot_datasets(plot_files,
            args.data_opt,
            plot_nightshade = args.plot_nightshade,
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
