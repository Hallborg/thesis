import sys
f1 = open("Thread-1")
f2 = open("Thread-2")
f3 = open("Thread-3")
f4 = open("Thread-4")
f = open(sys.argv[1], 'w')
write = 0
read = 0
update = 0
delete = 0
for r1, r2, r3, r4 in f1, f2, f3, f4:
    write += int(r1.rstrip())
    read += int(r2.rstrip())
    update += int(r3.rstrip())
    delete += int(r4.rstrip())
    #th1.append(int(r.rstrip()))
f.write(str(write) + ", ")
f.write(str(read) + ", ")
f.write(str(update) + ", ")
f.write(str(delete) + "\n")
f.close()
