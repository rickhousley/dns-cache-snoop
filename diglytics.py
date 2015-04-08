__author__ = 'bug-r'

# For multiple site digs simultaneously
from multiprocessing.pool import ThreadPool as Pool

# For DNS digg-ing
import subprocess
import shlex
import time
# For list to file dumping
import pickle
# Debug rand generator
#import numpy as np

# Configurations

# The number of samples to take duration = num_samples * timeout
#   Use this to scale up to day
num_samples = 1000

timeout = 1 # The assignment gives 1 second dif as criteria

# The list of sites' DNS caches to snoop
dig_list = 'www.china.com', 'www.reddit.com', 'www.roosterteeth.com',\
     'www.cnn.com'


# Threading stuff, leave this alone
pool_size = len(dig_list)  # your "parallelness"
pool = Pool(pool_size)


def main():    

    print 'Processing Sites...'
    
    # Spin off workers for each site
    for site in dig_list:            
        pool.apply_async(digWorker, (site,))        

    # Kill threads
    pool.close()
    pool.join()


def digWorker(site):
    """ Does the dig processing for a given site (threadsafe)"""

    #Build the dig command
    cmd = 'dig ' + site

    consec_auths = 0
    consec_auths_list = []

    for _ in range(0,num_samples):
        
        # Execute the command in a process (basically a shell)
        proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
        out,err=proc.communicate()
        
        # For debugging, disable for quiet
        print(out)

        #Check output for Auth or Answer in response
        if 'AUTHORITY SECTION' in out:
            print 'Not in Cache ' + consec_auths
            consec_auths+=1
        else:
            # Add consec_auths to list if it's not zero, this'll be used for cdf
            if consec_auths is not 0:
                consec_auths_list.append(consec_auths)
            consec_auths_list = 0

        time.sleep(timeout)    

    # Debug generate random consec_auths_list data to test CDF
    #consec_auths_list = np.random.randn(10000)

    # Save list to file
    with open(site+'_consec_auths.txt', 'wb') as f:
        # Pickle just dumps a list to a file in a binary format, will load later
        # We had to dump to file and re-open because matplotlib doesnt deal well
        # with threading. Also this saves our data so we wont have to re-run it
        # for super long durations
        pickle.dump(consec_auths_list,f)

    print 'Site: ' + site + ' Done'

if __name__ == '__main__':
    main()