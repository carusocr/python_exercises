'''Write a function in Python that takes a list as input and repeatedly appends the sum
of the last three elements of the list to the end of the list. 
Your function should loop for 25 times'''
lst = [0,1,2]
def sumlist(lst):
    for i in range(25):
        lst.append(lst[-1]+lst[-2]+lst[-3])

sumlist(lst)
print lst[20]

-135 75
