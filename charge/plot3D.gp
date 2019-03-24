#!/usr/bin/gnuplot

### This script aims at displaying a 3-D plot with gnuplot
### NOTE: before opening this script with gnuplot,
### please edit and modify some values below
### (see comments starting with "MODIFY").

### For visualization, run:
###   gnuplot plot3D.gp

set encoding iso_8859_1

### MODIFY: if you want to output to an EPS file, then uncomment
### the 2 following lines, and comment or remove the last line ("pause -1")
#set terminal postscript eps enhanced size 400,400
#set output 'density.eps'

### Graph parameters
set pm3d map   # If you wish for a 2-D projection
#set pm3d       # If you wish for a true 3-D visualization
set hidden3d
set view 0,0
set samples 40
set isosamples 40
set ytics offset 0.0,-0.8
set palette rgb 33,13,10
set xyplane 0
set size 0.66,1
set nokey

### Set title of graph and axes
set title "Some quantity I computed"
set xlabel "X" font "Helvetica,20"
set ylabel "Y" font "Helvetica,20"
#set zlabel "Value" font "Helvetica,20"

### MODIFY: set xrange and yrange according to your system size
### (or comment it out to leave automatic scaling of axes)
#set xrange [0:100]
#set yrange [0:100]

### MODIFY: set cbrange according to the value range of your system
### (or comment it out to leave automatic scaling of colours)
#set cbrange [-0.01:0.01]

### MODIFY: use the name of the date file you want to visualize
file = 'file.dat'
splot file using 1:2:3 with pm3d

pause -1

