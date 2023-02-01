import os
hostname = input("Please enter IP in XXX.XXX.XXX. format: ") 

for ip in range(0,151):
    newhost = hostname + str(ip)
    response = os.system("ping -c 1 -w 1 " + newhost)

    if response ==0 :
        print(newhost, 'is up')
    else:
        print(newhost, 'is down')