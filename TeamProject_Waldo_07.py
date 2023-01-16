

import matplotlib as mp
import numpy as np
import time
import TeamProject_Waldo_SSD_07 as SSD
import TeamProject_Waldo_NCC_07 as NCC
import TeamProject_Waldo_CC_07 as CC



#This function takes in a 3D array (such as an image) and converts each of the values to make it into a 2D grayscaled matrix
def convertToGray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


#This method identifies and returns the minimum value, min x index, and min y index of the given matrix
def minMatrixVals(matrix):
    Mmin = np.amax(matrix)
    MminX = 0
    MminY = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < Mmin:
                if matrix[i][j] != 0:
                    Mmin = matrix[i][j]
                    MminX = i
                    MminY = j
                    
    return Mmin, MminX, MminY


#This method identifies and returns the maximum value, max x index, and max y index of the given matrix
def maxMatrixVals(matrix):
    Mmax = np.amin(matrix)
    MmaxX = 0
    MmaxY = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > Mmax:
                if matrix[i][j] != 0:
                    Mmax = matrix[i][j]
                    MmaxX = i
                    MmaxY = j
                    
    return Mmax, MmaxX, MmaxY



def main():
    
    #Get the image names
    c_img = input('Enter the name of the color image file: ')
    c_temp = input('Enter the name of the color template file: ')
    
    #Read them in as images
    c_img = mp.image.imread(c_img)
    c_temp = mp.image.imread(c_temp)
    
    #Use user-defined function to convert the RGB image to grayscale
    #Use np.array to convert data type into correct format (uint8)
    g_img = convertToGray(np.array(c_img, dtype=np.uint8))
    g_temp = convertToGray(np.array(c_temp, dtype=np.uint8))
    
    
    #Get user input - how they want to analyze the image
    method = ''
    while method != 'ssd' and method != 'ncc' and method != 'cc' and method != 'all':
        method = input("How you want to search for the template?\n\tSum of Squared Differences (Enter 'SSD')\n\tNormalized Cross Correlation (Enter 'NCC')\n\tCorrelation Coeficcient CC\n\tCombine all three (Enter 'All')\n")
        method = method.lower()
    
    #Begin measuring time of excecution
    start = time.time()
    
    #Perform calculations based on the user's input
    if method == 'ssd':
        
        #Use the function to get the output matrix after SSD is applied
        r = SSD.calculate_matrix(g_img, g_temp)
        
        #Find the minimum point (which is the closest match identified by SSD)
        rmin, rminX, rminY = minMatrixVals(r)
        
        #Define the rectangle that surrounds the target on the entire image plot
        rect = mp.patches.Rectangle((rminY, rminX), g_temp.shape[1],g_temp.shape[0], linewidth=2, edgecolor='g', facecolor="none")
        
        #Define the cropped image plot
        width = 30
        target_img = c_img[rminX-width:rminX+c_temp.shape[0]+width, rminY-width:rminY+c_temp.shape[1]+width]
        
        #Define the rectangle that surrounds the target on the cropped image plot
        temp_rect = mp.patches.Rectangle((width, width), g_temp.shape[1],g_temp.shape[0], linewidth=4, edgecolor='g', facecolor="none")
        
        #Print The location of the target
        print(f"The center of the target image in the input image is located at ({rminY+(c_temp.shape[1]/2)}, {rminX+(c_temp.shape[0]/2)})")
 
    elif method == 'ncc':

        #Use the function to get the output matrix after SSD is applied
        r = NCC.calculate_matrix(g_img, g_temp)
        
        #Find the maximum point (which is the closest match identified by NCC)
        rmax, rmaxX, rmaxY = maxMatrixVals(r)           
        
        #Define the rectangle that surrounds the target on the entire image plot
        rect = mp.patches.Rectangle((rmaxY, rmaxX), g_temp.shape[1],g_temp.shape[0], linewidth=2, edgecolor='g', facecolor="none")
        
        #Define the cropped image plot
        width = 30
        target_img = c_img[rmaxX-width:rmaxX+c_temp.shape[0]+width, rmaxY-width:rmaxY+c_temp.shape[1]+width]
        
        #Define the rectangle that surrounds the target on the cropped image plot
        temp_rect = mp.patches.Rectangle((width, width), g_temp.shape[1],g_temp.shape[0], linewidth=4, edgecolor='g', facecolor="none")
   
        #Print The location of the target
        print(f"The center of the target image in the input image is located at ({rmaxY+(c_temp.shape[1]/2)}, {rmaxX+(c_temp.shape[0]/2)})")
 
    elif method == 'cc':
        #Use the function to get the output matrix after SSD is applied
        r = CC.calculate_matrix(g_img, g_temp)
        
        #Find the maximum point (which is the closest match identified by NCC)
        rmax, rmaxX, rmaxY = maxMatrixVals(r)           
        
        #Define the rectangle that surrounds the target on the entire image plot
        rect = mp.patches.Rectangle((rmaxY, rmaxX), g_temp.shape[1],g_temp.shape[0], linewidth=2, edgecolor='g', facecolor="none")
        
        #Define the cropped image plot
        width = 30
        target_img = c_img[rmaxX-width:rmaxX+c_temp.shape[0]+width, rmaxY-width:rmaxY+c_temp.shape[1]+width]
        
        #Define the rectangle that surrounds the target on the cropped image plot
        temp_rect = mp.patches.Rectangle((width, width), g_temp.shape[1],g_temp.shape[0], linewidth=4, edgecolor='g', facecolor="none")
        
        #Print The location of the target
        print(f"The center of the target image in the input image is located at ({rmaxY+(c_temp.shape[1]/2)}, {rmaxX+(c_temp.shape[0]/2)})")
 
    else:
        #Get the result matrix from each method to combine the results
        r1 = SSD.calculate_matrix(g_img, g_temp)
        r2_norm = NCC.calculate_matrix(g_img, g_temp)
        r3 = CC.calculate_matrix(g_img, g_temp)
        
        #Normalize the matrices that need to be (NCC is already normalized)
        r1_norm = 1-(r1-r1.mean())
        r3_norm = (r3-r3.mean())
        
        #Add all loops together to get a combined result
        r = r1_norm + r2_norm + r3_norm
        
        #Find the maximum in the combined result array which is your combined result
        maximum, rmaxX, rmaxY = maxMatrixVals(r)
        
        #Define the rectangle that surrounds the target on the entire image plot
        rect = mp.patches.Rectangle((rmaxY, rmaxX), g_temp.shape[1],g_temp.shape[0], linewidth=2, edgecolor='g', facecolor="none")
        
        #Define the cropped image plotal
        width = 30
        target_img = c_img[rmaxX-width:rmaxX+c_temp.shape[0]+width, rmaxY-width:rmaxY+c_temp.shape[1]+width]
        
        #Define the rectangle that surrounds the target on the cropped image plot
        temp_rect = mp.patches.Rectangle((width, width), g_temp.shape[1],g_temp.shape[0], linewidth=4, edgecolor='g', facecolor="none")
        
        #Print The location of the target
        print(f"The center of the target image in the input image is located at ({rmaxY+(c_temp.shape[1]/2)}, {rmaxX+(c_temp.shape[0]/2)})")
    
    #End measuring time
    total_time = time.time() - start
    print(f"The function took {total_time} seconds to run")

    #Plot the r output matrix
    mp.pyplot.imshow(r, cmap='gray')
    mp.pyplot.show()

    #Plot the whole image with the box around the figure
    mp.pyplot.imshow(c_img)
    mp.pyplot.gca().add_patch(rect)
    mp.pyplot.show()
    
    #Plot the cropped image plot with the box around the target
    mp.pyplot.gca().add_patch(temp_rect)
    mp.pyplot.imshow(target_img)
    
   
        
if __name__ == '__main__':
    main()
