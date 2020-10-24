import math
from . import functions as fnct
import numpy
import plotly.graph_objs as go
import plotly.offline as opy
import scipy.optimize as optimize


class REO:
    def __init__(self,kąt,typ,sprężyna,Rotor_Bob):
        self.kąt = kąt
        self.typ = typ
        self.sprężyna = sprężyna
        self.Rotor_Bob = Rotor_Bob
        self.obr = []
        self.yl = []
        self.ks = []
        self.ns = []
        self.t = []
        self.y = []
        self.f = []
        self.l=[]
        self.mn = []
        self.lb =[]
        self.ty = []
        self.mb = []
        self.no =[]
        self.k = []
        self.modw = []
        self.fcas = []
        self.tyc = []
        self.modc = []
        self.n =[]
        self.khb = []
        self.tyhb =[]
        self.modhb = []
        self.RN = []
        self.RB = []
        self.Rodw = []
        self.RC = []
        self.Rhb = []


    def obroty(self):
        if len(self.kąt) is 6:
            self.obr = [3, 6, 100, 200, 300, 600]
        elif len(self.kąt) is 12:
            self.obr = [1, 2, 3, 6, 10, 20, 30, 60, 100, 200, 300, 600]
        else:print('Error')
        return self.obr

    def szybkosc_scinania_rz(self):         #szybkość ścinania rezcyzywista
        if self.typ is 1:
            self.yl = 1.7034
        elif self.typ is 2:
            self.yl = 0.3769
        elif self.typ is 3:
            self.yl = 0.2682
        elif self.typ is 4:
            self.yl = 5.4106
        elif self.typ is 5:
            self.yl =0.40865
        elif self.typ is 6:
            self.yl = 0.27589
        elif self.typ is 7:
            self.yl = 0.37723
        elif self.typ is 8:
            self.yl = 0.27052
        elif self.typ is 9:
            self.yl = 0.23579
        elif self.typ is 10:
            self.yl = 0.23579
        return self.yl

    def stala_spr(self):                            #Stała sprężyny
        if self.sprężyna is 1:
            self.ks = 0.2
        if self.sprężyna is 2:
            self.ks = 0.5
        if self.sprężyna is 3:
            self.ks = 1
        if self.sprężyna is 4:
            self.ks = 2
        if self.sprężyna is 5:
            self.ks = 3
        if self.sprężyna is 6:
            self.ks = 10
        return self.ks

    def rodzaj_cilindra(self):                      #Dobór rodzaju cylindra
        if self.Rotor_Bob is 1:
            self.ns = 0.511
        if self.Rotor_Bob is 2:
            self.ns = 1.009
        if self.Rotor_Bob is 3:
            self.ns = 2.045
        if self.Rotor_Bob is 4:
            self.ns = 4.092
        return self.ns

    def count_naprezenie_styczne_rzecz (self):      #Obliczanie rzeczywistego naprężenia stycznego
        for i in range(len(self.kąt)):
            self.t.append(self.kąt[i] * self.ns * self.ks)
        return self.t

    def count_szybkosc_scinania_rzecz (self):       #Obliczanie rzeczywistej szybkości ścinania
        for i in range(len(self.obr)):
            self.y.append(self.obr[i]*self.yl)
        return self.y

    def count_lepkosc_poz_rzecz (self):             #Obliczanie lepkość pozorną cieczy
        for i in range(len(self.t)):
            self.f.append(self.t[i] / self.y[i])
        return self.f


    def lepkosc_dynamiczna_newtona (self):          #Obliczenie lepkości plastycznej Newtona
        self.l=sum((fnct.multlist(self.t,self.y)))/sum((fnct.listexp(self.y)))
        return self.l

    def model_newtona_wart(self):                   #Obliczanie wartości do wykresu dla modelu Newtona
        self.mn = list(map(lambda x: x*self.l,self.y))
        return self.mn

    def lepkosc_plastyczna_binghama (self):         #Obliczanie lepkości plastycznej binghama
        self.lb = ((len(self.kąt)*(sum(fnct.multlist(self.t,self.y)))) - sum(self.y) * sum(self.t)) /\
                  ((len(self.kąt) * sum(fnct.listexp(self.y)) - (sum(self.y)) ** 2))
        return self.lb

    def granica_plyniecia (self):                   #Obliczenie granicy płynięcia dla modelu Binghama
        self.ty=(sum(self.t)-(self.lb*sum(self.y)))/(len(self.kąt))
        return self.ty

    def model_binghama_wartosci(self):              #Obliczenie wartości do wykresu dla modelu Binghama
        self.mb =list(map(lambda x: x*self.lb + self.ty,self.y))
        return self.mb

    def wspl_ksztaltu_0dw(self):                    #Obliczenie współczynnika kształtu dla modelu Ostwalda
        self.no = ((len(self.kąt)*sum(fnct.multlist(fnct.lnlist(self.y),fnct.lnlist(self.t))))-
                   (sum(fnct.lnlist(self.y))*sum(fnct.lnlist(self.t))))/\
                  ((len(self.kąt)*sum(fnct.multlita(fnct.lnlist(self.y)))-(sum(fnct.lnlist(self.y)))**2))
        return self.no

    def wspl_konsystencji_0dw(self):                #Obliczenie współczynnika konsystencji dla modelu Ostwalda
        self.k = math.exp((sum(fnct.lnlist(self.t))-self.no*sum(fnct.lnlist(self.y)))/len(self.kąt))
        return self.k

    def model_odw_wartosci(self):                   #Obliczenie wartości do wykresu modelu Ostwalda
        self.modw = fnct.explist(list(map(lambda x: x*self.no + math.log(self.k),fnct.lnlist(self.y))))
        return self.modw

    def lepkosc_cassona(self):                      #Obliczenie lepkości Cassona
        self.fcas = (((len(self.kąt)*sum(fnct.multlist(fnct.sqrtlist(self.y),fnct.sqrtlist(self.t))))- \
                     (sum(fnct.sqrtlist(self.y))*sum(fnct.sqrtlist(self.t))))/\
                    ((len(self.kąt)*sum(fnct.multlita(fnct.sqrtlist(self.y)))) - ((sum(fnct.sqrtlist(self.y)))**2)))**2
        return self.fcas

    def granica_plyniecia_Cassona(self):            #Obliczenie granicy płynięcia Cassona
        self.tyc = ((sum(fnct.sqrtlist(self.t))-(math.sqrt(self.fcas)*sum(fnct.sqrtlist((self.y)))))/len(self.kąt))**2
        return self.tyc

    def model_cassona_wartosci(self):               #Obliczenie wartości do wykresu modelu Cassona
        self.modc = fnct.multlita(list(map(lambda x : x*math.sqrt(self.fcas)+ \
                                                     math.sqrt(self.tyc),fnct.sqrtlist(self.y))))
        return self.modc

    def gne(self,n):                                #Funkcja z której liczymy miejsce zerowe
        return len(self.kąt)*(sum(fnct.multlist(fnct.multlist(self.t,fnct.lnlist(self.y)),list(map(lambda x: x**n,self.y)))))-\
               sum(self.t)*sum(fnct.multlist(list(map(lambda x: x**n,self.y)),fnct.lnlist(self.y))) + \
               ((len(self.kąt) * sum(fnct.multlist(self.t, (list(map(lambda x: x ** n, self.y)))))) - \
                (sum(self.t) * sum((list(map(lambda x: x ** n, self.y)))))) / ((len(self.kąt) * sum((list(map(lambda x: x ** (2 * n), self.y))))) - \
                 (sum((list(map(lambda x: x ** n, self.y)))) * sum(list(map(lambda x: x ** n, self.y))))) * \
               ((sum((list(map(lambda x: x ** n, self.y)))) * (sum(fnct.multlist(list(map(lambda x: x ** n, self.y)), fnct.lnlist(self.y)))))- \
                (len(self.kąt) * (sum(fnct.multlist(list(map(lambda x: x **(2 * n), self.y)), fnct.lnlist(self.y))))))

    def bisekcja(self):                             #Moduł bisekcji
        self.n = optimize.bisect(self.gne, 0.00001, 10)
        if 0 < self.n < 100:
            return self.n
        else:
            return 'nieprawidłowy wynik'


    def wspolczynnik_konsytencji_HB(self):          #obliczenie współ. Konsyst. HB
        self.khb = (len(self.kąt) * sum(fnct.multlist(self.t,list(map(lambda x: x**self.n, self.y)))) - sum(self.t)* sum(list(map(lambda x: x**self.n,self.y))))/ \
                    (len(self.kąt)* sum(list(map(lambda x: x**(2*self.n),self.y))) - sum(list(map(lambda x: x**self.n,self.y))) * sum(list(map(lambda x: x**self.n,self.y))))
        return self.khb

    def granica_plyniecia_HB(self):                 #obliczanie granicy płynięcia modelu Herschela
        self.tyhb = (sum(self.t) - self.khb * sum(list(map(lambda x: x**self.n, self.y))))/ len(self.kąt)
        return self.tyhb

    def model_H_B_wartosci(self):                   #Obliczanie wartości dla modelu Herschela
        self.modhb = list(map(lambda x : x**self.n * self.khb + self.tyhb, self.y))
        return self.modhb


    def wspl_korelacji_N(self):                     #Obliczenie wspł. korelacji dla modelu Newtona
        if sum(fnct.multlita(fnct.minuslist(self.t,self.mn))) == 0 or sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) == 0 or 1 - sum(fnct.multlita(fnct.minuslist(self.t,self.mn)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) < 0:
            self.RN = 0
            return str('Zbyt niska korelacja')
        else:
            self.RN = math.sqrt(1 - sum(fnct.multlita(fnct.minuslist(self.t,self.mn)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))))
            return round(self.RN,6)


    def wspl_korelacji_B(self):                     #Obliczenie wspł. korelacji dla modelu Binghama
        if sum(fnct.multlita(fnct.minuslist(self.t,self.mb))) == 0 or sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) == 0 or 1 - sum(fnct.multlita(fnct.minuslist(self.t,self.mb)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) < 0:
            self.RB = 0
            return str('Zbyt niska korelacja')
        else:
            self.RB = math.sqrt(1 - sum(fnct.multlita(fnct.minuslist(self.t,self.mb)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))))
            return round(self.RB,6)

    def wspl_korelacji_odw(self):                   #Obliczenie wspł. korelacji dla modelu Ostwalda
        if sum(fnct.multlita(fnct.minuslist(self.t,self.modw))) == 0 or sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) == 0 or 1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modw)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) < 0:
            self.Rodw = 0
            return str('Zbyt niska korelacja')
        else:
            self.Rodw = math.sqrt(1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modw)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))))
            return round(self.Rodw,6)

    def wspl_korelacji_cass(self):                  #Obliczenie wspł. korelacji dla modelu Cassona
        if sum(fnct.multlita(fnct.minuslist(self.t,self.modc))) == 0 or sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) == 0 or 1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modc)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) < 0:
            self.RC = 0
            return ('Zbyt niska korelacja')
        else:
            self.RC = math.sqrt(1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modc)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))))
            return round(self.RC,6)

    def wspl_korelacji_hb(self):                    #Obliczenie wspł. korelacji dla modelu Herschela
        if sum(fnct.multlita(fnct.minuslist(self.t,self.modhb))) == 0 or sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) == 0 or 1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modhb)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))) < 0:
            self.Rhb = 0
            return ('Zbyt niska korelacja')
        else:
            self.Rhb = math.sqrt(1 - sum(fnct.multlita(fnct.minuslist(self.t,self.modhb)))/sum(fnct.multlita(fnct.mlist(self.t, numpy.average(self.t)))))
            return round(self.Rhb,6)



    def dopasowanie(self):                          #Określa najlepiej dopasowany model
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) <= 0.70:
            return 'Żaden z modelów nie zapewnia akceptowalego poziomu dopasowania'
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) == self.RN:
            return 'Model Newtona'
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) == self.RB:
            return 'Model Binghama'
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) == self.Rodw:
            return 'Model Ostwalda de Waele'
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) == self.RC:
            return 'Model Cassona'
        if max(self.RN,self.RB,self.Rodw,self.RC,self.Rhb) == self.Rhb:
            return 'Model Herschela - Bulkleya'
        else:
            return 'Wystąpił błąd'



    def wykres_newton(self):                     # oblicza wartości do wykresu dla modelu newtona
        return list(map(lambda x: x * self.l, numpy.arange(0, 1050, 10)))

    def wykres_bingham(self):                    # oblicza wartości do wykresu dla modelu binghama
        return list(map(lambda x: x * self.lb + self.ty, numpy.arange(0, 1050, 10)))

    def wykres_odw(self):                          # oblicza wartości do wykresu dla modelu ostwalda
        return fnct.explist(list(map(lambda x: x * self.no + math.log(self.k), fnct.lnlist(numpy.arange(1, 1050, 10)))))

    def wykres_casson(self):                        # oblicza wartości do wykresu dla modelu cassona
        return fnct.multlita(list(map(lambda x: x * math.sqrt(self.fcas) + \
                                                math.sqrt(self.tyc), fnct.sqrtlist(numpy.arange(0, 1050, 10)))))

    def wykres_hb(self):                            ## oblicza wartości do wykresu dla modelu herschela
        return list(map(lambda x: x ** self.n * self.khb + self.tyhb, numpy.arange(0, 1050, 10)))


    def wykres(self):               #wykres szybkości ścinania od naprężenia stycznego

        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.y, y=self.t,
                                 mode='markers', name='Punkty pomiarowe'))
        fig.add_trace(go.Scatter(x=numpy.arange(0,1050,10), y=self.wykres_newton(),
                                 mode='lines',
                                 name='Model Newtona',line_shape='spline'))
        fig.add_trace(go.Scatter(x=numpy.arange(0,1050,10), y=self.wykres_bingham(),
                                 mode='lines',
                                 name='Model Binghama',line_shape='spline'))
        fig.add_trace(go.Scatter(x=numpy.arange(0,1050,10), y=self.wykres_odw(),
                                 mode='lines', name='Model Ostwalda de Waele',line_shape='spline'))
        fig.add_trace(go.Scatter(x=numpy.arange(0,1050,10), y=self.wykres_casson(),
                                 mode='lines', name='Model Cassona',line_shape='spline'))
        fig.add_trace(go.Scatter(x=numpy.arange(0,1050,10), y=self.wykres_hb(),
                                 mode='lines', name='Model Herschela - Bulkleya',line_shape='spline'))

        fig.update_layout(title='Dopasowanie Modelów',
                          xaxis_title='Szybkość Ścinania [1/s]',
                          yaxis_title='Naprężenia Styczne [Pa]')

        div = opy.plot(fig,auto_open= False,output_type='div')

        return div

