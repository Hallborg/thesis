#!/usr/bin/env python2

import matplotlib.pyplot as plt
import sys

xaxis = [1,2,3,4,5]
axis_holder = []
files = sys.argv[1:5]

x_axis = []
bm_y_axis = []
lxc_y_axis = []
doc_y_axis = []

axis_holder.append(x_axis)
axis_holder.append(bm_y_axis)
axis_holder.append(lxc_y_axis)
axis_holder.append(doc_y_axis)

for i in range(len(files)):
    f = open(files[i], "r")
    for row in f:
        axis_holder[i].append(float(row.split(" ")[1].replace("value=", "")))
    f.close()

print axis_holder

plt.plot(
    axis_holder[0],axis_holder[1],'r--',
    axis_holder[0],axis_holder[2],'b--',
    axis_holder[0],axis_holder[3],'g--'
    )
plt.ylabel('some numbers')
plt.xlabel('Time elapsed')
plt.show()
