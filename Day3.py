#Creating list with values in 4 nearest neighbours to 1
d=[2,4,6, 8]
#Input number
num=368078
#Iniziating count to 3 since 4 number been created but counting starts in 0 for 2n+1 structure
count=3
#Iniziating steps which is in how many steps current calculated value has to 1
step=1

#Calculating new values until one value larger than num is created
while d[count%4]<=num:
    count=count+1
    #Calculating new number since the increase is 2*count+1+value at position in step before
    d[count%4]=d[count%4]+2*count+1
    #Adding step if a 4 cylce is completed
    if count%4==0:
        step=step+1
#Adding steps which would be needed to arrive to value that has "straight" line to 1. It selects the closest nukmber, either a larger or smaLler.
total_step=step+min(num-d[(count-1)%4], d[count%4]-num)
#Print how many steps needed
print(total_step)
