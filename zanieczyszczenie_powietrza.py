#Projekt wykonany w ramach uczestnictwa w warsztatach WrocLove Code Carrots Python
#Program tworzy interaktywną mapę poziomu zanieczyszczenia powietrza ze stacji pomiarowych w miastach w Polsce,
#podaje też historię pomiarów dla wybranej stacji.

def get_measuring_stations():
    import json
    import requests
    r = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll')
    return r.json()

#get_measuring_stations()

def get_measuring_stations_for_city(city):

    #Krok 2.
    #Stwórz funkcję get_measuring_stations_for_city(city) wyświetlającą dane wszyskich stacji pomiarowych
    #dla podanego miasta. Jeśli dla danego miasta nie ma stacji, wypisz Brak danych.

    stacje_pom = []
    stacje_pom_nazwy = []
    jest_stacja = 0
    wszystko = get_measuring_stations()
    for element_stacji in wszystko:
        if element_stacji['city'] != None:
            dane_stacji = element_stacji['city']
            miasto = dane_stacji['name']
            nazwa_stacji = element_stacji['stationName']
            if miasto == city:
                station_id = element_stacji['id']
                print('Dane stacji pomiarowej {} dla miasta {}: \n'.format(nazwa_stacji, city), element_stacji)
                stacje_pom.append(station_id)
                jest_stacja = 1
        elif element_stacji['city'] == None and city == element_stacji['stationName']:
            nazwa_stacji = element_stacji['stationName']
            station_id = element_stacji['id']
            print('Dane stacji pomiarowej {} dla miasta {}: \n'.format(nazwa_stacji, city), element_stacji)
            stacje_pom.append(station_id)
    if jest_stacja == 0:
        print('Brak danych \n')
    return stacje_pom

#get_measuring_stations_for_city('Kraków')

def get_sensors(station_id):

    #Krok 3.
    #Pobieranie   stanowisk   pomiarowych   dostępnych   dla   stacji
    #Stwórz funkcję get_sensors(station_id), wyświetlającą stanowiska pomiarowe dla danej stacji.

    stanowisko_dla_stacji_numery = []
    import requests
    station = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}'.format(station_id)
    stanowiska = requests.get(station)
    print('\n Stanowiska pomiarowe dla stacji o id {} \n'.format(station_id))
    stanowiska_pom_dla_stacji = stanowiska.json()
    for stanowisko in stanowiska_pom_dla_stacji:
        print('Stanowisko nr {}:'.format(stanowisko['id']), stanowisko, '\n')
        stanowisko_dla_stacji_numer = stanowisko['id']
        stanowisko_dla_stacji_numery.append(stanowisko_dla_stacji_numer)
    return stanowisko_dla_stacji_numery

#get_sensors(400)

def get_sensors_for_city(city):

    #Krok   4:
    #Pobieranie   stanowisk   pomiarowych   dostępnych   dla   podanego   miasta
    #Stwórz funkcję get_sensors_for_city(city), wyświetlającą stanowiska pomiarowe
    #dla wszystkich stacji w danej miejscowości. Jeśli dla danego miasta nie ma stacji, wypisz Brak danych.

    numery_stanowisk_dla_miasta = []
    stacje_pomiarowe = get_measuring_stations_for_city(city)
    sensory = []
    if stacje_pomiarowe == []:
        print('Brak danych')
    else:
        print('\n', 'Stanowiska pomiarowe dla wszystkich stacji w miejscowości {}'.format(city))
        for elem in stacje_pomiarowe:
            sensory_po_kolei = get_sensors(elem)
            for nr in sensory_po_kolei:
                numery_stanowisk_dla_miasta.append(nr)
    return numery_stanowisk_dla_miasta

#get_sensors_for_city('Kraków')

def zanieczyszczenia_dla_stacji(station_id):

    #Krok   5:
    #Pobieranie   danych   z   konkretnej   stacji
    #Stwórz   funkcję,   która   będzie   pobierała   aktualny   stan
    #zanieczyszczeń   dla   danej   stacji. Parametr:   stantion_id

    import requests
    nr_stanowiska_pomiarowe_dla_stacji = get_sensors(station_id)
    zanieczyszczenie_stacja = []
    for nr_stan in nr_stanowiska_pomiarowe_dla_stacji:
        d_pom = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'.format(nr_stan)
        dane_pom = requests.get(d_pom)
        dane_pom_stanowisko = dane_pom.json()
        zanieczyszczenie_stacja.append(dane_pom_stanowisko)
    if zanieczyszczenie_stacja == []:
        zanieczyszczenie_stacja = 'Brak danych'
    return zanieczyszczenie_stacja

#zanieczyszczenia_dla_stacji(400)

def czy_bezpiecznie_wyjsc_z_domu_dla_stacji(station_id):

    #Krok   6:
    #Dla   danych   z   konkretnej   stacji   aplikacja   powie   czy   bezpiecznie   wyjść   z   domu
    #Stwórz funkcję, zwracającą aktualny poziom (dopuszczalny, informowania, alarmowy) dla danej   stacji.
    #Normy   pyłów:   http://www.gios.gov.pl/pl/aktualnosci/294-normy-dla-pylow-drobnych-w-polsce

    dane_pomiarowe_stanowisko = zanieczyszczenia_dla_stacji(station_id)
    zanieczyszczenie = []
    czy_jest_pm10 = 0
    poziom = 'brak danych'
    if dane_pomiarowe_stanowisko == 'Brak danych':
        return 'Brak danych'
    for stan in dane_pomiarowe_stanowisko:
        if stan['key'] == 'PM10':
            czy_jest_pm10 = 1
            values = stan['values']
            pm_prawie_dobowy = 0
            ilosc_na_dobe = 0
            pm_dobowy = 0
            for dv in values[0:25]:
                if dv['value'] != None:
                    ilosc_na_dobe = ilosc_na_dobe + 1
                    pm_prawie_dobowy = pm_prawie_dobowy + dv['value']
                    pm_dobowy = pm_prawie_dobowy/ilosc_na_dobe
            if pm_dobowy > 0 and pm_dobowy < 50:
                poziom = 'w normie'
                napis2 = 'Poziom pyłów drobnych (PM10) jest w normie i wynosi {} µg/m3 \nPoziom dopuszczalny: 50 µg/m3 (dobowy).'.format(pm_dobowy)
            elif pm_dobowy > 50.0 and pm_dobowy < 200.0:
                poziom = 'dopuszczalny'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3 \nPoziom dopuszczalny: 50 µg/m3 (dobowy). Jakość powietrza nie jest dobra, ale nie wywołuje ciężkich skutków dla ludzkiego zdrowia. \n'.format(pm_dobowy)
            elif pm_dobowy > 200.0 and pm_dobowy < 300.0:
                poziom = 'informowania'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3 \nPoziom informowania: 200 µg/m3 (dobowy). Jest źle i trzeba ograniczyć aktywności na powietrzu, bo norma przekroczona jest czterokrotnie. \n'.format(pm_dobowy)
            elif pm_dobowy > 300.0:
                poziom = 'alarmowy'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3. NIE WYCHODŹ!  \nPoziom alarmowy: 300 µg/m3 (dobowy). Jest bardzo źle, norma przekroczona jest sześciokrotnie i należy bezwzględnie ograniczyć przebywanie na powietrzu, a najlepiej zostać w domu, szczególnie osoby chore.\n'.format(pm_dobowy)
        else:
            if czy_jest_pm10 == 0:
                pm_dobowy = 0
                poziom = 'Brak danych'
                napis2 = 'Brak danych'
    zanieczyszczenie.append(pm_dobowy)
    zanieczyszczenie.append(poziom)
    return zanieczyszczenie

#czy_bezpiecznie_wyjsc_z_domu_dla_stacji(400)

def czy_bezpiecznie_wyjsc_z_domu_dla_stacji_teraz(station_id):

    dane_pomiarowe_stanowisko = zanieczyszczenia_dla_stacji(station_id)
    zanieczyszczenie = []
    czy_jest_pm10 = 0
    poziom_aktualny = 0
    napis2 = 'brak danych'
    poziom = 'brak danych'
    if dane_pomiarowe_stanowisko == 'Brak danych':
        return 'Brak danych'
    for stan in dane_pomiarowe_stanowisko:
        if stan['key'] == 'PM10':
            czy_jest_pm10 = 1
            values = stan['values']
            for dv in values:
                if dv['value'] != None:
                    #print(dv['date'], dv['value'])
                    poziom_aktualny = dv['value']
                    break
            if poziom_aktualny > 0 and poziom_aktualny < 50:
                poziom = 'w normie'
                napis2 = 'Poziom pyłów drobnych (PM10) jest w normie i wynosi {} µg/m3 \nPoziom dopuszczalny: 50 µg/m3 (dobowy).'.format(poziom_aktualny)
            elif poziom_aktualny > 50.0 and poziom_aktualny < 200.0:
                poziom = 'dopuszczalny'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3 \nPoziom dopuszczalny: 50 µg/m3 (dobowy). Jakość powietrza nie jest dobra, ale nie wywołuje ciężkich skutków dla ludzkiego zdrowia. \n'.format(poziom_aktualny)
            elif poziom_aktualny > 200.0 and poziom_aktualny < 300.0:
                poziom = 'informowania'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3 \nPoziom informowania: 200 µg/m3 (dobowy). Jest źle i trzeba ograniczyć aktywności na powietrzu, bo norma przekroczona jest czterokrotnie. \n'.format(poziom_aktualny)
            elif poziom_aktualny > 300.0:
                poziom = 'alarmowy'
                napis2 = 'Poziom pyłów drobnych (PM10) wynosi {} µg/m3. NIE WYCHODŹ!  \nPoziom alarmowy: 300 µg/m3 (dobowy). Jest bardzo źle, norma przekroczona jest sześciokrotnie i należy bezwzględnie ograniczyć przebywanie na powietrzu, a najlepiej zostać w domu, szczególnie osoby chore.\n'.format(poziom_aktualny)
        else:
            if czy_jest_pm10 == 0:
                poziom_aktualny = 0
                poziom = 'Brak danych'
                napis2 = 'Brak danych'
    zanieczyszczenie.append(poziom_aktualny)
    zanieczyszczenie.append(poziom)
    zanieczyszczenie.append(poziom_aktualny)
    return zanieczyszczenie

#czy_bezpiecznie_wyjsc_z_domu_dla_stacji_teraz(400)

def current_state_for_city(city):

    #Krok   7:
    #Wyświetl   obecny   stanu   powietrza   dla   danej   miejscowości.
    #Stwórz funkcję current_state_for_city(city), która dla danej miejscowości,
    #dla wszystkich stanowisk   pomiarowych   wyświetli   obecne   wskazania   pomiarowe.

    stacje_pomiarowe = get_measuring_stations_for_city(city)
    for stanowiska in stacje_pomiarowe:
        print(czy_bezpiecznie_wyjsc_z_domu_dla_stacji_teraz(stanowiska))

#current_state_for_city('Kraków')

#print('***************************************** \nKrok   9:    Wyświetlanie   mapy   z   obecnym   stanem. Dla wszystkich dostępnych miast, sprawdzić czy bezpiecznie wyjść z domu i nanieść to na mapę   Polski. Polecana   biblioteka:    https://github.com/python-visualization/folium')

def zanieczyszczenie_na_mapie():
    import folium
    m = folium.Map(location=[52, 19], zoom_start=6)
    wszystko = get_measuring_stations()
    for stacje in wszystko:
        miasto = stacje['city']
        nazwa_stacji = stacje['stationName']
        if miasto == None:
            miasto = nazwa_stacji
            continue
        nazwa_miasta = miasto['name']
        szerokosc = float(stacje['gegrLat'])
        dlugosc = float(stacje['gegrLon'])
        station_id = stacje['id']
        zanieczyszczenie_stacje = czy_bezpiecznie_wyjsc_z_domu_dla_stacji(station_id)
        #czy_bezpiecznie_wyjsc_z_domu_dla_stacji -> pokazuje dobowe wyniki pomiarów pm10
        #czy_bezpiecznie_wyjsc_z_domu_dla_stacji_teraz -> pokazuje aktualne wyniki pomiarów pm10
        if zanieczyszczenie_stacje == 'Brak danych':
            continue
        poziom_stacje = zanieczyszczenie_stacje[1]
        poziom_stacje_ile = str(zanieczyszczenie_stacje[0])
        print(dlugosc, szerokosc, poziom_stacje)
        if poziom_stacje == None:
            continue
        if poziom_stacje =='w normie':
            folium.Marker([szerokosc, dlugosc], popup=nazwa_stacji +', '+nazwa_miasta +' Poziom zanieczyszczenia: ' +poziom_stacje + ' ' + poziom_stacje_ile, icon=folium.Icon(color='green', icon='cloud')).add_to(m)
        elif poziom_stacje =='dopuszczalny':
            folium.Marker([szerokosc, dlugosc], popup=nazwa_stacji +', ' +nazwa_miasta +' Poziom zanieczyszczenia: ' +poziom_stacje + ' ' + poziom_stacje_ile, icon=folium.Icon(color='orange', icon='cloud')).add_to(m)
        elif poziom_stacje == 'informowania':
            folium.Marker([szerokosc, dlugosc], popup=nazwa_stacji +', ' +nazwa_miasta +' Poziom zanieczyszczenia: ' +poziom_stacje + ' ' + poziom_stacje_ile, icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        elif poziom_stacje == 'alarmowy':
            folium.Marker([szerokosc, dlugosc], popup=nazwa_stacji +', ' +nazwa_miasta +' Poziom zanieczyszczenia: ' +poziom_stacje + ' ' + poziom_stacje_ile, icon=folium.Icon(color='black', icon='cloud')).add_to(m)
    return m.save('zanieczyszczenie.html')

zanieczyszczenie_na_mapie()

#print('Krok   8   -opcjonalny-:    Dla   wybranej   stacji   narysuj   historię   pomiarów   z   czujników Poczytaj o matplotlib. Przy użyciu pythona narysuj wykres poziomu zanieczyszczeń od czasu.')

def historia_pomiarow_dla_stacji(station_id):
    import matplotlib.pyplot as plt
    zanieczyszczenia = zanieczyszczenia_dla_stacji(station_id)
    for zaniecz in zanieczyszczenia:
        nazwa_z=zaniecz['key']
        values = zaniecz['values']
        value_wszystkie = []
        date_wszystkie = []
        for v in values:
            vw=value_wszystkie.append(v['value'])
            dw=date_wszystkie.append(v['date'])
            wykres1 = plt.plot(date_wszystkie, value_wszystkie, '-co')
            plt.ylabel(nazwa_z)
            plt.xticks(rotation='vertical')
        plt.show()
#nr_stacji = input("Podaj numer stacji, dla której wyswietlona zostanie historia pomiarów: ")
#historia_pomiarow_dla_stacji(nr_stacji)
