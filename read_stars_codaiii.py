import numpy as np
from os import listdir, path
from utils import *

def get_nb_lines(in_path):

    dt_line=np.dtype([('buf1','i4'),('id','i4'),('mass','f8'),('x','f8'),('y','f8'),('z','f8'),('age','f8'),('Z/0.02','f8'),('ll','i4'),('tag','i1'),('family','i1'),('buf2','i4')])

    byte_size = path.getsize(in_path)
    bytes_per_line = dt_line.itemsize

    nb_lines = byte_size - (4 + 8 + 4) #remove universe age and buffers
    nb_lines = byte_size / bytes_per_line
    
    assert int(nb_lines) == int(nb_lines//1), "found a non integer number of lines %i in file %s"%(nb_lines, in_path)
    
    return(int(nb_lines))


def read_star_file(in_path):
    """
    masses are in units of solar mass
    ages are in Myr
    x,y,z are in box length units (>0, <1)
    metallicities are in solar units
    """
    dt=np.dtype([('buf1','i4'),('id','i4'),('mass','f8'),('x','f8'),('y','f8'),('z','f8'),('age','f8'),('Z/0.02','f8'),('ll','i4'),('tag','i1'),('family','i1'),('buf2','i4')])

    with open(in_path, 'rb') as src:

        buf = np.fromfile(src,dtype=np.int32, count=1)
        time_myr = np.fromfile(src,dtype=np.float64, count=1)
        buf = np.fromfile(src,dtype=np.int32, count=1)
        
        data=np.fromfile(src, dtype=dt)[['id','mass','x','y','z','age','Z/0.02','family']]



        
    return(time_myr, data)

def read_all_star_files(tgt_path):


    dt=np.dtype([('id','i4'),('mass','f8'),('x','f8'),('y','f8'),('z','f8'),('age','f8'),('Z/0.02','f8'),('family','i1')])

    
    targets = [path.join(tgt_path,f) for f in listdir(tgt_path) if 'star' in f]

    size = 0
    for target in targets:

        size += get_nb_lines(target)
        
    datas = np.zeros((size), dtype = dt)


    size = 0
    for target in targets[:]:


        time_myr, loc_data = read_star_file(target)
        
        l = len(loc_data['mass'])

        datas[:][size:size + l] = loc_data[:][:]

        size += l

    
    return(time_myr, datas)

def read_rank_star_files(tgt_path, rank, Nproc):


    dt=np.dtype([('id','i4'),('mass','f8'),('x','f8'),('y','f8'),('z','f8'),('age','f8'),('Z/0.02','f8'),('family','i1')])

    
    targets = [path.join(tgt_path,f) for f in listdir(tgt_path) if 'star' in f]

    nb_files = len(targets)

    nmin, nmax, nperProc = divide_task(nb_files, Nproc, rank)

    targets = targets[nmin:nmax]
    
    size = 0
    for target in targets:

        size += get_nb_lines(target)
        
    datas = np.zeros((size), dtype = dt)


    size = 0
    for target in targets[:]:


        time_myr, loc_data = read_star_file(target)
        
        l = len(loc_data['mass'])

        datas[:][size:size + l] = loc_data[:][:]

        size += l

    
    return(time_myr, datas)

