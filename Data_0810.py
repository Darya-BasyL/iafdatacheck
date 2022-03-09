#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


# In[2]:


path = 'C://IAF//0810/'
filelist = os.listdir(path)


# In[3]:


filelist


# In[4]:


spectrnames = ['S048121', 'S048133', 'S074872']
head_num = {'t2': [None, None, None],
            't3': [None, None, None],
            't1': [None, None, 14]}
timefr = ['t2' ,'t3', 't1']


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
    readedfile = pd.read_csv(file,  sep = '\t', header = headnum, decimal = ',')
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


# In[14]:


def getmin(dict, newdict, x):
    for key in dict.keys():
        new = []
        for i in range(len(dict[key])):
            new.append(dict[key][i][x])
        newdict.update({key: min(new)})
    return newdict


# In[15]:


mintime = {}
getmin(time, mintime, 0)


# In[100]:


timesec = {}
for key in time.keys():
    new = []
    for i in range(len(time[key])):
        delta = time[key][i] - mintime[key]
        new.append(delta.dt.seconds)
    timesec.update({key : new})


# In[21]:


timediff = {}
for key in timesec.keys():
    new = []
    for i in range(len(timesec[key])):
        new.append(np.diff(timesec[key][i]))
    timediff.update({key : new})


# In[22]:


def showdiff(dict, legend, timeframe, num):
    for i in range(num):
        plt.plot(dict[timeframe][i], label = legend[timeframe][i])
    return plt.legend()
    return plt.show()


# In[44]:


plt.plot(np.diff(timesec['t3'][0][54:60]), label = spectr_files['t3'][0])
plt.show()


# In[23]:


showdiff(timediff, spectr_files, 't1', 3)


# In[24]:


showdiff(timediff, spectr_files, 't2', 3)


# In[25]:


showdiff(timediff, spectr_files, 't3', 3)


# In[26]:


def approx_bright(time_old, time_new, bright, wlenght):
    bright_new = pd.DataFrame(columns = wlenght)
    for i in range(1024):
        y = CubicSpline(time_old, bright.iloc[:,i])
        newy = y(time_new)
        bright_new[wlenght[i-2]] = newy
    return bright_new


# In[33]:


newcol = dict(zip(bright['t1'][1].columns, wlenght))
bright_t1_1 = bright['t1'][1].rename(columns = newcol)


# In[ ]:


bright_new = {}
new_time_num = 1
for key in bright.keys():
    new = []
    for i in range(len(bright[key])):
        if i == new_time_num:
            newcol = dict(zip(bright[key][i].columns, wlenght))
            bright[key][i] = bright[key][i].rename(columns = newcol)
            new.append(bright[key][i])
        else:
            new.append(approx_bright(timesec[key][i], timesec[key][new_time_num], bright[key][i], wlenght))        
    bright_new.update({key : new})


# In[92]:


a = pd.Series(timesec['t1'][0])
b = pd.Series(timesec['t2'][0])
c = pd.Series(timesec['t3'][0])


# In[98]:


time_all = pd.concat([timesec['t1'][1],timesec['t2'][1]], ignore_index=True)
time_all = pd.concat([time_all, timesec['t3'][1]], ignore_index=True)


# In[99]:


time_all


# In[ ]:


bright_new = []
new_time_num = 1
for key in bright.keys():
    new = []
    for i in range(len(bright[key])):
        if i == new_time_num:
            newcol = dict(zip(bright[key][i].columns, wlenght))
            bright[key][i] = bright[key][i].rename(columns = newcol)
            new.append(bright[key][i])
        else:
            new.append(approx_bright(timesec[key][i], timesec[key][new_time_num], bright[key][i], wlenght))        
    bright_new.update({key : new})


# In[74]:


def show_intence(bright, time, lenght, legend, key):
    for i in range(3):
        plt.plot(time[key][1], bright[key][i][lenght], label = legend[key][i])
    plt.xlabel('t, sec --->')
    plt.ylabel('Intense --->')
    plt.title('Длина волны ' + lenght)
    return plt.legend()
    return plt.show()


# In[85]:


show_intence(bright_new, timesec, '342,339', spectr_files, 't3')


# In[ ]:




