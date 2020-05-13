# Kaefer Problem. Kaefer will vom Grund auf Spitze eines Baumes erreichen
# Kaefer luft langsam, der Baum wächst gleichmässig verteilt über seine 
# gesamte Länge
import math
xx=[]
x=0
n=100
for ll in range(0,3) :

  xp=100.0
  dx=xp/n
  for i in range(0,n):
    x=x+dx
    xx.append(x)

  dt=1
  vpeak=0.2/dt
  if ll == 0 :
    dtb=0.5
    dtk=0.5
    vpeak=0.2/dtb
    vk=0.1/dtk
    xk=0
    k=0
    ns=20
    while (xk < xp) :
      k=k+1
      dtbs=dtb/ns
      for i in range(0,ns):
# 20 Integration steps   mitfahrender ruhender Käfer 1/2 Tag
        vb=xk/xp*vpeak
        xk=xk+vb*dtbs
        xp=xp+vpeak*dtbs
#        print (i,dtbs,vb,xk,xp)
#  Baum steht in der Nacht still und nur der Käfer läuft 1/2 Tag
      vka=vk
      xk=xk+vka*dtk
      dt=dtb+dtk
    print (("mode %5.0f Tage %5.0f xk %6.2f  xp %6.2f")%(ll,k,xk,xp))
  if ll == 1 :
    dtb=1
    dtk=0.5
    vpeak=0.2/dtb
    vk0=0.1/dtk
    xk=0
    k=0
    ns1=20
    ns=2*ns1
    while (xk < xp) :
      k=k+1
      dtbs=dtb/ns
      ts=0
      for i in range(0,ns1):
# ns1 Integration steps mitfahrender Käfer, Käfer ruht
        ts=ts+dtbs 
        vk=0
        vb=xk/xp*vpeak
        xk=xk+(vk+vb)*dtbs
        xp=xp+vpeak*dtbs
      for i in range(0,ns1):
# ns1 Integration steps mitfahrender und laufender Käfer
        ts=ts+dtbs 
        vk=vk0
        vb=xk/xp*vpeak
        xk=xk+(vk+vb)*dtbs
        xp=xp+vpeak*dtbs
#        print (i,ts,vk,xk)
    print (("mode %5.0f Tage %5.0f xk %6.2f  xp %6.2f")%(ll,k,xk,xp))
  if ll == 2 :
    dtb=1
    dtk=1
    vpeak=0.2/dtb
    vk0=0.1/dtk
    xk=0
    k=0
    ns=20
    while (xk < xp) :
      k=k+1
      dtbs=dtb/ns
      ts=0
      for i in range(0,ns):
# ns Integration steps mitfahrender und laufender Käfer.
        ts=ts+dtbs 
        vk=vk0
        vb=xk/xp*vpeak
        xk=xk+(vk+vb)*dtbs
        xp=xp+vpeak*dtbs
#        print (i,ts,vk,xk)
  
    print (("mode %5.0f Tage %5.0f xk %6.2f  xp %6.2f")%(ll,k,xk,xp))


# analytische Lösung für den letzten Fall mode = 2

t=0
dt=0.01
vb=0.2
vk=0.1
l0=100.0
xp=l0
xk=0.0
while (xk < xp ) :

   xp=xp+dt*vb
   xk=xk+ xk*vb/(vb*t+l0)*dt+vk*dt
     
   t=t+dt

print  ( "numerische dgl",t,xk,xp)


t=0
dt=0.01

vb=0.2
vk=0.1
vk=0.2
l0=10.0
xp=l0
xk=0.0
while (xk < xp ) :

   xp=l0+vb*t
   xk=vk*math.log(1.0+vb/l0*t)*(l0/vb+t)
     
   t=t+dt

print  ( "analytische Lösung dgl",t,xk,xp)
