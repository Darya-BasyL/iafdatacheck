#!/usr/bin/env python
# coding: utf-8

# In[21]:


import os
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


# In[3]:


path = 'D://IAF//DATA//0810/'
filelist = os.listdir(path)


# In[4]:


spectrnames = ['S048121', 'S048133', 'S074872']
head_num = {'t2': [None, None, None],
            't3': [None, None, None],
            't1': [None, None, 14]}
timefr = ['t2' ,'t3', 't1']
#spectr_dic = dict(zip(spectrnames,head_num))


# In[5]:


def get_file_list(spectrname, filelist):
    spectrfilelist = [i for i in filelist if spectrname in i]
    return spectrfilelist


# In[6]:


spectr_first = get_file_list(spectrnames[0], filelist)
spectr_sec = get_file_list(spectrnames[1], filelist)
spectr_third = get_file_list(spectrnames[2], filelist)


# In[7]:


spectr_files = {}
for i in range(len(spectr_first)):
    spectr_files.update({timefr[i] : [spectr_first[i], spectr_sec[i], spectr_third[i]]})


# In[8]:


spectr_files


# In[9]:


def read_file(file, headnum):
    readedfile = pd.read_csv(file,  sep = '\t', header = headnum)
    return readedfile


# In[10]:


readedfiles = {}
for key in spectr_files.keys():
    new = []
    for i in range(len(spectr_files[key])):
        new.append(read_file(path+spectr_files[key][i], head_num[key][i]))
    readedfiles.update({key: new})


# In[11]:


wlenght = readedfiles['t1'][2].columns[2:]


# In[68]:


#readedfiles['t1'][2].iloc[:,0]
pd.to_datetime(readedfiles['t1'][2].iloc[:,0]).dt.second

readedfiles['t1'][0].iloc[:,1:]
wlenght


# In[12]:


time = {}
for key in readedfiles.keys():
    new = []
    for i in range(len(readedfiles[key])):
        new.append(pd.to_datetime(readedfiles[key][i].iloc[:,0]))
    time.update({key: new})


# In[13]:


bright = {}
for key in readedfiles.keys():
    new = []
    for i in range(len(readedfiles[key])):
        new.append(readedfiles[key][i].iloc[:,2:])
    bright.update({key: new})


# In[60]:


bright['t1'][0]


# In[14]:


mintime = {}
for key in time.keys():
    new = []
    for i in range(len(time[key])):
        new.append(time[key][i][0])
    mintime.update({key : min(new)})


# In[15]:


timesec = {}
for key in time.keys():
    new = []
    for i in range(len(time[key])):
        delta = time[key][i]-mintime[key]
        new.append(delta.dt.seconds)
    timesec.update({key : new})


# In[16]:


np.diff(timesec['t1'][0])


# In[17]:


def getmin(dict, newdict, x):
    for key in dict.keys():
        new = []
        for i in range(len(dict[key])):
            new.append(dict[key][i][x])
        newdict.update({key: min(new)})
    return newdict
minmintime = {}
getmin(time, minmintime, 0)


# In[18]:


timediff = {}
for key in timesec.keys():
    new = []
    for i in range(len(timesec[key])):
        new.append(np.diff(timesec[key][i]))
    timediff.update({key : new})


# In[19]:


timediff['t1']


# In[22]:


def showdiff(dict, legend, timeframe, num):
    for i in range(num):
        plt.plot(dict[timeframe][i], label = legend[timeframe][i])
    return plt.legend()
    return plt.show()

showdiff(timediff, spectr_files, 't1', 3)


# In[23]:


showdiff(timediff, spectr_files, 't2', 3)


# In[24]:


showdiff(timediff, spectr_files, 't3', 3)


# In[108]:


y = pd.DataFrame(columns = wlenght)


# In[104]:


bright['t1'][0]


# In[87]:


#for i in range(2,1025):
 #   bright['t1'][2][i] = int(bright['t1'][2][i])
bright['t1'][0][2].astype(float)


# In[109]:





# In[25]:


#def approximate(time_old, time_new, bright):
#    y = CubicSpline(time_old, bright)
#    bright_new = y(time_new)
#    return bright_new


# In[94]:


def approx_bright(time_old, time_new, bright, wlenght):
    bright_new = pd.DataFrame(columns = wlenght)
    for i in range(2,1026):
        y = CubicSpline(time_old, bright[i].astype(float))
        newy = y(time_new)
        bright_new[wlenght[i-2]] = newy
    return bright_new


# In[70]:


#bright_t1_0_new = pd.DataFrame(columns = wlenght)
#for i in range(2,1026):
#    bright_t1_0_new[wlenght[i-2]] = approximate(timesec['t1'][0], timesec['t1'][1], bright['t1'][0][i])


# In[96]:


#approx_bright(timesec['t1'][2], timesec['t1'][1], bright['t1'][2], wlenght)
wlenght


# In[78]:


bright_new = {}
new_time_num = 1
for key in bright.keys():
    new = []
    for i in range(len(bright[key])):
        if i = new_time_num:
            new.append(bright[key][i])
        new.append(approx_bright(timesec[key][i], timesec[key][new_time_num], bright[key][i], wlenght))        
    bright_new.update({key : new})


# In[ ]:


def show_intence(dict, legend, timeframe, num):
    for i in range(num):
        plt.plot(dict[timeframe][i], label = legend[timeframe][i])
    return plt.legend()
    return plt.show()


# In[54]:


bright['t1'][0]


# In[ ]:




