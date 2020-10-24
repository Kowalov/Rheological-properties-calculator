import math

#liczy logarytm naturalny z liczby
def lnx (x):
    lnx=math.log(x)
    return(lnx)

#liczy logarytm naturalny z listy
def lnlist (x):
    lnxl=[]
    for i in range(0, len(x)):
        lnxl.append(math.log(x[i]))
    return(lnxl)

#mnoży listy
def multlist (x,y):
    xy=[]
    for i in range(0, len(x)):
        xy.append(x[i]*y[i])
    return(xy)

#sumowanie wartości listy
def listsum (x):
    sx=sum(x)
    return (sx)

#Podnoszenie każdego wyrazu listy do kwadratu
def listexp (x):
    expl=[]
    for i in range(len(x)):
        expl.append(x[i] ** 2)
    return(expl)

#liczy pierwiastek z liczby
def sqrtx (x):
    sqrtx=math.sqrt(x)
    return(sqrtx)

#Liczy pierwiastek z każdej liczby z listy
def sqrtlist (x):
    sqrx=[]
    for i in range(0, len(x)):
        sqrx.append(math.sqrt(x[i]))
    return(sqrx)

#Podnosi każdy element listy do potęgi 2
def multlita (x):
    mx=[]
    for i in range (len(x)):
        mx.append (x[i]**2)
    return(mx)

#exp listy
def explist (x):
    ex =[]
    for i in range (len(x)):
        ex.append (math.exp(x[i]))
    return (ex)

#odejmuje poszczególne wyrazy z list
def minuslist (x,y):
    mx = []
    for i in range(0, len(x)):
        mx.append(x[i] - y[i])
    return(mx)

#odejmowanie liczby od każdej liczby w liście
def mlist(x,y):
    mx = []
    for i in range(0, len(x)):
        mx.append(x[i] - y)
    return(mx)

def test(x):
    ang=[]
    for i in range(0,len(x)):
       ang = int(x[i])
    return ang