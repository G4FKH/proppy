#!/usr/bin/env python

from distutils.core import setup

setup(name='proppy',
      version='0.1',
      description='Propagation Prediction Plotting Utilities',
      author='James Watson',
      author_email='jwatson@mac.com',
      py_modules=['proppy.predictionParams',
                    'proppy.propAreaPlot',
                    'proppy.propP2PPlot',
                    'proppy.rec533Out',
                    'proppy.cmap.plotlyAlt'],
     )
