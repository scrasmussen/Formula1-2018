import numpy as np

points = np.array([70,32,42,27,40,33,20,48,12,19,-13,22,1,21,17,13,26,14,-5,-14,
                   17,0,4,2,16,4,16,13,8,17], dtype=np.float)
cost = np.array([32,30.5,29,27.5,25,24.5,23.5,20.5,17.5,12.5,12,11.8,11,10,10,
                 9.7,9.5,9.5,9.3,7.7,7.7,7.4,6.9,6.8,6.2,6,6,6,5.5,5.5],
                 dtype=np.float)

ave = points / cost

name = ['c','d','c','d','c','d','d','d','d','c','d','d','d','d','d','c','c',
        'c','d','d','d','c','d','d','c','d','c','d','d','d']

z = list(zip(name,ave,)) #range(1,20)))
# for (n,a,i) in z:
#   if (n == 'c'):
#     print(i,n,a)
# print("-----")
# for (n,a,i) in z:
#   if (n != 'c'):
#     print(i,n,a)
# print(ave)
# print(z)
for i in z:
  if (i[0] == 'c'):
    print(i)
print('-------')
for i in z:
  if (i[0] == 'd'):
    print(i)
