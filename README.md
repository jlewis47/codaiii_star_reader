# codaiii_star_reader
Quick python code for reading the output of the unformatted binary files containing stellar particle information in Cosmic Dawn III (built in python 3.7.6) 
2 functions : One is for reading individual files (possibly useful since different files correspond to different regions). The other reads in all star files
in a given directory (beware if you have other files in the directoy that contain "star" there will be issues)


quick usage example: 


>>datas=read_all_star_files('/gpfs/alpine/proj-shared/ast031/jlewis/CoDaIII/prod_sr/getstarlist_runs/output_000034')   

>>datas['mass']



available keys are: 'id','mass','x','y','z','age','Z/0.02'
mass is in solar units
age is in Myr
Z/0.02 is (a bit explicitly) in solar metallicities
x,y,z are in box units (so 0<=x,y,z<=1 -- you can get the cell coordinates by multiplying by 8196, which is the number of cells per box side)
