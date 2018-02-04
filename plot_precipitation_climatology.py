# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 08:38:34 2018

@author: joshu
"""

import argparse
import iris
iris.FUTURE.netcdf_promote = True
import matplotlib.pyplot as plt
import iris.plot as iplt
import numpy
import cmocean
import iris.coord_categorisation


#
# All your functions (that will be called by main()) go here.
#

def read_data(fname, month):
    """Read in the precipitation flux for month X given
    climatology file pr_file. Also extract this month.
    
    Args:
        pr_file (str): Precipitation data file
        month (str): Month (3 letter abbreviation, e.g. Jun)"""
    
    cube = iris.load_cube(fname, 'precipitation_flux')
    iris.coord_categorisation.add_month(cube, 'time')
    cube = cube.extract(iris.Constraint(month=month))
    
    return cube

def convert_pr_units(cube):
    """Convert the precipitation from kg mm^-2 s^-1 to mm/day. Also
        collapse the data (take average over all data).
    
        Args:
            cube (str): Name of the cube
    """
    cube.data = cube.data * 86400
    cube.units = 'mm/day'    
    
    return cube


def plot_data(cube, month, gridlines=False):
    """Plot the precipitation climatology data for a specific
    month."""
    fig = plt.figure(figsize=[12,5])
    iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
                  levels=numpy.arange(0, 10),
                  extend='max')
    plt.gca().coastlines()
    if gridlines:
        plt.gca().gridlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))

    title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
    plt.title(title)

def main(inargs):
    """Run the program."""

    cube = read_data(inargs.infile, inargs.month)    
    cube = convert_pr_units(cube)
    clim = cube.collapsed('time', iris.analysis.MEAN)
    plot_data(clim, inargs.month)
    plt.savefig(inargs.outfile)


if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("month", type=str, choices=['Jan','Feb','Mar','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], help="Month to plot")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()            
    main(args)