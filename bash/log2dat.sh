#!/bin/bash
export LC_NUMERIC=C

### PURPOSE:
### This script extracts part of the data from a LAMMPS log file ("log.lammps")
### and writes it into a data file containing only two columns.
### The user must provide the names of the two fields that must be extracted,
### as they exist in the log file (e.g. Step, PotEng, Temp, Press...)
### The goal is to plot one property as function of the other.

### USAGE:
###   log2dat.sh <field1> <field2> [<outfile>]
### where <field1> and <field2> must be field names as printed by the "thermo_style" command.
### <outfile> is optional, and will be used as the name of the output data file.

### EXAMPLES:
### Extract the temperature as function of the time step:
###   log2dat.sh Step Temp
### Extract the potential energy as function of volume:
###   log2dat.sh Volume PotEng V_pe.dat

### PRE-REQUISITE:
### - a file named "log.lammps" must exist in current directory
### - the "thermo_style" used in the LAMMPS simulation must be the same along the whole log.lammps
###   (i.e. the "thermo_style" must be defined only once in the LAMMPS input script, and not modified afterwards)

# Just a fancy header
printf "___________________________________________________________\n"
printf "\e[1m                    L O G 2 D A T\n"
printf "         Extracting data from LAMMPS log file\e[0m\n"
printf "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

if [[ -z "$@" ]]; then
  printf "\e[1m Usage:\e[0m  log2dat.sh <f1> <f2> [<outfile>] \n"
  printf " where <f1> and <f2> must be names as used in the 'thermo_style' command.\n"

else

  if [ $# -le 1 ] || [ $# -ge 4 ]; then
    printf "\e[1m X!X ERROR:\e[0m illegal number of arguments.\n"
    printf "___________________________________________________________\n"
    exit
  fi

  if [ ! -e log.lammps ] ; then
    printf "\e[1m X!X ERROR:\e[0m log.lammps: no such file in current directory.\n"
    printf "___________________________________________________________\n"
    exit
  fi

  ### Get the arguments entered by user
  f1=$1
  f2=$2
  outfile=$3

  ### Check that f1 and f2 are not empty
  if [ "$f1" = "" ] || [ "$f2" = "" ] ; then
    printf "\e[1m X!X ERROR:\e[0m expected two field names as arguments.\n"
    printf "___________________________________________________________\n"
    exit
  fi

  ### If user did not provide an output file name, use a default one
  if [ "$outfile" = "" ] ; then
    outfile="${f2}_${f1}.dat"
  fi

  ### Extract the line containing the names of the fields (as written by "thermo_style" command)
  ### NOTE: only the first line containing "Step" is taken into account
  ### If your LAMMPS script performs several calculations, then the "thermo_style"
  ### should be the same for all calculations
  line=$(grep "Step" log.lammps | head -n 1)

  i=0
  n1=0
  n2=0
  for f in $line ; do
    let i++
    if [ $f = $f1 ] ; then
      n1=$i
    elif [ $f = $f2 ] ; then
      n2=$i
    fi
  done

  ### Save total number of fields
  Nf=$i

  if [ $n1 = 0 ] ; then
    printf "\e[1m X!X ERROR:\e[0m the field '$f1' does not exist in log.lammps.\n"
    printf "           Please specify existing fields among the following:\n"
    printf "     $line \n"
    printf "___________________________________________________________\n"
    exit
  fi
  if [ $n2 = 0 ] ; then
    printf "\e[1m X!X ERROR:\e[0m the field '$f2' does not exist in log.lammps.\n"
    printf "           Please specify existing fields among the following:\n"
    printf "     $line \n"
    printf "___________________________________________________________\n"
    exit
  fi

  ### Check if the output file already exists
  while [ -e $outfile ] ; do
    printf " <?> The file $outfile already exists. Overwrite? (y/n): "
    read answer
    if [[ "${answer}" = "y" || "${answer}" = "Y" ]] ; then
      rm -f $outfile
    else
      printf " <?> Enter a name for the output file: "
      read outfile
    fi
  done
  rm -f $outfile

  printf " Extracting $f1 and $f2 from log.lammps ..."

  ### Write a header in the data file
  echo "# $f1      $f2" > $outfile

  ### Extract the relevant data
  ### - grep keeps only lines that do not contain pairs of letters (a-z or A-Z, followed by a-z or A-Z)
  ### - then, awk keeps only lines that contain exactly $Nf fields
  ### - then, awk keeps only the fields number $n1 and $n2
  grep -v "[a-zA-Z][a-zA-Z]" log.lammps | awk -v nf="$Nf" 'NF==nf' | awk -v m="$n1" -v n="$n2" '{print $m "   " $n}' >> $outfile

  printf " Done.\n"
  echo " Data was written in: $outfile"
fi

printf "___________________________________________________________\n"

