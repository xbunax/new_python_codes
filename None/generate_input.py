import commands
import shutil
import os
import sys
import time
import linecache
#import numpy as np
import math

do_submit = True

delete_help_file = True # if True, delete all current jobs_*, out, err files

Ncell = 4 
Nsite = Ncell*Ncell
#mus = [0.0, -0.05, -0.1, -0.15, -0.2, -0.25, -0.3, -0.35, -0.4, -0.45, -0.5, -0.55, -0.6, -0.65, -0.7, -0.75, -0.8, -0.85, -0.9, -0.95, -1.0, -1.1, -1.2]#, -1.3, -1.4, -1.5]#, -0.08, -0.1, -0.12, -0.14, -0.16, -0.18, -0.2]#, -0.1, -0.12, -0.14, -0.16, -0.18, -0.2, -0.22, -0.24]#, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0, -1.1, -1.2, -1.3, -1.4, -1.5, -1.6, \
#      -1.7, -1.8, -1.9, -2.0, -2.1, -2.2, -2.3, -2.4, -2.5, -2.6, -2.7, -2.8, -2.9, -3.0, \
#      -3.1, -3.2, -3.3, -3.4, -3.5]#, -3.6, -3.7, -3.8, -3.9, -4.0]
#mus = [0.0]
#mus = [-0.55, -0.6, -0.65, -0.7, -0.75, -0.8, -0.85, -0.9, -0.95, -1.0]
#mus = [0.0, -0.05, -0.1, -0.15, -0.2]
#mus = [-0.75, -0.8, -0.9, -1.0]
mus = [0.0, -0.1, -0.2, -0.3, -0.4, -0.5]

V1 = 0.05
#V2s = [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
#V2s = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4]
V2s = [0.01]#, 0.8, 1.2, 1.6]
V12s = V2s
tps = [0.0]
Vp = 0.0
U1s = [4]
U2s = [4]

seeds = [1234567]#, 3234567]#, 3234567, 4234567, 5234567, 6234567, 7234567, 8234567, 9234567]

#! betas following: 
#          0.4, 0.45,  0.5, 0.55,  0.6,  0.7,  0.8,  0.9,   1,    1.2,   1.5,   1.6,   1.8,    2,    2.5,   3,    3.2,  3.5,  4,   4.2,   5,   6,   7,   8,   10,  15,    20,    25
Ls      = [40,   45,   50,   55,   30,   35,   40,   45,    40,    48,    30,    32,    36,    40,    50,   30,   32,   35,   40,   42,   50,  60,  70,  80,  100, 120,   160,   200]
dtaus   = [0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02,  0.025, 0.025, 0.05, 0.05, 0.05,  0.05,  0.05,   0.1,  0.1,  0.1,  0.1,  0.1,  0.1, 0.1, 0.1, 0.1,  0.1, 0.125, 0.125, 0.125]
norths  = [10,   9,    10,   11,   10,   7,    10,   9,     10,    12,    10,    8,      8,    10,    10,   10,    8,    7,   10,    7,   10,  10,  10,  10,   10,  10,   10,    10]

#          1,    1.2,   1.5,   1.6,    2,   2.5,   3,    3.2,  3.5,  4,   4.2,   5,   6,   7,   8,   10,   12,    15,    20,    25,    30,    35,    40
Ls      = [40,    48,    30,    32,    40,   50,   30,   32,   35,   40,   42,   50,  60,  70,  80,  100,  96,    120,   160,   200,   240,   280,  320]
dtaus   = [0.025, 0.025, 0.05, 0.05, 0.05,  0.05, 0.1,  0.1,  0.1,  0.1,  0.1,  0.1, 0.1, 0.1, 0.1,  0.1, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
norths  = [10,    12,    10,    8,     10,   10,   10,    8,    7,   10,    7,   10,  10,  10,  10,   10,   8,    10,    10,    10,    10,    10,   10]

#! betas following: 
#          2,    3,   4,   5,   6,   7,   8,   10,  12.5,  20, 25
#Ls      = [20,  30,   40,  50,  60,  70,  80,  100, 100,   160]#,   200]
#dtaus   = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.125, 0.125]#, 0.125]
#norths  = [10,  10,   10,  10,  10,  10,  10,   10,  10,   10]#,    10]

#! betas following: 
#          6,   7,   8,   10,  12.5,  15
#Ls      = [60,  70,  80,  100, 100,   120]
#dtaus   = [0.1, 0.1, 0.1, 0.1, 0.125, 0.125]
#norths  = [10,  10,  10,   10,  10,   10]

#          10,  12.5,  15
#Ls      = [80, 100,   120]
#dtaus   = [0.125, 0.125, 0.125]
#norths  = [10,  10,   10]

#          5,   6,   7,   8,   10,    12.5,  15,    20,  25,   30,    40
#Ls      = [50,  60,  70,  80,  80,    100,   120,   160, 200]#,   240,  320]
#dtaus   = [0.1, 0.1, 0.1, 0.1, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
#norths  = [10,  10,  10,  10,   10,    10,   10,    10,     10,    10,   10]

#          15
#Ls      = [50]
#dtaus   = [0.05]
#norths  = [10]

#          30    40
#Ls      = [240,  320]
#dtaus   = [0.125, 0.125, 0.125, 0.125]
#norths  = [10,     10,    10,   10]

#          40
Ls      = [40]
dtaus   = [0.1]
norths  = [10]

#          30
#Ls      = [240]
#dtaus   = [0.125]
#norths  = [10]

#! betas following for calculating entropy: 
#          0.01,   0.05,   0.1,   0.2,  0.3,  0.4, 0.45,  0.5, 0.55,  0.6,  0.7,  0.8,  0.9,   1,    1.2,   1.5,   1.6,   1.8, 2.2,  2.5,   2.8,  3.2,  3.5, 4.2,  5.5,  
#Ls      = [20,     20,     20,    20,   30,   40,   45,   50,   55,   30,   35,   40,   45,    40,    48,    30,    32,    36,  44,   50,   28,   32,   35,   42,  44]
#dtaus   = [0.0005, 0.0025, 0.005, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02,  0.025, 0.025, 0.05, 0.05, 0.05, 0.05,  0.05, 0.1,  0.1, 0.1,  0.1, 0.125]
#norths  = [10,     10,     10,    10,   10,    10,   9,    10,   11,   10,   7,   10,    9,    10,    12,    10,    8,      8,  11,   10,    7,    8,    7,    7,  11]

#Ls      = [50,   56,   64,   70,   60,   40,  42,  50,  60,  70,  80,  100, 120, 160]#,   200]
#dtaus   = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.125]#, 0.125, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
#norths  = [10,   8,    8,    10,   10,   10,  7,   10,  10,  10,  10,  10,  10,  10]#,    10]
ntry    = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]
ntry2   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]
#ntry    = [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#ntry2   = [1,1,1,1,1,1,1,1,1]

tdm = 1
HSF = -1      # -1 = random, 1 = from file 
nbin = 10      # only applies for non-MPI run
FTphy = 1    # if do FT for phy0

node = 1
walltime = "3:30:00"

def clean():

    for i in range(0,len(temp)):

        if os.path.exists("./T_" + str(temp[i])):
            shutil.rmtree("./T_" + str(temp[i]))

        cmd = "mkdir T_" + str(temp[i])
        os.system(cmd)

def prepare_input_file(filename, outputname, i, s, m):

    file = open(filename, "r")
    text = file.read()
    file.close()

    text = text.replace("OUTPUT"    , str(outputname))
    text = text.replace("GEOM"      , str(geomfile))

    if(Ls[i] >= 50):
        text = text.replace("NMEASval"    , str(3000))
    else:
        text = text.replace("NMEASval"    , str(3000))

    if(Ls[i] >= 50):
        text = text.replace("NWARMval"   , str(1200))
    else:
        text = text.replace("NWARMval"   , str(1200))

    text = text.replace("SEEDval"    , str(seeds[s]))
    text = text.replace("MUval"      , str(mus[m]))

    text = text.replace("Lval"    , str(Ls[i]))
    text = text.replace("DTAUval" , str(dtaus[i]))

    text = text.replace("NTRYval"   , str(ntry[i]))
    text = text.replace("NTRY2val"  , str(ntry2[i]))
    text = text.replace("TDMval"    , str(tdm))

    text = text.replace("NORTHval"  , str(norths[i]))

    text = text.replace("HSFval"    , str(HSF))
    text = text.replace("NBINval"   , str(nbin))

    text = text.replace("FTPHY" , str(FTphy))

    file = open(filename, "w")
    file.write(text)
    file.close()

def prepare_geom_file(geomfile, iU, iV, tp):

    file = open(geomfile, "r")
    text = file.read()
    file.close()

    text = text.replace("NCELL",  str(Ncell))
    text = text.replace("U1val" ,  str(U1s[iU]))
    text = text.replace("U2val" ,  str(U2s[iU]))
    text = text.replace("V1val" ,  str(V1))
    text = text.replace("V2val" ,  str(V2s[iV]))
    text = text.replace("V12val" ,  str(V12s[iV]))
    text = text.replace("tpval" ,  str(tp))
    file = open(geomfile, "w")
    file.write(text)
    file.close()

cmd = "rm jobs_*"
if(delete_help_file):
    os.system(cmd)

#cmd = "rm -r run_*"
#if(delete_help_file):
#    os.system(cmd)

#cmd = "rm out_*"
#if(False and delete_help_file):
#    os.system(cmd)

cmd = "rm error_*"
if(False and delete_help_file):
    os.system(cmd)

for iU in range(0, len(U1s)):
    for iV in range(0, len(V2s)):
        for tp in tps:
       	    lattice  = "U"+str(U1s[iU])+"_V"+str(V1)+"_tp"+str(V2s[iV])+"_N"+str(Nsite)
    	    geomfile = "geomU"+str(U1s[iU])+"_V"+str(V1)+"_tp"+str(V2s[iV])+"_N"+str(Nsite)
            print lattice  

            cmd = "cp g_template" + " "+ geomfile
            print cmd
            os.system(cmd)

            prepare_geom_file(geomfile, iU, iV, tp)

            for m in range(0, len(mus)):
                for i in range(0, len(Ls)):

                    beta = Ls[i]*dtaus[i]
                    print "L=", Ls[i], "dtau=", dtaus[i], "beta = ", beta, "mu = ", mus[m]

                    dir = "./"+lattice+"_be" + str(beta)+"_mu" + str(mus[m])

                    if not os.path.exists(dir):
                      cmd = "mkdir " + dir
                      os.system(cmd)
                      cmd = "cp main.e " + dir
                      os.system(cmd)
                      cmd = "cp " + geomfile + " "+ dir
                      os.system(cmd)

                    for s in range(0,len(seeds)):

                        input_file_name    = dir + "/input_seed" + str(seeds[s])
                        data_file_name     = lattice + "_be" + str(beta)+ "_s" + str(seeds[s])+ "_mu" + str(mus[m])

                        cmd = "cp ./in_template " + input_file_name + ";"
                        os.system(cmd)
                        prepare_input_file(input_file_name, data_file_name, i, s, m)

                        batch_str = ""
                        
			if node==1:
                            batch_str = batch_str + "./main.e " + dir + "/input_seed"+ \
                                            str(seeds[s])+" > out_"+lattice+ "_be" + str(beta)+ "_s" + str(seeds[s])+ "_mu" + str(mus[m]) +"\n"
                        elif node>1:
                            batch_str = batch_str + "mpirun -np "+str(node)+" ./main.e " + dir + "/input_seed"+ \
                                            str(seeds[s]) +"\n"

                        file = open("batch_script.pbs", "r")
                        text = file.read()
                        file.close()

                        jobs_file_name = dir + "/jobs_"+lattice+"_be"+ str(beta)+ "_s"+str(seeds[s])+".slm"
                
                        text = text.replace("NODES"  , str(node))
                        text = text.replace("WALLTIME"  , str(walltime))
                        text = text.replace("MPI"   , str(node*8))
                        text = text.replace("BETA" , str(beta))
                        text = text.replace("SEED" , str(seeds[s]))
                        text = text.replace("JOBS" , str(batch_str))
                        text = text.replace("LATTICE" , lattice)
			text = text.replace("tpval" ,  str(tp))
                        text = text.replace("V1val" ,  str(V1))
                        text = text.replace("V2val" ,  str(V2s[iV]))
                        text = text.replace("V12val" ,  str(V12s[iV]))
                        text = text.replace("muval" ,  str(mus[m]))

                        if(not batch_str == ""):
                    	    file = open(jobs_file_name, "w")
                    	    file.write(text)
                    	    file.close()
     
                        if(do_submit):
                    	    cmd = "qsub " + jobs_file_name
                     	    os.system(cmd)

