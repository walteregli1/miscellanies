# look for a number 10 digits all digits are 
# used 0,1,2,3,4,5,6,7,8,9
# and in each position the number, counting from the start (left)  
# is a multiple of the digit at the position.
# 10 Zahl 
# python recursive script WE 22.March 2020
##########################################
z=['1','2','3','4','5','6','7','8','9']
zz=['1','2','3','4','5','6','7','8','9']

def ttt(n,z):
  if n < 10 :
#    print n,z[0:n]
    even=[1,3,5,7]
    odd=[0,2,4,6,8]
    lll=even
    if n % 2 == 1:
      lll=odd 
    for k in lll:
      s=''
      for i in range (0,n) :
          s=s+z[i]
      t=int(s)
#      print n,k,s
      if n ==9 and t % n ==0 :
          print "cool number ",t*10
      if t % n ==0 and z[n-1] not in z[0:n-1] or n==1 :
          ttt(n+1,z)  
      z[n-1]=zz[k]
  return
#------------------------------------------
# here we start the recursive procedure ttt
#------------------------------------------
n=1
ttt(n,z)
print "end search cool number"
