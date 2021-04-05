# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:48:28 2020

@author: subha

Generates a repeating tiling pattern
Outputs the pattern 

"""
import json
import matplotlib as plt
from matplotlib import pyplot
import numpy as np
import random
import time

colors_list = ['#000000', '#0074D9','#FF4136','#2ECC40','#FFDC00',
     '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']

COLORS = {}
for i in range(len(colors_list)):
    COLORS[i]=colors_list[i]


RGB_COLORS = {'#000000':(0,0,0),
              '#0074D9': (0, 116, 217),
              '#FF4136':(255, 65, 54),
              '#2ECC40':(46, 204, 64),
              '#FFDC00':(255, 220, 0),
              '#AAAAAA':(170, 170, 170),
              '#F012BE':(240, 18, 190),
              '#FF851B':(255, 133, 27),
              '#7FDBFF':(127, 219, 255),
              '#870C25':(135, 12, 37)}
'''
task = 6
training_directory = 'neurosymbolic-modules-master/ec/data/ARC/data/training'

with open(training_directory+'/'+tasks_to_json[task]) as f:
      data = json.load(f)
      training = data['train'][0]
      training_input = training['input'] #should give 3 different grids
      training_output = training['output'] # same here
      testing = data['test'][0]
      testing_input = testing['input']
      
      output_ = np.asarray(data['test'][0]['output'])
'''

def output_grid_image(array,file_name = None):
    #function either shows the plot of an array, or saves 
    #a grid with a filename
    rgb_list = []
    for i in range(np.shape(array)[0]):
        mini = []
        for j in range(np.shape(array)[1]):
            mini.append(RGB_COLORS[COLORS[array[i][j]]])
        rgb_list.append(mini)
    fig = pyplot.imshow(rgb_list)
    if file_name is not None:
        pyplot.savefig(file_name, bbox_inches='tight')

def save_grid_jpg_json(filename, jpg_path,json_path,input_,output_):
    #takes filename and paths to save jpg/json to
    # in addition to the input output grid themselves.
    #jpg/json path must be followed by /
    i_o = {}
    i_o['input'] = input_.tolist()
    i_o['output'] = output_.tolist()
    with open(f'{json_path}{filename}.json','w') as outfile:
        json.dump(i_o,outfile)
    output_grid_image(input_,f'{jpg_path}{filename}_input.jpg')
    output_grid_image(output_,f'{jpg_path}{filename}_output.jpg')
    
    

#CREATING GRID/PLOTTING POINTS FUNCTIONS
def make_grid(row,col,background_color=0):
    #makes a grid with a certain color
    return np.full((row,col), fill_value=background_color)

def make_square_grid(n,color = 0):
    return make_grid(n,n,color)
    

def least_common_color(array):
    #returns least common color in an array
    occurences = [0 for _ in range(len(COLORS))]
    for row in array:
        for pixel in row:
            occurences[int(pixel)]+=1
    minimum = float('inf')
    min_ind = []
    for index in range(1,len(occurences)): #no 0 index to avoid black
        if occurences[index]<minimum:
            min_ind = [index]
            minimum = occurences[index]
        if occurences[index]==minimum:
            min_ind.append(index) #will give us all indices with min occurences
    return random.choice(min_ind) #pick a random one of them
            
def make_same_grid(array,color=None):
    #returns a grid where every element of array that was black is the new color
    #all other elements of array stay the same
    #makes every pixel the input color or the least common color in the input grid
    shape = np.shape(array)
    if color is None:
        color = least_common_color(array)
    new_grid = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if array[i,j]==0:
                new_grid[i,j]=color
            else: new_grid[i,j]=array[i,j]        
    return new_grid



def plot_n_points(array,n):
    # plots n random points of random color on grid
    #only plots in upper left quadrant, mutates original array, no return
    shape = np.shape(array)
    plotted = set()
    k = 0
    while k<n:
        i = random.randint(0,shape[0]//2)
        j = random.randint(0,shape[1]//2)
        if (i,j) not in plotted:
            array[i][j] = random.randint(0,9) #give it a random color
            plotted.add((i,j))
            k+=1
    return plotted

def pixel_in_quadrant(array,quadrant):
    # returns a random pixel thats in the quadrant
    shape = np.shape(array)
    if quadrant==1 or quadrant==3:
        i = random.randint(0,shape[0]//2)
    else: 
        i = random.randint(shape[0]//2+1,shape[0]-1)
    if quadrant==1 or quadrant==2:
        j = random.randint(0,shape[1]//2)
    else: 
        j = random.randint(shape[1]//2+1,shape[1]-1)
    return (i,j)

def plot_block_points(array,n,quadrant=1,color=random.randint(1,len(COLORS)-1)):
    #plots a block of points in a certain quadrant with random color
    #block is defined so that no point in the block is more than sqrt(n)
    #from any other point, where n is number of points in the block
    #also, each point must share an edge with another point in the block
    shape = np.shape(array)
    plotted = set()
    def distance(point1,point2):
        return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**(0.5)
    def touching(point1,point2):
        (i,j) = point1
        x = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        return point2 in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    k = 0
    while k<n:
        new_pixel = pixel_in_quadrant(array,quadrant)
        (i,j)=new_pixel
        touch= False
        for plot in plotted:
            if distance(new_pixel,plot)>n**0.5:
                break
        else:
                array[i,j] = color
                plotted.add(new_pixel)
                k+=1

def overlay(arr1,function):
    '''
    Overlays matrix 1 and matrix 2 together, where matrix 2 is the function applied on matrix1
    If both matrix 1 and 2 have non zero values at a certain location,
    this function takes the value of matrix2. Hopefully, this case wont be relevant
    Also assumes that applying the function maintains arr1s shape
    '''
    arr2 = function(arr1)
    shape = np.shape(arr1)
    new_arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if arr2[i][j]!=0:
                new_arr[i][j]=arr2[i][j]
            else: new_arr[i][j]=arr1[i][j]
    return new_arr
  
#TRANSFORM FUNCTIONS
def rotate_90_CCW(array): 
    #NOTE DOES NOT WORK FOR 1D ARRAYS
    return np.rot90(array)

def rotate_180_CCW(array):
    #does not mutate original array
    return np.rot90(rotate_90_CCW(array))

def rotate_90_CW(array):
    #this is inefficient but it gets the job done
    return np.rot90(rotate_180_CCW(array))

def flip_down_diagonal(array):
    #does not mutate original array
    return np.rot90(np.fliplr(array))

def flip_up_diagonal(array):
    #flips it across the upwards diagonal
    #eg from bottom left corner to top right corner 
    return rotate_90_CW(np.fliplr(array))

def flip_horizontal(array):
    return np.flipud(array)#, np.shape(array)[0]//1)

def flip_vertical(array):
    return np.fliplr(array)


    

#Mirroring functions
# these take the input array and overlay it with transform(array)
    #where transform is one of the functions defined above
def mirror_down_diagonal(array):
    return overlay(array,flip_down_diagonal)

def mirror_up_diagonal(array):
    return overlay(array,flip_up_diagonal)

def mirror_horizontal(array):
    return overlay(array,flip_horizontal)

def mirror_vertical(array):
    return overlay(array,flip_vertical)

def mirror_90_CCW(array):
    return overlay(array,rotate_90_CCW)

def mirror_180_CCW(array):
    return overlay(array,rotate_180_CCW)

def mirror_90_CW(array):
    return overlay(array,rotate_90_CW)

def mirror_cascade(mirrors):
    """
    Given a list of mirrors (implemented as mirrors on grids), returns a new
    single mirror such that applying that mirror to a grid produces the same
    output as applying each of the individual ones in turn.
    """
    def cascade(grid):
        result = np.copy(grid)
        for mirror in mirrors:
            result = mirror(result)
        return result
    return cascade

MIRRORS = [mirror_down_diagonal, mirror_up_diagonal,#,
           mirror_horizontal, mirror_vertical]#,
           #mirror_180_CCW,mirror_90_CCW, mirror_90_CW]

def run_n_mirrors(array,n, fill_in = False):
    #this method is a little bit bad bc sometimes two filters applied consecutively negate each other
    #shouldnt matter though, method doesnt have to be very efficient
    #essentially just runs n mirrors on an array, a good n is probably like n=20
    mirrors = []
    for i in range(n):
        mirrors.append(random.choice(MIRRORS))
    if fill_in:
        shape = np.shape(array)
        return overlay(mirror_cascade(mirrors)(array),make_same_grid)
    return mirror_cascade(mirrors)(array)

    
def check_symmetry(array):
    # checks if array has symmetry
    #must have all four types of symmetry (about horizontal, vertical, both diagonals)
    def all_transformed_grids(grid):
        for mirror in MIRRORS:
            yield mirror(grid)
    for grid in all_transformed_grids(array):
        if not np.array_equal(array,grid):
            return False
    return True

# OCCLUSION FUNCTIONS
def occlusion(array,size,color=0):
    #makes an occlusion on the array of a given size with the inputted color
    shape = np.shape(array)
    (width,height)=size
    def not_in_center(x,y,width,height,shape):
        #ensures that the occlusion doesnt take up the center pixel, bc u need the center pixel
        # to be showing
        center_x = shape[0]//2
        center_y = shape[1]//2
        if x<center_x<x+width and y<center_y<y+width:
            return False
        return True
    while True:
        x = random.randint(0,shape[0])
        y = random.randint(0,shape[1])
        if x+width<shape[0] and y+height<shape[1] and not_in_center(x,y,width,height,shape):
            return_array = np.zeros((width,height))
            for i in range(x,x+width):
                for j in range(y,y+height):
                    return_array[i-x,j-y] = array[i,j]
                    array[i,j]=color
            return return_array
    
def make_occlusions(array,color=0):
    #occludes out a max of 15% of image
    #creates a bunch of smaller occlusions
    shape = np.shape(array)
    max_number_occlusions = int(shape[0]*shape[1]*.15)
    iterations = 0
    while max_number_occlusions>=1:
        iterations+=1
        width = random.randint(1,min(shape[0]//3,max_number_occlusions))
        height = random.choice([h for h in range(width-2,width+3) if 0<=h<shape[1]])
        occlusion(array,(width,height),color)
        max_number_occlusions-=width*height
        if iterations==10:
            break
        


    
#CREATING A WHOLE UNIT PATTERN
#ALL OF THESE GRIDS SHARE SYMMETRY ABOUT HORIZONTAL, VERTICAL, AND BOTH DIAGONALS   
def generate_whole_pattern(n,sizes):
    #NOTE: CODE CANNOT HANDLE 2X2 CASE 
    #generates n number of blocks patterns
    #maps full grids with occlusions to their full grid if gen_occlusion
    #otherwise, maps full grid to the original occluded part
    for size in sizes:
        for _ in range(n):
            while True:
                new = make_square_grid(size) 
                plot_block_points(new,size) #plots down as many points as side length
                plot_n_points(new,size)
                #,'generated_tasks/task_109.jpg')
                result = run_n_mirrors(new,20,True)
                output= np.copy(result)
                if check_symmetry(result):
                    yield result
                    break


#CREATING REPEATED UNIT PATTERN
# ESSENTIALLY TESSELATES A BUNCH OF WHOLE UNIT PATTERNS
def tile(pattern,width,height):
    #given a pattern as a np array, tiles it onto a larger grid
    #tiles in width times in the x direction, and height times in the y direction
    pattern_list = pattern.tolist()
    pattern_list = [row*width for row in pattern_list]
    return_list = pattern_list.copy()
    for i in range(1,height):
        return_list+=pattern_list
    return subset_tile(np.asarray(return_list))

def subset_tile(tile):
    #sometimes we dont want to see the whole pattern, we only want a subgrid
    #this program finds the subgrid of any tile, makes it harder for the AI
    # to recognize patterns
    shape = np.shape(tile)
    width = random.choice(range(shape[0]-2,shape[0]+1))
    height = random.choice(range(shape[1]-2,shape[1]+1))
    return tile[:width,:height]

def generate_repeated_pattern(n,pieces):
    #generates n grids for each base pattern
    #pieces is a defunct argument that lets it keep the same form as generate_whole_pattern
    sizes = list(range(3,16))
    for pattern in generate_whole_pattern(n,sizes):
        shape = np.shape(pattern)
        width = random.randint(2,30//shape[0])
        height = random.randint(2,30//shape[1])
        yield pattern, tile(pattern,width,height)

    
#GENERATING THE OCCLUSION 
def generate_occlusion(n,function,pattern_type, gen_occlusion=False):
    # pattern type is probably either whole_patterns or repeated
    #if gen_occlusion is true, the output grid is just the occluded area filled
    #otherwise its the total grid with the occluded area filled

    i_o = {'train':[]}

    sizes = [3]+list(range(5,35,5)) #MAKES N GRIDS FOR EACH SIZE IN SIZES
    shape_count = {}
    for subpattern, pattern in function(n,sizes):
        shape = np.shape(pattern)
        random_int = random.randint(1,2)
        if random_int%2==0:
            color = least_common_color(pattern) #half in different color, half in black
        else: color = 0
        if shape in shape_count:
            shape_count[shape]+=1
        else: shape_count[shape]=1
        type_pattern = pattern_type[:pattern_type.index('_')] #ex diagonal/repeated/whole
        type_output = 'occlusion' if gen_occlusion else 'whole_grid'
        filename = f'{type_pattern}_{type_output}_{shape[0]}_{shape[1]}_{shape_count[shape]}'
        if gen_occlusion:
            input_ = np.copy(pattern)
            output_ =  np.zeros(shape=input_.shape)#occlusion(input_,closest_size(int(.15*shape[0]*shape[1])),color)
            output_[0:subpattern.shape[0], 0:subpattern.shape[1]] = subpattern

            jpg_dir = f'generated_tasks/{pattern_type}/occlusion_jpg/'
            json_dir = f'generated_tasks/{pattern_type}/occlusion_json/'


            i_o['train'].append({})
            i_o['train'][-1]['input'] = input_.tolist()
            i_o['train'][-1]['output'] = output_.tolist()

    #save_grid_jpg_json(filename,jpg_dir,json_dir,input_,output)

    with open(f'generated_tasks/repeated_100tasks.json','w') as outfile:
        json.dump(i_o,outfile)

if __name__ == '__main__':
    start = time.process_time()
    #running the folowing arguments should generate about 100 of each type
    #gives a total of 600 cases
    #its kind of slow though, dont be surprised if it takes 10 minutes to create 600 examples
    #also, occasionally it can run into a bug and just completely stop. in this case, its safest to
    #interrupt the program and start the run again
    arguments = [
                 [7,generate_repeated_pattern,'repeated_units',True]
                 ]
    for arg in arguments[:]:
        generate_occlusion(*arg)
    end = time.process_time()
    print(f'Elapsed time: {end-start}')
    
    #array = make_square_grid(15)
    #for _ in range(5):
    #    for i in range(1,9):
    #        add_diagonal(array,i)
    #output_grid_image(create_diagonal_grid(15))
    
    