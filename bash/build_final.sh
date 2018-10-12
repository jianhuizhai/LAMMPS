#!/bin/bash

atomsk dump.dipole.465 dipole465.cfg

# vi dipole465.cfg

atomsk dipole465.cfg dipole465.lmp

python ~/bin/charge.py dipole465.lmp dipole465_used.lmp

ovito dipole465_used.lmp

