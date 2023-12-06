2023/12/5

Mini script to create files for simulation runs
This is mainly a series of patchwork scripts to help generate
parameter files for CP2K equilibration, using MCBP amber files
and non-bonded metal parameterization model

Require installation of python's version of ambertools to use MCPB 

*Usage note* 
At the current stage, the error handling of the script is minimal. 
The .sh file serves mostly as a mean to keep track of commandlines 
and data transformation that must be manually retyped/require manual
 adjustment in the original protocol. 
