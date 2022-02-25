import math
import random
def shuffle_array(array):
    array2=[]
    while len(array2)<len(array):
        i=random.random()
        i=i*len(array)
        i=math.floor(i)
        i=array[i]
        if i in array2:
            pass
        else:
            array2.append(i)
    return array2
    