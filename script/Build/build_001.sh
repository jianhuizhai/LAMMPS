#!/bin/bash

rm -f origin.lmp dipole.lmp

#a=4.218    #   0 GPa
a=4.047    #  30 Gpa
#a=3.935    #  60 GPa
#a=3.828    # 100 GPa

b_posi=$(echo "$a/sqrt(2.0)" | bc -l)
b_negt=$(echo "-1.0*$a/sqrt(2.0)" | bc -l)

nx=80
ny=56

n=$(echo "$ny+1" | bc -l)

x1=$(echo "0.5*$a*sqrt(2.0)*$nx*0.5  + 0.25*$a*sqrt(2.0)*0.25" | bc -l)
y1=$(echo "$a*$ny*0.25 + 0.25*$a" | bc -l)

x2=$(echo "0.5*$a*sqrt(2.0)*$nx*0.5  + 0.75*$a*sqrt(2.0)*0.25" | bc -l)
y2=$(echo "$a*$ny*0.75 + 0.75*$a" | bc -l)

echo "First dislocation position: $x1 $y1"
echo "Second dislocation position: $x2 $y2"

atomsk --create rocksalt $a Mg O orient [110] [001] [1-10] -duplicate $nx $n 1 origin.lmp

atomsk origin.lmp -disloc $x1 $y1 edge z y  $b_negt 0.3275 -disloc $x2 $y2 edge z y $b_posi 0.3275 dipole.lmp

lmp_atom2charge.sh dipole.lmp

ovito dipole.lmp

