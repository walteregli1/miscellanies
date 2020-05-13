# 10 Zahl 
z=['1','2','3','4','5','6','7','8','9']
zz=['1','2','3','4','5','6','7','8','9']

even=[1,3,5,7]
# 5 ist immer am gleichen Ort
odd=[0,2,6,8]
i5=4

for i1 in odd :
  for i2 in even:
    t2=int(z[0]+z[1])
    if t2 %  2 == 0:
      for i3 in odd :
        t3=int(z[0]+z[1]+z[2])
        if t3 % 3 == 0 and z[2] not in z[0:2]:
          for i4 in even :
            t4=int(z[0]+z[1]+z[2]+z[3])
            if t4 % 4  == 0  and z[3] not in z[0:3]:
              for i6 in even :
                t6=int(z[0]+z[1]+z[2]+z[3]+z[4]+z[5])
                if t6 % 6 == 0 and z[5] not in z[0:5]:
                  for i7 in odd :
                   t7=int(z[0]+z[1]+z[2]+z[3]+z[4]+z[5]+z[6])
                   if t7 % 7 == 0 and z[6] not in z[0:6]:
                    for i8 in  even:
                     t8=int(z[0]+z[1]+z[2]+z[3]+z[4]+z[5]+z[6]+z[7])
                     if t8 % 8 == 0 and z[7] not in z[0:7]:
                       for i9 in odd :
                         t9=int(z[0]+z[1]+z[2]+z[3]+z[4]+z[5]+z[6]+z[7]+z[8])
                         if t9 %9 == 0 and z[8] not in z[0:8]:
                           print 'ok',t9
                         z[8]=zz[i9]
                     z[7]=zz[i8]
                   z[6]=zz[i7]
                z[5]=zz[i6]
            z[3]=zz[i4]
        z[2]=zz[i3]
    z[1]=zz[i2]
  z[0]=zz[i1]
print "end"
