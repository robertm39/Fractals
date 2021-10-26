# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:00:21 2021

@author: rober
"""

import numpy as np

from IPython.display import display

from PIL import Image

class RegionBounds:
    def __init__(self, min_x, max_x, min_y, max_y, image=None):
        self.min_x = min_x
        self.max_x = max_x
        
        self.min_y = min_y
        self.max_y = max_y
        
        self.x_diff = max_x - min_x
        self.y_diff = max_y - min_y
        
        self.image = image
    
    def coords_in_graph(self, ix, iy, image=None):
        if image is None:
            image = self.image
        
        width, height = image.size
        
        x_disp = self.x_diff / (width - 1)
        y_disp = self.y_diff / (height - 1)
        
        return self.min_x + x_disp * ix, self.min_y + y_disp * iy
    
    def coords_in_image(self, x, y, image=None):
        if image is None:
            image = self.image
        
        width, height = image.size
        
        x_disp = self.x_diff / (width - 1)
        y_disp = self.y_diff / (height - 1)
        
        ix = round((x - self.min_x) / x_disp)
        iy = round((y - self.min_y) / y_disp)
        
        return ix, iy

def mandelbrot_proto():
    image_size = 600
    # Get a black image
    image = Image.new('RGB', (image_size, image_size), 'black')
    
    # Get the pixel map
    pixels = image.load()
    
    min_x = -1.5
    max_x = 0.5
    
    min_y = -1
    max_y = 1
    
    width, height = image.size
    max_iters = 129
    
    # x_disp = (max_x - min_x) / (width - 1)
    # y_disp = (max_y - min_y) / (height - 1)
    bounds = RegionBounds(min_x, max_x, min_y, max_y, image)
    
    for ix in range(width):
        if (ix + 1) % 10 == 0:
            print('processing column {}'.format(ix+1))
        
        for iy in range(height):
            # Get the complex number
            # x = min_x + ix * x_disp
            # y = min_y + iy * y_disp
            x, y = bounds.coords_in_graph(ix, iy)
            
            c = np.cdouble(x + y * 1.j)
            
            # Get the starting z value
            z = np.cdouble(0.0)
            
            diverges = False
            # Do the iterations
            for i in range(1, max_iters + 1):
                z = z*z + c
                
                # We got outside of the critical circle
                if np.linalg.norm(z) > 2:
                    diverges = True
                    break
        
            # Don't do fancy coloring for now
            if diverges:
                intensity = 255 - i + 1
                pixels[ix, iy] = (intensity, intensity, intensity)
            else:
                pixels[ix, iy] = (0, 0, 0)
    
    display(image)

def region_bounds_test():
    region_bounds = RegionBounds(-1, 1, -1, 1)
    image = Image.new('RGB', (200, 200), 'black')
    
    x, y = region_bounds.coords_in_graph(image, 100, 100)
    print(x, y)
    print(region_bounds.coords_in_image(image, x, y))

def main():
    mandelbrot_proto()
    # region_bounds_test()

if __name__ == '__main__':
    main()