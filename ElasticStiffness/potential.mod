# potential
# Buckingham potential
pair_style      buck/coul/long 12.0
pair_coeff      1 1     0.0         1.0         0.0    # Mg-Mg
pair_coeff      1 2     929.69     0.29909      0.0    # Mg-O
pair_coeff      2 2     4870.0     0.2670       77.0   # O-O

# MD parameters
kspace_style        ewald/disp    1.0e-12