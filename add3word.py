num='0123456789'
dd=[]
n=len(num)
for i in range(0,n):
  dd.append(num[i])
sst0=dd
w1='UHU'
w2='ENTE'
w3='STORCH'
w4='NISTEN'
ww=w1+w2+w3+w4
t=0
z4=1
bb='UHENTSORCI'
wwk=[]
aa=[]
for i in range(0,len(ww)):
   for k in range(0,len(bb)): 
       if ww[i] == bb[k] :
          wwk.append(k)
          aa.append(dd[k])

def checkFreunde(dd):
    for i in range(0,len(ww)):
           aa[i]=dd[wwk[i]]
    if aa[0] != '0'  and aa[3] != '0' and aa[7] != '0' and aa[13]!= '0': 
      z1=int(aa[0]+aa[1]+aa[2])
      z2=int(aa[3]+aa[4]+aa[5]+aa[6])
      z3=int(aa[7]+aa[8]+aa[9]+aa[10]+aa[11]+aa[12])
      z4=int(aa[13]+aa[14]+aa[15]+aa[16]+aa[17]+aa[18])

      t=z1+z2+z3
      if (t == z4)  :
         print ("weiter")
         print (z1,z2,z3,z4)
         print (ww)

def permutate ( left, right, sstp):
  if ( left == right):
#   print sstp
   checkFreunde(sstp)
  else:
    for i in range (left,right+1):
      wapped=swap(left,i,sstp)
      permutate (left+1,right,wapped[:])
def swap (i,k,str):
  ss=[]
  ss=str
  h=ss[i]
  ss[i]=ss[k]
  ss[k]=h
  return ss
   
permutate (0,n-1,dd)
