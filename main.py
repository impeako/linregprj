import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# import dataset
def import_dataset(path="heart.data", index_col=[0]):
    if os.path.exists("heart.data"):
        print("Dataset: {}\nFound: Locally".format(path))
        try:
            df = pd.read_csv(path, header=0, engine='python', index_col=[0])
        except IndexError as ind:
            print(ind)
            print("Index provided: {}".format(index_col))
            exit()
        except:
            print("Failed to parse data set...")
            raise
    else:
        print("Dataset not found locally.\nDownloading dataset...")
        try:
            df = pd.read_csv(path)
        except:
            exit("Not a valid dataset URL")

        with open(path, 'w') as local_file:
            print("Saving dataset locally")
            df.to_csv(local_file, index=False)
    return df

# split into x and y type array
def split_x_y(df, x, y):
    array_x = np.array(df[x])
    array_y = np.array(df[y])
    return array_x, array_y

# data split train_test function
def split_train_test(array_x,array_y):
    matrice = np.empty()
    for i in range(len(array_x)):
        matrice = np.append(matrice, [array_x[i], array_y[i]])
    print(matrice)

# training the data
def reglintrain(arrayX, arrayY):
    # creating two copies of the arrays which they are going to contain the middle points of the couples
    midarrayX = arrayX
    midarrayY = arrayY
    # n is going be the number of points each time
    n = len(arrayX)
    for i in range(0, n, 2):
        # appending middle points to the mid-array in each loop
        mid_arrayX = np.insert(mid_arrayX, 0, (mid_arrayX[i]+mid_arrayX[i+1])/2)
        mid_arrayY = np.insert(mid_arrayY, 0, (mid_arrayY[i]+mid_arrayY[i+1])/2)
        if i == n-1 and n > 1:
            i = 0
            # if we have an even number of points we can couple all of them
            if (n % 2) == 0:
                n = n//2
            # if we have an odd number of points we have to couple the last point with the point right before it so we create a new point named n which equals to point n-2
            else:
                n = (n+1)//2
                # adding the point
                mid_arrayX[n] = mid_arrayX[n-2]
                mid_arrayY[n] = mid_arrayY[n-2]
    # the two points that the lane is going to be built on
    # final point 1
    fp1 = [mid_arrayX[0], mid_arrayY[0]]
    # final point 2
    fp2 = [mid_arrayX[1], mid_arrayY[1]]
    # calculate the slope of the line
    a = (fp2[1]-fp1[1])/(fp2[0]-fp1[0])
    # then we calculate the coef of x
    b = (a*fp1[0])-fp1[1]
    # returning a list containing a and b in the order
    final_list = [a, b]
    return final_list

# returning the predicted result
def pred(x, flist):
    return (x*flist[0])+flist[1]

df = import_dataset("bd.csv")
arrayx, arrayy = split_x_y(df, "x", "y")
split_train_test(arrayx, arrayy)
