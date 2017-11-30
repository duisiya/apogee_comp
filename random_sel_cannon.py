
# coding: utf-8

# In[1]:

from astropy.io import fits
import numpy as np
import random


# In[2]:

#clean cannon DR 14: no bad or warn stars, no high persistence
cannon_fits = fits.open('cannon_14_clean_all.fits')
cannon = cannon_fits[1].data

#Troup's sample with cannon abundances
troup_fits = fits.open('troup_cannon.fits')
troup = troup_fits[1].data


# In[14]:

len(troup)


# In[10]:

id_array = []
d = 0
no_twin = []
for l in troup: #individual Troup's star for which we are looking for counterparts in DR 14
    #masks: Teff, logg, Fe/H, and SNR + exclude the l-th Troup star from the random search 
    #other Troup stars remain in the DR 14 sample from which we randomly select 
    mask_ID = cannon['APOGEE_ID'] != l['APOGEE_ID']
    
    mask_Teff = np.logical_and(cannon['TEFF'] <= (l['TEFF'] + 100),                                  cannon['TEFF'] >= (l['TEFF'] - 100))
    mask_logg = np.logical_and(cannon['LOGG'] <= (l['LOGG'] + 0.1),                                  cannon['LOGG'] >= (l['LOGG'] - 0.1))
    mask_FeH = np.logical_and(cannon['FE_H'] <= (l['FE_H'] + 0.1),                                  cannon['FE_H'] >= (l['FE_H'] - 0.1))
    mask_SNR = np.logical_and(cannon['SNR'] <= (l['SNR'] + 0.1 * l['SNR']),                                  cannon['SNR'] >= (l['SNR'] - 0.1 * l['SNR']))
    
    masked = cannon[mask_ID & mask_Teff & mask_logg & mask_FeH & mask_SNR]
    n = 0
    
    #some Troup stars have zero counterparts, I'm not going to use them in the analysis
    if len(masked) == 0:
        d = d + 1
        no_twin.append([l['APOGEE_ID'], l['RA'], l['DEC']])


    elif 1 <= len(masked) <= 10: 
    
    # HACKY BELOW BUT IT WORKS 
        k = 0
        n = 0
        #if number of counterparts < 10, I adding them  
        #until the number of selected counterparts = # of counterparts * int(10./ # of counterparts)
        while k < int(10./ len(masked)): 
            for i in range(0, len(masked)): 
                id_array.append([masked[i]['APOGEE_ID'], masked[i]['RA'], masked[i]['DEC']])
                n = n + 1

            k = k + 1
        if n < 10: #the rest of the counterparts are randomly selected until I get 10
            while n < 10:
                r = random.randint(0, len(masked) - 1)
                id_array.append([masked[r]['APOGEE_ID'], masked[r]['RA'], masked[r]['DEC']])
                n = n + 1

                

    #trivial here
    elif len(masked) > 10:
        print l['APOGEE_ID'], len(masked)
        n = 0
        while n < 10: 
             r = random.randint(0, len(masked) - 1)
             print masked[r]['APOGEE_ID']
             n = n + 1 
                #
             id_array.append([masked[r]['APOGEE_ID'], masked[r]['RA'],masked[r]['DEC']])
    


# In[17]:

col1 = fits.Column(name='APOGEE_ID', format='18A', array=np.asarray(id_array)[:,0])
col2 = fits.Column(name='RA', format='D', array=np.asarray(id_array)[:,1])
col3 = fits.Column(name='DEC', format='D', array=np.asarray(id_array)[:,2])


# In[19]:

cols = fits.ColDefs([col1, col2, col3])


# In[20]:

test_sample = fits.BinTableHDU.from_columns(cols)


# In[21]:

test_sample.writeto('test_ids_cannon.fits')


# In[22]:

col1 = fits.Column(name='APOGEE_ID', format='18A', array=np.asarray(no_twin)[:,0])
col2 = fits.Column(name='RA', format='D', array=np.asarray(no_twin)[:,1])
col3 = fits.Column(name='DEC', format='D', array=np.asarray(no_twin)[:,2])


# In[23]:

cols = fits.ColDefs([col1, col2, col3])


# In[24]:

test_sample = fits.BinTableHDU.from_columns(cols)


# In[25]:

test_sample.writeto('troup_lonely_ids.fits')


# In[ ]:



