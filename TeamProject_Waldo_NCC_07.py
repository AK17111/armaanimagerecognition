
import numpy as np
import math as m

def calculate_matrix(img, temp):
    iw, ih = img.shape
    tw, th = temp.shape
    
    r = np.zeros((iw-tw+1, ih-th+1))
    
    for i in range(iw-tw):
        for j in range(ih-th+1):
            r[i, j] = np.sum(((img[i:i+tw, j:j+th]) * temp[:, :]) / m.sqrt((np.sum((img[i:i+tw, j:j+th])**2) * np.sum((temp[:, :])**2))) )
    
    return r
