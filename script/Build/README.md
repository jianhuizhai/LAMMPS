This folder contains bash scripts which are used to construct dislocation dipole configuration with accurate dislocation position.
===================================================================================================================================
* build_with_charge.sh is used to build system with charge which is used to check system charge

* build_110.sh is used to build config of slip system [110] (1-10)
* build_001.sh is used to build config of slip system [110] (001)
* build_with_charge.sh is used to build system with charge and also it is useful to check the total charge of system.
* build_in_plane.py is used to remove atom which is in a cyclinder around dislocation core position.
* job_submit.py is used to submit job on cluster. (Some commands may be need to change according to different jobs)
* build_in_cylinder is used to select atoms in the specified cylinder.
