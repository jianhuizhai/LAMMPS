#!/bin/bash

rm -f origin.lmp dipole.lmp

a=4.218    #   0 GPa
#a=4.047    #  30 Gpa
#a=3.935    #  60 GPa
#a=3.828    # 100 GPa

b_posi=$(echo "$a/sqrt(2.0)" | bc -l)
b_negt=$(echo "-1.0*$a/sqrt(2.0)" | bc -l)

nx=80
ny=30

x1=$(echo "0.5*$a*sqrt(2.0)*$nx*0.5  + 0.25*$a*sqrt(2.0)*0.2" | bc -l)
y1=$(echo "$a*sqrt(3.0)*$ny*0.25 - 0.25*$a*sqrt(3.0)" | bc -l)

x2=$(echo "0.5*$a*sqrt(2.0)*$nx*0.5  + 0.25*$a*sqrt(2.0)*0.2" | bc -l)
y2=$(echo "$a*sqrt(3.0)*$ny*0.75 + 3*0.25*$a*sqrt(3.0)" | bc -l)

echo "First dislocation position: $x1 $y1"
echo "Second dislocation position: $x2 $y2"

echo "charge" > charge.txt
echo "Mg  1.7" >> charge.txt
echo "O  -1.7" >> charge.txt

atomsk --create rocksalt $a Mg O orient [110] [1-11] [1-1-2] -duplicate $nx $ny 1 -prop charge.txt origin.lmp

atomsk origin.lmp -disloc $x1 $y1 edge z y  $b_negt 0.3275 -disloc $x2 $y2 edge z y $b_posi 0.3275 -prop charge.txt dipole.lmp

#lmp_atom2charge.sh dipole.lmp

ovito dipole.lmp

