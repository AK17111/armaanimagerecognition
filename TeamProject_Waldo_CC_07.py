
import numpy as np

def calculate_matrix(img, temp):
 
     #Get the width and height of 
     iw, ih = img.shape
     tw, th = temp.shape
     
     r = np.zeros((iw-tw+1, ih-th+1))
    
     for i in range(iw-tw+1):
         for j in range(ih-th+1):
             r[i][j] = np.sum( ((img[i:i+tw, j:j+th]) - (img[i:i+tw, j:j+th].mean())) * (temp[:,:] - (temp[:,:].mean())))
             
     return r
