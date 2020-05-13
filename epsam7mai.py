#***************************************************************
# planets, moon and sun postions 
# sunrise and sunset according the zero af altitude +daltof  = 0
# moonrise and moonst
# moon declinaton path: zunehmende oder absteigende Kulminationshöhe
#                       Obsigaent oder Nidsigaent
# sun light frame on the moon 
#
#  by using markup.py building a html page
#  crontab applied to create an actuel page 
#  matplotlib local instaled on hostpoint
#  EGW Walter Egli  5.Mai 2029
# planets date from 
# 'How to compute planetary positions, by Paul Schlyter, Stockholm, Sweden
#***************************************************************
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import markup
local_longitude = 8.8544  # Baeretswil 
local_b         =47.3386
#local_longitude = 8.5392  # Zuerich 
#local_b         =47.36865
#local_longitude = 8.672  # Andelfingen 
#local_b         =47.601
daltof=0.833
pi=math.pi
def sind(x):
   return math.sin(x*pi/180.0)
def cosd(x):
   return math.cos(x*pi/180.0)
def sqrt(x):
   return math.sqrt(x)
def atan2(x,y):
   return math.atan2(x,y)*180.0/pi
def convhm(x):
   xp=x
   if x <0.0 :
     xp=x+24.0
   a=math.floor(xp)
   b=(xp-math.floor(xp))*60
   return (a,b)    

def zeithms(UTp) :
  UT=UTp 
  if UT < 0.0 :
      UT=UT+24.0 
  zeith=int(UT) % 24
  zeitm=(UT-int(UT))*60.0
  zeits=(zeitm-int(zeitm))*60.0
  strxt=" "
  if zeith<10 :
     strxt=strxt+"0"
  strxt=strxt+str(zeith)+":"
  if int(zeitm)<10 :
     strxt=strxt+"0"
  strxt=strxt+str(int(zeitm))+":"
  if int(zeits)<10 :
     strxt=strxt+"0"
  strxt=strxt+str(int(zeits))

  return strxt

def convdeg(x):
   a=math.floor(x)
   b=(x-math.floor(x))*60
   return (a,b)    

# Day 0.0 occurs at 2000 Jan 0.0 UT (or 1999 Dec 31, 0:00 UT). This "day number" d is computed as follows (y=year, m=month, D=date, UT=UT in hours+decimals):*/

def day (y,m,D,UT):
 
    d = 367*y - 7 * ( y + (m+9) // 12 ) // 4 + 275*m//9 + D - 730530
    d = d + UT/24.0  
    return d

def ecli (d):
    ecl = 23.4393 - 3.563E-7 * d
    return ecl

def kepler(e,M) :
    E1=e*180/pi
    E=0.0
    while (abs(E-E1)>1.0e-06) :
      E=E1
      E1=E-(E-e*180.0/pi*sind(E)-M)/(1-e*cosd(E))
    return E1   
def planet_pos(name,d,UT):
    ecl=ecli(d)
    Longcor=0
    Altcor=0
    Rcor=0
    (lonsun,LST,rsun,xsun,ysun,zsun,xesun,yesun,zesun,RAsun,Decsun) = sunpos(d,UT)
    if name =="jupiter" :
       (N,i,w,a,e,Ms)= orbsaturn(d)
       (N,i,w,a,e,Mj)= orbjupiter(d)
       M=Mj
       Longcor=-0.332 * sind(2*Mj - 5*Ms - 67.6 ) + (
       -0.056 * sind(2*Mj - 2*Ms + 21 )
       +0.042 * sind(3*Mj - 5*Ms + 21 )
       -0.036 * sind(Mj - 2*Ms)
       +0.022 * cosd(Mj - Ms)
       +0.023 * sind(2*Mj - 3*Ms + 52 )
       -0.016 * sind(Mj - 5*Ms - 69 ) )
    if name =="saturn" :
       (N,i,w,a,e,Mj)= orbjupiter(d)
       (N,i,w,a,e,Ms)= orbsaturn(d)
       M=Ms

       Longcor=+0.812 * sind(2*Mj - 5*Ms - 67.6 ) + ( 
       -0.229 * cosd(2*Mj - 4*Ms - 2 )          
       +0.119 * sind(Mj - 2*Ms - 3 )           
       +0.046 * sind(2*Mj - 6*Ms - 69 )        
       +0.014 * sind(Mj - 3*Ms + 32 )         )

       Altcor=-0.020 * cosd(2*Mj - 4*Ms - 2 )+ (
       +0.018 * sind(2*Mj - 6*Ms - 49 ) )
       
    if name =="mond" :
       (N,i,w,a,e,M)= orbmoon(d)
       wm=w
       Mm=M
       Nm=N
       (Nsun,isun,ws,asun,esun,Ms)=orbsun(d)
       Ls = Ms + ws
       Lm = Mm + wm + Nm
       D = Lm - Ls       # Mean elongation of the Moon
       F = Lm - Nm       # Argument of latitude for the Moon
       F = scF360(F)
       D = scF360(D)
       Lm= scF360(Lm)
       Ls= scF360(Ls)
# Korrekturen
#Add these terms to the Moon's longitude (degrees):
       Longcor= -1.274 * sind(Mm - 2*D) + (       
        +0.658 * sind(2*D)               
        -0.186 * sind(Ms)               
        -0.059 * sind(2*Mm - 2*D)       
        -0.057 * sind(Mm - 2*D + Ms)   
        +0.053 * sind(Mm + 2*D)        
        +0.046 * sind(2*D - Ms)       
        +0.041 * sind(Mm - Ms)        
        -0.035 * sind(D)               
        -0.031 * sind(Mm + Ms)        
        -0.015 * sind(2*F - 2*D)     
        +0.011 * sind(Mm - 4*D)   )
#Add these terms to the Moon's latitude (degrees):
       Altcor=-0.173 * sind(F - 2*D) + ( 
        -0.055 * sind(Mm - F - 2*D)  
        -0.046 * sind(Mm + F - 2*D)  
        +0.033 * sind(F + 2*D)      
        +0.017 * sind(2*Mm + F)    )

#Add these terms to the Moon's distance (Earth radii):
       Rcor=-0.58 * cosd(Mm - 2*D) + (
       -0.46 * cosd(2*D) )
 
    if name =="mars" :
       (N,i,w,a,e,M)= orbmars(d)
    if name =="venus" :
       (N,i,w,a,e,M)= orbvenus(d)
    if name =="merkur" :
       (N,i,w,a,e,M)= orbmercury(d)
    E=kepler(e,M)
# Now compute the planet's distance and true anomaly:
#    xv = r * cosd(v) = a * ( cosd(E) - e )
#    yv = r * sind(v) = a * ( sqrt(1.0 - e*e) * sind(E) )
    xv =  a * ( cosd(E) - e )
    yv =  a * ( sqrt(1.0 - e*e) * sind(E) )

    v = atan2( yv, xv )
    r = sqrt( xv*xv + yv*yv )
# Compute the planet's position in 3-dimensional space:
    xh = r * ( cosd(N) * cosd(v+w) - sind(N) * sind(v+w) * cosd(i) )
    yh = r * ( sind(N) * cosd(v+w) + cosd(N) * sind(v+w) * cosd(i) )
    zh = r * ( sind(v+w) * sind(i) )
    long = atan2(yh,xh)
    lat  = atan2(zh, math.sqrt(xh*xh+yh*yh))
    r    = math.sqrt ( xh*xh+yh*yh+zh*zh)
    long = long + Longcor
    lat  = lat +Altcor
    r    = r + Rcor
#    print "longcor",Longcor, long,name
#    print "altcor",Altcor,lat,name
#    print "rcor ",Rcor,r,name
# If we are computing the Moon's position, this is already the geocentric position, and thus we simply set xg=xh, yg=yh, zg=zh. Otherwise we must also compute the Sun's position: convert lonsun, rs (where rs is the r computed here) to xs, ys:
# (Of course, any correction for precession should be added to lonecl and lonsun before converting to xh,yh,zh and xs,ys).
    xg=r*cosd(long)*cosd(lat)
    yg=r*sind(long)*cosd(lat)
    zg=r*sind(lat)
    if name != "mond" :
# Now convert from heliocentric to geocentric position:
       xg = xh + xsun
       yg = yh + ysun
       zg = zh
  
#    print name, 'longitude ',long, ' altidude ', lat
# We now have the planet's geocentric (Earth centered) position in rectangular, ecliptic coordinates.

# 12. Equatorial coordinates
# Let's convert our rectangular, ecliptic coordinates to rectangular, equatorial coordinates: simply rotate the y-z-plane by ecl, the angle of the obliquity of the ecliptic:
    xe = xg
    ye = yg * cosd(ecl) - zg * sind(ecl)
    ze = yg * sind(ecl) + zg * cosd(ecl)
# Finally, compute the planet's Right Ascension (RA) and Declination (Dec):
    RA  = atan2( ye, xe )*12.0/180.0
    Dec = atan2( ze, math.sqrt(xe*xe+ye*ye) )
# Compute the geocentric distance:
#    rg = sqrt(xg*xg+yg*yg+zg*zg) = sqrt(xe*xe+ye*ye+ze*ze)
    rg = sqrt(xg*xg+yg*yg+zg*zg) 
# Thie completes our computation of the equatorial coordinates

    return (LST,r,RA, Dec)
def sunpos (d,UT):
# The position of the Sun
    ecl=ecli(d)
    (N,i,w,a,e,M)=orbsun(d)
    E = M + e*180.0/pi * sind(M) * ( 1.0 + e * cosd(M) )
#   print "E, kepler(e,M)",E,kepler(e,M)
# Note that the formulae for computing E are not exact; however they're accurate enough here.

# Then compute the Sun's distance r and its true anomaly v from:
#    xv = r * cosd(v) = cosd(E) - e
#    yv = r * sind(v) = sqrt(1.0 - e*e) * sind(E)
    xv = cosd(E) - e
    yv = math.sqrt(1.0 - e*e) * sind(E)

    v = atan2( yv, xv )
    r = math.sqrt( xv*xv + yv*yv )
#   atan2( y, x ) = atan(y/x)                 if x positive
#    atan2( y, x ) = atan(y/x) +- 180 degrees  if x negative
#    atan2( y, x ) = sign(y) * 90 degrees      if x zero

    lonsun = v + w

# Convert lonsun,r to ecliptic rectangular geocentric coordinates xs,ys:
    xs = r * cosd(lonsun)
    ys = r * sind(lonsun)
    zs = 0.0
# (sindce the Sun always is in the ecliptic plane, zs is of course zero). xs,ys is the Sun's position in a coordinate system in the plane of the ecliptic. To convert this to equatorial, rectangular, geocentric coordinates, compute:
    xe = xs
    ye = ys * cosd(ecl)
    ze = ys * sind(ecl)
# Finally, compute the Sun's Right Ascension (RA) and Declination (Dec):
    RA  = atan2( ye, xe )*12.0/180.0
    Dec = atan2( ze, math.sqrt(xe*xe+ye*ye) )
#    print "sun : RA /h Dec /deg",RA,Dec
#  Quite often we need a quantity called Sidereal Time. The Local Sideral Time (LST) is simply the RA of your local meridian. The Greenwich Mean Sideral Time (GMST) is the LST at Greenwich. And, finally, the Greenwich Mean Sidereal Time at 0h UT (GMST0) is, as the name says, the GMST at Greenwich Midnight. However, we will here extend the concept of GMST0 a bit, by letting "our" GMST0 be the same as the conventional GMST0 at UT midnight but also let GMST0 be defined at any other time such that GMST0 will increase by 3m51s every 24 hours. Then this formula will be valid at any time:

# We also need the Sun's mean longitude, Ls, which can be computed from the Sun's M and w as follows:
    Ls = M + w
    Ls=scF360(Ls)
    
# The GMST0 is easily computed from Ls (divide by 15 if you want GMST0 in hours rather than degrees), GMST is then computed by adding the UT, and finally the LST is computed by adding your local longitude (east longitude is positive, west negative).
    GMST0 = Ls/15 +12   # (Ls + 180)/15.0  #  = Ls/15 + 12_hours
    GMST = GMST0 + UT
    LST  = GMST + local_longitude/15
#    print "GMST und LST" ,GMST,LST,Ls,M,w
    return (lonsun,LST,r,xs,ys,zs,xe,ye,ze,RA,Dec)


def scF360(x) :
  
  if x > 360.0 :
     y = x-(x // 360) * 360.0
  else:
    if x < -360.0 :
       y= x+(-x // 360) * 360.0
    else :
       y=x
  if y < 0.0  :
    y=y+360.0
  return y

def orbsun(d):

# Orbital elements of the Sun: */
    N = 0.0
    i = 0.0
    w = 282.9404 + 4.70935E-5 * d
    a = 1.000000  #(AU)
    e = 0.016709 - 1.151E-9 * d
    M = 356.0470 + 0.9856002585 * d
    M=scF360(M)
    w=scF360(w)
    return (N,i,w,a,e,M)
def orbmoon(d):
# Orbital elements of the Moon:
    N = 125.1228 - 0.0529538083 * d
    i = 5.1454
    w = 318.0634 + 0.1643573223 * d
    a = 60.2666  #(Earth radii)
    e = 0.054900
    M = 115.3654 + 13.0649929509 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbmercury(d):
# Orbital elements of Mercury:
    N =  48.3313 + 3.24587E-5 * d
    i = 7.0047 + 5.00E-8 * d
    w =  29.1241 + 1.01444E-5 * d
    a = 0.387098 # (AU)
    e = 0.205635 + 5.59E-10 * d
    M = 168.6562 + 4.0923344368 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbvenus(d):
# Orbital elements of Venus:
    N =  76.6799 + 2.46590E-5 * d
    i = 3.3946 + 2.75E-8 * d
    w =  54.8910 + 1.38374E-5 * d
    a = 0.723330  #(AU)
    e = 0.006773 - 1.302E-9 * d
    M =  48.0052 + 1.6021302244 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbmars(d):
# Orbital elements of Mars:
    N =  49.5574 + 2.11081E-5 * d
    i = 1.8497 - 1.78E-8 * d
    w = 286.5016 + 2.92961E-5 * d
    a = 1.523688  #(AU)
    e = 0.093405 + 2.516E-9 * d
    M =  18.6021 + 0.5240207766 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbjupiter(d):
# Orbital elements of Jupiter:
    N = 100.4542 + 2.76854E-5 * d
    i = 1.3030 - 1.557E-7 * d
    w = 273.8777 + 1.64505E-5 * d
    a = 5.20256  #(AU)
    e = 0.048498 + 4.469E-9 * d
    M =  19.8950 + 0.0830853001 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbsaturn(d):
# Orbital elements of Saturn:
    N = 113.6634 + 2.38980E-5 * d
    i = 2.4886 - 1.081E-7 * d
    w = 339.3939 + 2.97661E-5 * d
    a = 9.55475  #(AU)
    e = 0.055546 - 9.499E-9 * d
    M = 316.9670 + 0.0334442282 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orburanus(d):
# Orbital elements of Uranus:
    N =  74.0005 + 1.3978E-5 * d
    i = 0.7733 + 1.9E-8 * d
    w =  96.6612 + 3.0565E-5 * d
    a = 19.18171 - 1.55E-8 * d  #(AU)
    e = 0.047318 + 7.45E-9 * d
    M = 142.5905 + 0.011725806 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)
def orbneptune(d):
# Orbital elements of Neptune:
    N = 131.7806 + 3.0173E-5 * d
    i = 1.7700 - 2.55E-7 * d
    w = 272.8461 - 6.027E-6 * d
    a = 30.05826 + 3.313E-8 * d  #(AU)
    e = 0.008606 + 2.15E-9 * d
    M = 260.2471 + 0.005995147 * d
    M=scF360(M)
    w=scF360(w)
    N=scF360(N)
    return (N,i,w,a,e,M)

def azimutcoor(LST,RA,Decl) :
    HA = LST -RA
#    print (HA,LST,RA)
    HA=HA/12.0*180.0
    x = cosd(HA) * cosd(Decl)
    y = sind(HA) * cosd(Decl)
    z = sind(Decl)
    lat = local_b
    xhor = x * sind(lat) - z * cosd(lat)
    yhor = y
    zhor = x * cosd(lat) + z * sind(lat)

    az  = atan2( yhor, xhor ) + 180
    alt = atan2( zhor, math.sqrt(xhor*xhor+yhor*yhor) )
    return (az,alt)

def azimutcoorsun(UT) :
    y=ydate
    m=mdate
    D=Ddate
    d=day (y,m,D,UT)
    (lonsun,LST,r,xs,ys,zs,xe,ye,ze,RA,Dec) = sunpos(d,UT)
    (az,alt)= azimutcoor(LST,RA,Dec) 
    return(az,alt)
def azimutcoormoon(UT) :
    y=ydate
    m=mdate
    D=Ddate
    d=day (y,m,D,UT)
    (LST,r,RA,Dec) = planet_pos("mond",d,UT)
    (az,alt)= azimutcoor(LST,RA,Dec) 
    return(az,alt)

#    y=2020
#    m=4
#    D=12
#    UT=9+30/60.0 
dstr=datetime.datetime.utcnow()
dstr=str(dstr)
ydate=int(dstr[0:4])
mdate=int(dstr[5:7])
Ddate=int(dstr[8:10])
UTdate=int(dstr[11:13])
Umindate=int(dstr[14:16])
Usecdate=int(dstr[17:19])
UTdate=UTdate+(Umindate+Usecdate/60.0)/60.0 

d=day (ydate,mdate,Ddate,UTdate)
d00=d
(lonsun,LST,r,xs,ys,zs,xe,ye,ze,RA,Dec) = sunpos(d,UTdate)
sunRA=RA
sunDec=Dec
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssp=[]
ssr=[]
ssr.append((RAh+RAm/60.0,0))
ssp.append(("sun",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("sun","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
  
#    print ("sun      r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))

# 6. The position of the Moon and of the planets applied in function kepler(e,M)
# Now we must solve Kepler's equation
#    M = e * sind(E) - E
# where we know M, the mean anomaly, and e, the eccentricity, and we want to find E, the eccentric anomaly.
# We start by computing a first approximation of E:
(lst,r,RA,Dec)= planet_pos("jupiter",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,1))
ssp.append(("jupiter",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("jupiter","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
#    print ("jupiter  r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))
(lst,r,RA,Dec)= planet_pos("venus",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,2))
ssp.append(("venus",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("venus","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
#    print ("venus    r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))
(lst,r,RA,Dec)= planet_pos("mars",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,3))
ssp.append(("mars",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("mars","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
#    print ("mars     r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))
(lst,r,RA,Dec)= planet_pos("saturn",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,4))
ssp.append(("saturn",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("saturn","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
#    print ("saturn   r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))
(lst,r,RA,Dec)= planet_pos("merkur",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,5))
ssp.append(("merkur",r, RAh,RAm,Decd,Decm,RA,Dec))
#    ssp.append(("merkur","     %8.4f","  %4.1f","   %5.2f","   %5.1f","  %5.2f ") % ( r, RAh,RAm,Decd,Decm))
#    print ("merkur   r %8.4f  RA %4.1f h  %5.2f min  Dec %5.1f deg %5.2f min" % ( r, RAh,RAm,Decd,Decm))
# For the Moon, this is the geocentric (Earth-centered) position in the ecliptic coordinate system. For the planets, this is the heliocentric (Sun-centered) position, also in the ecliptic coordinate system. If one wishes, one can compute the ecliptic longitude and latitude (this must be done if one wishes to correct for perturbations, or if one wants to precess the position to a standard epoch):
#    lonecl = atan2( yh, xh )
#    latecl = atan2( zh, sqrt(xh*xh+yh*yh) )
# As a check one can compute sqrt(xh*xh+yh*yh+zh*zh), which of course should equal r (except for small round-off errors).
ddecm=[]
for iin in range(0,62) :
    (lst,r,RA,ddec)=planet_pos("mond",d-14+0.5*iin,UTdate)
    ddecm.append(ddec)
(lst,r,RA,Dec)= planet_pos("mond",d,UTdate)
(RAh,RAm)=convhm(RA)
(Decd,Decm)=convdeg(Dec)
ssr.append((RAh+RAm/60.0,6))
ssp.append(("mond",r, RAh,RAm,Decd,Decm,RA,Dec))
#print ("mond",r,RAh,RAm,Dec)

    
(sunazim,sunalt)=azimutcoor(LST,sunRA,sunDec)
page=markup.page()
now=str(datetime.datetime.now())
page.init(  doctype="<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN' 'http://www.w3.org/TR/html4/loose.dtd'> ",
               title="Planeten Positionen",
               css=( 'planets.css' ),
               charset='UTF-8',
               header="",
               metainfo={'author':['Walter Egli'], 'keywords':['' ]}
               )
    
#page.body (style="background-image:url('L1001107v1.JPG'), background-size:'cover'")
page.div(" ")
page.h1(" Aktuelle Positionen der Planeten "+now[0:16])
page.p(" ohne Uranus und Neptun.")
page.p(" <small>python program,  Daten aus ref. 'How to compute planetary positions, by Paul Schlyter, Stockholm, Sweden' </small>")
page.p(" sortiert nach RA Rektaszension (right ascension),<br> <small>Azimut und H&ouml;he basierend auf "+str(local_longitude)+ " und "+str(local_b)+" L&auml;nge und Breite B&auml;retswil/ZH </small>")
ssr.sort()
lll=""
page.table()
page.tr.open()
page.td("<b>planet")
page.td("<b>r/a {/km}")
page.td("<b> RA/h ")
page.td("<b> Dec/deg ")
page.td("<b> Azim/deg ")
page.td("<b> Alt/deg </b>")
page.tr.close()
#    page.p ("planet     r/a      RA    RAmin     Dec   Decmin")
for k in range(0,7):
       (rra,j)=ssr[k]
#      lll=lll+ (ssp[j])+"<br>"
       (nam,r,ra,ram,dec,decm,RA,Dec)=ssp[j]
#       rs=str(r)
       page.tr.open()
       if RA < 0 :
          RA=RA+24.0
       (azim,alt)=azimutcoor(LST,RA,Dec)
       if nam =="mond" :
              RAmoon=RA
              Decmoon=Dec
              moonalt=alt
              moonazim=azim
       if nam == "sun" :
          sunalt=alt
          sunazim=azim
          RAsun=RA
       if (alt < 0)   or ((sunalt > 1) and nam !="sun") :  
          page.td(nam)
          if nam == "mond" :
              dmo=r*6371
              page.td(str.format(("%9.0f")%(dmo)))
          else:   
              page.td(str.format(("%7.2f")%(r)))
          page.td(str.format(("%9.3f")%(RA)))
          page.td(str.format(("%9.2f")%(Dec)))
          page.td(str.format(("%9.2f")%(azim)))
          page.td(str.format(("%9.2f")%(alt)))
       else:
          page.td("<b>"+nam)
          if nam == "mond" :
              dmo=r*6371
              page.td(str.format(("<b>%9.0f")%(dmo)))
          else:   
              page.td(str.format(("<b>%7.2f")%(r)))
          page.td(str.format(("<b>%9.3f")%(RA)))
          page.td(str.format(("<b>%9.2f")%(Dec)))
          page.td(str.format(("<b>%9.2f")%(azim)))
          page.td(str.format(("<b>%9.2f </b>")%(alt)))

#       page.td(ra)
#       ram=str(ram)
#       page.td(ram[0:6])
#       page.td(dec)
#       decm=str(decm)
#       page.td(decm[0:6])
       page.tr.close()

page.table.close()

xx=[]
yy=[]
npkt=62
pi=3.1415926
xfig=6
yfig=5
plt.figure(figsize=(xfig,yfig))
plt.xlabel('Zeit/Tag', fontsize=18)
plt.ylabel('Dec/grad', fontsize=18)
axs=plt.axis([0,28,-24,24])

n=14*2
for i in range(0,n+1):
  t=0.5*i
  x=t
#  y=decmax*math.sin(t/14.0*pi)
  y=ddecm[i]
  xx.append(x)
  yy.append(y)
plt.plot(xx,yy,'black')
xx=[]
yy=[]
for i in range(n,npkt):
  t=0.5*i
  x=t
#  y=decmax*math.sin(t/14.0*pi)
  y=ddecm[i]
  xx.append(x)
  yy.append(y)
plt.plot(xx,yy,'--',color='black')

t=14
#yd=decmax*math.sin(t/14.0*pi)
yd=Decmoon
plt.plot([t],[yd],'o',color='black')
plt.title ('Mond Verlauf und Phase', fontsize=22)
xxti=np.arange(0,31,1)

plt.xticks(xxti)
plt.tick_params(labelbottom=False)

plt.yticks(np.arange(-30, 35, 5))
rmond=2.0
xxm=[]
yym=[]
alfa=(sunRA-RAmoon)*pi/12.0

dal=(sunalt-moonalt)*pi/180.0
daz=(sunazim-moonazim)*pi/180.0
beta=math.atan(dal/daz)
scalx=1
scaly=1.0*xfig/yfig*60.0/30.
scalx = -scalx*math.cos(alfa)
if alfa >=  -pi :
  for i in range(0,16):                                                        
    phi=i*2.0*pi/30.0-pi/2.0
    xxm.append(rmond*math.cos(phi))
    yym.append(rmond*math.sin(phi))
  for i in range(16,31):                                                        
    phi=i*2.0*pi/30.0-pi/2.0
    xxm.append(rmond*math.cos(phi)*scalx)
    yym.append(rmond*math.sin(phi))
else :
  for i in range(16,31):                                                        
    phi=i*2.0*pi/30.0-pi/2.0
    xxm.append(rmond*math.cos(phi))
    yym.append(rmond*math.sin(phi))
  for i in range(0,16):                                                        
    phi=i*2.0*pi/30.0-pi/2.0
    xxm.append(rmond*math.cos(phi)*scalx)
    yym.append(rmond*math.sin(phi))

#  drehen um beta
for i in range (0,31):
  xxmd=xxm[i]*math.cos(beta)-yym[i]*math.sin(beta) 
  yymd=xxm[i]*math.sin(beta)+yym[i]*math.cos(beta)
  xxm[i]=xxmd+t
  yym[i]=yymd*scaly+yd
#plt.plot(xxm,yym,color='#ffcc33')    
plt.fill(xxm,yym,'#ffcc33')    
xtext = 2
idd=14*2
if ddecm[idd+1] -ddecm[idd] <0.0 :
    plt.text(xtext,yd,'Mond im Nidsigänt',fontsize=12)
if ddecm[idd+1] -ddecm[idd] >0.0 :
    plt.text(xtext,yd,'Mond im Obsigänt',fontsize=12)
xtext=5
plt.text(xtext,-2,'Ecliptic',fontsize=12)
plt.plot([0,30],[0,0])

dni=1
while (ddecm[idd+dni]<ddecm[idd+dni-1]) :
   dni=dni+1
strr=" "
#print ("anzahl tage ",int(dni/2))
if int(dni/2) == 1 :
   strr='noch '+str(int(dni/2))+' Tag'
if int(dni/2) > 1 :
   strr='noch '+str(int(dni/2))+' Tage'
xtext=2
plt.text(xtext,yd-2.5,strr,fontsize=12)
xxm=[]
yym=[]
for i in range(0,31):                                                           
  phi=i*2.0*pi/30.0
  xxm.append(rmond*math.cos(phi)+14)
  yym.append(rmond*math.sin(phi)*scaly+sunDec)
#plt.plot(xxm,yym,color='#ffcc33')    
#
# Zero points sunalt(d) = 0 Sonnenauf- und  Sonnenuntergang
#             sunalt(d)+daltof = 0
#
#  Sonnenuntergang zuerst Start um 16 Uhr
UT=14.0
(azsun,sunalt)= azimutcoorsun(UT)
sunaltv=sunalt
ddxx=3.0
deltaUT=1.0 # for numerical first order differential
while (sunalt*sunaltv > 0.0 ) :
   UT=UT+ddxx    #  3 Stunden
   sunaltv=sunalt
   (azsun,sunalt)= azimutcoorsun(UT)
while (abs(sunalt-sunaltv)> 0.0001) :
# newton
   (azsun,sunaltv)=azimutcoorsun(UT-deltaUT)
   sunaltv=sunaltv+daltof
   sunalts=(sunalt-sunaltv)
   dxx=-sunalt/sunalts
   UT=UT+dxx
   sunaltv=sunalt
   (azsun,sunalt)= azimutcoorsun(UT)
   sunalt=sunalt+daltof
#   print (UT,dxx,sunalt)
stxt=zeithms(UT+2.0)
#print (" sunset ",sunalt,stxt)
stxt="Sonnenuntergang "+stxt
UT=8.0   #  wir gehen rueckwärts
while (sunalt*sunaltv > 0.0 ) :
   UT=UT-ddxx    #  3 Stunden
   sunaltv=sunalt
   (azsun,sunalt)= azimutcoorsun(UT)
#   print (UT,sunalt) 
while (abs(sunalt-sunaltv)> 0.0001) :
# newton
   (azsun,sunaltv)=azimutcoorsun(UT-deltaUT)
   sunaltv=sunaltv+daltof
   sunalts=(sunalt-sunaltv)
   dxx=-sunalt/sunalts
   UT=UT+dxx
   sunaltv=sunalt
   (azsun,sunalt)= azimutcoorsun(UT)
   sunalt=sunalt+daltof
stxtr=zeithms(UT+2.0)
#print (" sunrise ",sunalt,stxtr)
daltofm=0.0
stxtr="Sonnenaufgang "+stxtr
stxtt=stxtr+ " -- "+stxt
#page.p(stxtt)
# Zero points   Mondaufgang - Monduntergang
#
#  Wahl-   zuerst Start 
UT=-2.0
(azmoon,moonalt)= azimutcoormoon(UT)
(azmoon,moonaltv)= azimutcoormoon(UT-1.0)

stxt="Mondaufgang " 
ddxx=3.0
if (moonalt > moonaltv ) and moonalt>0.0 :
#   moonrise am Vortag
#    print("moonrise am Vortag")
    stxt="Mondaufgang am Vortag " 
    ddxx=-3.0
#print ("mond UT,alt,altv,az",UT,moonalt,moonaltv,azmoon)
while (moonalt*moonaltv > 0.0 ) :
   UT=UT+ddxx    #  3 Stunden
   moonaltv=moonalt
   (azmonn,moonalt)= azimutcoormoon(UT)
#   print (UT,dxx,moonalt)
while (abs(moonalt-moonaltv)> 0.0001) :
# newton 
   (azmoon,moonaltv)=azimutcoormoon(UT-deltaUT)
   moonaltv=moonaltv+daltofm
   moonalts=(moonalt-moonaltv)
   dxx=-moonalt/moonalts
   UT=UT+dxx
   moonaltv=moonalt
   (azmoon,moonalt)= azimutcoormoon(UT)
   moonalt=moonalt+daltofm
#   print (UT,dxx,moonalt)
#print (" moonrise ",moonalt,stxt)
stxt=stxt+zeithms(UT+2.0)

UT=UT+4.0
#UT=15.0-(RAmoon-RAsun)
##print ("UT 2",UT,moonalt)
ddxx=3.0
#  wir gehen rueckwärts
(azmoon,moonalt)= azimutcoormoon(UT)
moonaltv=moonalt
#print ("UT 2",UT,moonalt)
while (moonalt*moonaltv > 0.0 ) :
   UT=UT+ddxx    #  3 Stunden   find zero
   moonaltv=moonalt
   (azmoon,moonalt)= azimutcoormoon(UT)

# newton 
if UT < 0.0 :
   UT=UT+24.0
if UT > 24.0 :     #  do not go to the next day
   UT=UT-24.0
while (abs(moonalt-moonaltv)> 0.0001) :
   (azmoon,moonaltv)=azimutcoormoon(UT-deltaUT)
   moonaltv=moonaltv+daltofm
   moonalts=(moonalt-moonaltv)
   dxx=-moonalt/moonalts
   UT=UT+dxx
   moonaltv=moonalt
   (azmoon,moonalt)= azimutcoormoon(UT)
   moonalt=moonalt+daltofm
stxtr=zeithms(UT+2.0)
#print (" moonset ",moonalt,stxtr)
stxtr="Monduntergang "+stxtr
stxtt=stxtt + "<br>"+stxt+ " -- "+stxtr
stxtt="<small>"+stxtt+"</small>"
page.p(stxtt)
page.div.close()

#plt.show()
#Then in order to save your figure use:
#plt.savefig("/home/eglich1/public_html/mondverlauf.svg", format="svg")
plt.savefig("mondverlauf.svg", format="svg")
page.img(src="mondverlauf.svg",height=400,width=500)
#file=open('/home/eglich1/public_html/planets.html','w')
file=open('planets.html','w')
print ( page, file=file)
file.close()
