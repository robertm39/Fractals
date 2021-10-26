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
        
        return int(ix), int(iy)
    
    def in_image_bounds(self, ix, iy, image=None):
        if image is None:
            image = self.image
        
        if ix < 0 or iy < 0:
            return False
        
        width, height = image.size
        
        if ix >= width or iy >= height:
            return False
        
        return True

def square_norm(z):
    x, y = np.real(z), np.imag(z)
    return x*x + y*y

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
    
    bounds = RegionBounds(min_x, max_x, min_y, max_y, image)
    
    num_times = 0
    
    for ix in range(width):
        if (ix + 1) % 50 == 0:
            print('processing column {}'.format(ix+1))
        
        for iy in range(height):
            # Get the complex number
            x, y = bounds.coords_in_graph(ix, iy)
            
            c = np.cdouble(x + y * 1.j)
            
            # Get the starting z value
            z = np.cdouble(0.0)
            
            diverges = False
            # Do the iterations
            for i in range(1, max_iters + 1):
                z = z*z + c
                num_times += 1
                
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
    
    print('times: {}'.format(num_times))
    display(image)

def mandelbrot_light_side():
    """
    Make the "light side" image.
    """
    image_size = 600
    # Get a black image
    image = Image.new('RGB', (image_size, image_size), 'black')
    
    # Get the pixel map
    pixels = image.load()
    
    min_x = -2
    max_x = 2
    
    min_y = -2
    max_y = 2
    
    width, height = image.size
    max_iters = 200
    
    bounds = RegionBounds(min_x, max_x, min_y, max_y, image)
    
    # Keep track of how many times each coordinate is hit
    times_hit = np.zeros((image_size, image_size), dtype=np.int32)
    
    times = 0
    
    for ix in range(width):
        if (ix + 1) % 50 == 0:
            print('processing column {}'.format(ix+1))
        
        for iy in range(height):
            x, y = bounds.coords_in_graph(ix, iy)
            
            c = np.cdouble(x + y * 1.j)
            
            # Get the starting z value
            z = np.cdouble(0.0)
            
            diverges = False
            values = list()
            # Do the iterations
            for i in range(1, max_iters + 1):
                z = z*z + c
                # crit_1 = np.linalg.norm(z) > 2
                
                # prev = z.copy()
                values.append(z)
                # assert prev == z
                
                # crit_2 = np.linalg.norm(z) > 2
                
                # assert crit_1 == crit_2
                
                times += 1
                
                # We got outside of the critical circle
                # if np.linalg.norm(z) > 2:
                if square_norm(z) > 4:
                    diverges = True
                    break
            
            if diverges:
                for value in values:
                    x, y = np.real(value), np.imag(value)
                    ixv, iyv = bounds.coords_in_image(x, y)
                    if bounds.in_image_bounds(ixv, iyv):
                        times_hit[ixv, iyv] += 1
    
    # Put the values from times_hit into the image
    
    
    print('times: {}'.format(times))
    
    max_hit = np.amax(times_hit)
    for ix in range(width):
        for iy in range(height):
            intensity = times_hit[ix, iy] / max_hit
            intensity = int(round(intensity * 255))
            
            pixels[ix, iy] = (intensity, intensity, intensity)
    
    display(image)

def region_bounds_test():
    region_bounds = RegionBounds(-1, 1, -1, 1)
    image = Image.new('RGB', (200, 200), 'black')
    
    x, y = region_bounds.coords_in_graph(image, 100, 100)
    print(x, y)
    print(region_bounds.coords_in_image(image, x, y))

def main():
    # mandelbrot_proto()
    mandelbrot_light_side()
    # region_bounds_test()

if __name__ == '__main__':
    main()