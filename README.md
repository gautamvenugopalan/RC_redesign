[![pipeline status](https://git.ligo.org/40m/RC_redesign/badges/master/pipeline.svg)](https://git.ligo.org/40m/RC_redesign/commits/master)
# RC_redesign

Collection of notebooks / code for the 40m RC re-design for optomechanics.

 - `RClengths.ipynb` --- Notebook for walking through all design considerations for choosing RC lengths and mirror curvatures
 - `PRMtrans.py` ------- Script for determining PRG as a function of PRM transmission and arm cavity losses
 - `Adjacency_DRFPMI_GV.nb` ------- Mathematica notebook working out the adjacency matrix elements relevant to this exercise (consistent with svg schematic).
 - `reqs.txt` -------------- Installs the python requirements to run the notebook.

A simple pipeline is setup to run the following tests: 
 - Install the python dependencies.
 - Run the notebook as a script using nbconvert.
 - Check for errors.
