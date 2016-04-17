import numpy as np
import scipy as scp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep, clock

name = 'Chicago_Traffic_Tracker_-_Historical_Congestion_Estimates_by_Region.csv'

if __name__ == '__main__':

    #print 'reading csv'
    #sleep(.1)
    #start = clock()
    #df = pd.read_csv(name)
    #print 'time taken: %1.2f' %(clock() - start)
    #
    #print '\nSample data:'
    #print df[:5]
    #print '\n Length: %i\n' %df.shape[0]
    #
    #df = df[df['BUS COUNT'] > 6]
    #idx = df[df['SPEED'] == 0].index.tolist()
    
    #print df.loc[idx]
    #by inspection, see that all zero values occur late at night and don't reflect
    #real traffic, so drop them
    
    #df = df[df['SPEED'] > 0]
    #df = df[df['REGION_ID'] == 1]
    
    #buses read only every ten minutes, but include second information
    #print 'translating time'
    #start = clock()
    #df['TIME'] = df['TIME'].apply(lambda x: 
    #                        pd.Timestamp(x))
    #print 'time taken: %1.2f' %(clock() - start)
    #print df[:10]
    
    
    #check for NaN
    #for key in df:
    #    print '\n %s \n' %key
    #    print df[df[key].isnull()]
    
    #df.to_csv('region1.csv')
    
    df = pd.read_csv('region1.csv')
    df['Time of Day'] = df['TIME'].apply(lambda x: int(x[-8:-6])+float(x[-5:-3])/60)
        
    vals = df.groupby('Time of Day')['SPEED'].mean()
    #not much value between midnight and 4:30, need some smoothing for clean data
    w_range = 5
    smooth = [1.0/(1+2*w_range)]*(1+2*w_range)
    vals.as_matrix()[:] = np.convolve(vals.as_matrix(), smooth, 'same')
    mask = vals.index.map(lambda x: 23.0>x>5.3)
    vals = vals[mask]
    
    mpl.style.use('seaborn-whitegrid')
    fig = plt.figure(figsize=(12,10))
    ax = plt.gca()
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(
            [6, 8, 10, 12, 14, 16, 18, 20, 22]))
    
    plt.xlabel('Time of Day', fontsize=20, color=(.6, .3, .0))
    plt.ylabel('Traffic Speed (MPH)', fontsize=20, color=(.6, .3, .0))
    plot = vals.plot(color=(.6, .3, .0))
    plot.tick_params(axis='both', which='major', labelsize=18)
    fig.suptitle('Chicago Traffic: Region 1', fontsize=24, color=(.2, .05, 0))
    #plt.savefig('plot1.jpg')
    
    
    mask = df['Time of Day'].apply(lambda x: 16 <= x <= 18)
    df = df[mask]
    print np.sum(mask.as_matrix())
    df['Day of Week'] = df['TIME'].apply(lambda x: pd.Timestamp(x).dayofweek)

    vals = df.groupby('Day of Week')['SPEED'].mean()
    print vals
    fig = plt.figure(figsize=(12,10))
    plot = vals.plot(kind='bar', color=(.6, .3, .0), ylim=(18, 20.5))
    ax = plt.gca()
    ax.set_position((.1, .2, .8, .7))
    ax.set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday'])
    plot.tick_params(axis='both', which='major', labelsize=18)
    plt.xlabel('Day of Week', fontsize=20, color=(.6, .3, .0))
    plt.ylabel('Traffic Speed (MPH)', fontsize=20, color=(.6, .3, .0))
    fig.suptitle('Chicago Rush Hour Traffic: Region 1', 
                    fontsize=24, color=(.2, .05, 0))
    plt.savefig('plot2.jpg')
    
    