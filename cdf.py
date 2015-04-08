__author__ = 'bug-r'

import pickle
import numpy as np
import matplotlib.pyplot as plt

# Make sure this matches your other dig-list,
#   should really be offloaded to a config file
dig_list = 'www.china.com', 'www.reddit.com', 'www.roosterteeth.com',\
     'www.cnn.com'

def main():
    # Loop through the list unpacking data and doing CDF on each dataset
    for site in dig_list:
        with open(site+'_consec_auths.txt', 'rb') as f:
            data = pickle.load(f)

        cdf(data,site)

def cdf(data, site):    
    """ Largely addapted from Stack Overflow CDF source """

    # Surrounded in stupid try/except that ignores all errors
    #   this is so it will process all graphs even if there
    #   isnt enough data for previous graphs

    try:
        # Sort the data
        data_sorted = np.sort(data)
        
        # Calculate the proportional values of samples
        p = 1. * np.arange(len(data)) / (len(data) - 1)

        # If it isn't cleared the data will persist from old ones
        plt.clf()
        
        # Plot the sorted data
        plt.plot(data_sorted, p)    
        plt.title(site)
        plt.xlabel('$x$')
        plt.ylabel('$p$')

        plt.savefig(site+'_cdf.png')   

    except:
        pass

if __name__ == '__main__':
    main()