from django.shortcuts import render
from django.forms import modelform_factory
from . models import InputData
from . reometry import REO



def index(request):
    InputDataForm = modelform_factory(InputData, exclude=[])

    if request.method == 'POST':
        form = InputDataForm(request.POST)

        if form.is_valid():

            kąty = form.cleaned_data['kąty']
            lst_angles = list(map(int,kąty.split(",")))
            uklad_cylindrów_RB = form.cleaned_data['uklad_cylindrów_RB']
            typ_sprężyny = form.cleaned_data['typ_sprężyny']
            rodzaj_cylindra_wewnętrznego = form.cleaned_data['rodzaj_cylindra_wewnętrznego']

            x = REO(lst_angles,uklad_cylindrów_RB,typ_sprężyny,rodzaj_cylindra_wewnętrznego)

            x.rodzaj_cilindra()
            x.stala_spr()
            x.obroty()
            x.szybkosc_scinania_rz()
            katy =lst_angles
            szybkosc_scinania =[round(x,6) for x in x.count_szybkosc_scinania_rzecz()]
            naprezenia_styczne = [round(x,6) for x in x.count_naprezenie_styczne_rzecz()]
            lepkosc_pozorna = [round(x,6) for x in x.count_lepkosc_poz_rzecz()]
            lepkosc_dym_newtona = round(x.lepkosc_dynamiczna_newtona(),6)
            x.model_newtona_wart()
            wspł_korelacji_newtona = x.wspl_korelacji_N()
            lepkosc_plastyczna_b = round(x.lepkosc_plastyczna_binghama(),6)
            granica_plyniencia_b = round(x.granica_plyniecia(),6)
            x.model_binghama_wartosci()
            wspl_korelacji_binghama = x.wspl_korelacji_B()
            wspl_ksztaltu_odw = round(x.wspl_ksztaltu_0dw(),6)
            wspl_konsystencji_odw = round(x.wspl_konsystencji_0dw(),6)
            x.model_odw_wartosci()
            wspl_korelacji_odw = x.wspl_korelacji_odw()
            lepkosc_cassona = round(x.lepkosc_cassona(),6)
            granica_plny_cassona = round(x.granica_plyniecia_Cassona(),6)
            x.model_cassona_wartosci()
            wspl_korelacji_cassona = x.wspl_korelacji_cass()
            wspl_ksztaltu_hb = round(x.bisekcja(),6)
            wspl_konsystencji_hb = round(x.wspolczynnik_konsytencji_HB(),6)
            granica_plyn_hb = round(x.granica_plyniecia_HB(),6)
            x.model_H_B_wartosci()
            wspl_korelacji_hb = x.wspl_korelacji_hb()
            dopasowanie = x.dopasowanie()
            wykres = x.wykres()
            return render(request, 'kalkulator/test.v01.html', {'katy': katy,
                                                                'szybkosc_scinania':szybkosc_scinania,
                                                                'naprezenia_styczne':naprezenia_styczne,
                                                                'lepkosc_pozorna':lepkosc_pozorna,
                                                                'lepkosc_dym_newtona':lepkosc_dym_newtona,
                                                                'wspł_korelacji_newtona':wspł_korelacji_newtona,
                                                                'lepkosc_plastyczna_b':lepkosc_plastyczna_b,
                                                                'granica_plyniencia_b':granica_plyniencia_b,
                                                                'wspl_korelacji_binghama':wspl_korelacji_binghama,
                                                                'wspl_ksztaltu_odw': wspl_ksztaltu_odw,
                                                                'wspl_konsystencji_odw':wspl_konsystencji_odw,
                                                                'wspl_korelacji_odw':wspl_korelacji_odw,
                                                                'lepkosc_cassona':lepkosc_cassona,
                                                                'granica_plny_cassona':granica_plny_cassona,
                                                                'wspl_korelacji_cassona':wspl_korelacji_cassona,
                                                                'wspl_ksztaltu_hb':wspl_ksztaltu_hb,
                                                                'granica_plyn_hb':granica_plyn_hb,
                                                                'wspl_konsystencji_hb':wspl_konsystencji_hb,
                                                                'wspl_korelacji_hb':wspl_korelacji_hb,
                                                                'dopasowanie':dopasowanie,
                                                                'wykres':wykres,})



    return render(request,'kalkulator/imput form.html',{'form':InputDataForm})



