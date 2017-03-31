import sys


# input - $1: How much to increment in each iteration
# input - $2: How many iterations will there be
# output - : number of objects needed to be created
inc = int(sys.argv[1])
total = 0
for i in range(int(sys.argv[2])):
    total +=  inc * (i + 1)

# * nr of threads!
print total *4 
