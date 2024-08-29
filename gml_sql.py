import sqlite3
import os
from gml_xlsx import save_xlsx

def read_sqlite_query(bdict, path, delete: bool = False, uzytki = None):

    db_path = path + '.db'

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    relacja = dict()

    selection = '''SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
    				concat(EGB_UdzialWeWlasnosci.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
    				EGB_UdzialWeWlasnosci.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
    				EGB_UdzialWeWlasnosci.rodzajPrawa AS [RODZAJ WŁASNOŚCI],
    				'F' as [Typ osoby],
                	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
    				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
    				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
    				'' AS [Krótka nazwa],
    				'' AS regon,				
                	EGB_OsobaFizyczna.pierwszeImie, 
        			EGB_OsobaFizyczna.drugieImie,
                	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
        			EGB_OsobaFizyczna.drugiCzlonNazwiska,
        			EGB_OsobaFizyczna.imieOjca,
        			EGB_OsobaFizyczna.imieMatki,
        			EGB_OsobaFizyczna.pesel,
    				EGB_AdresZameldowania.ulica,
    				EGB_AdresZameldowania.numerPorzadkowy,
    				EGB_AdresZameldowania.numerLokalu,
    				EGB_AdresZameldowania.kodPocztowy,
    				EGB_AdresZameldowania.miejscowosc,
    				'' AS INNE
                    FROM ((((EGB_DzialkaEwidencyjna 
                    LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                    ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_UdzialWeWlasnosci ON
            		EGB_UdzialWeWlasnosci.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_OsobaFizyczna ON
            		EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_UdzialWeWlasnosci.osobaFizyczna)
        			LEFT JOIN EGB_AdresZameldowania ON
        			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
        			UNION
        			SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej, 
    				concat(EGB_UdzialWeWlasnosci.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
    				EGB_UdzialWeWlasnosci.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
    				EGB_UdzialWeWlasnosci.rodzajPrawa AS [RODZAJ WŁASNOŚCI],
    				'M' as [Typ osoby],
                	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
    				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
    				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
    				'' AS [Krótka nazwa],
    				'' AS regon,
                	EGB_OsobaFizyczna.pierwszeImie, 
        			EGB_OsobaFizyczna.drugieImie,
                	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
        			EGB_OsobaFizyczna.drugiCzlonNazwiska,
        			EGB_OsobaFizyczna.imieOjca,
        			EGB_OsobaFizyczna.imieMatki,
        			EGB_OsobaFizyczna.pesel,
    				EGB_AdresZameldowania.ulica,
    				EGB_AdresZameldowania.numerPorzadkowy,
    				EGB_AdresZameldowania.numerLokalu,
    				EGB_AdresZameldowania.kodPocztowy,
    				EGB_AdresZameldowania.miejscowosc,
    				'' AS INNE
                    FROM (((((EGB_DzialkaEwidencyjna 
                    LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                    ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_UdzialWeWlasnosci ON
            		EGB_UdzialWeWlasnosci.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_Malzenstwo ON
            		EGB_Malzenstwo.EGB_IdentyfikatorIIP = EGB_UdzialWeWlasnosci.malzenstwo)
        			INNER JOIN EGB_OsobaFizyczna ON
        			EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna2)
        			LEFT JOIN EGB_AdresZameldowania ON
        			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
        			UNION
        			SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
    				concat(EGB_UdzialWeWlasnosci.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
    				EGB_UdzialWeWlasnosci.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
    				EGB_UdzialWeWlasnosci.rodzajPrawa AS [RODZAJ WŁASNOŚCI],
    				'M' as [Typ osoby],
                	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP, 
    				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
    				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
    				'' AS [Krótka nazwa],
    				'' AS regon,
                	EGB_OsobaFizyczna.pierwszeImie, 
        			EGB_OsobaFizyczna.drugieImie,
                	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
        			EGB_OsobaFizyczna.drugiCzlonNazwiska,
        			EGB_OsobaFizyczna.imieOjca,
        			EGB_OsobaFizyczna.imieMatki,
        			EGB_OsobaFizyczna.pesel,
    				EGB_AdresZameldowania.ulica,
    				EGB_AdresZameldowania.numerPorzadkowy,
    				EGB_AdresZameldowania.numerLokalu,
    				EGB_AdresZameldowania.kodPocztowy,
    				EGB_AdresZameldowania.miejscowosc,
    				'' AS INNE
                    FROM (((((EGB_DzialkaEwidencyjna 
                    LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                    ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_UdzialWeWlasnosci ON
            		EGB_UdzialWeWlasnosci.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_Malzenstwo ON
            		EGB_Malzenstwo.EGB_IdentyfikatorIIP = EGB_UdzialWeWlasnosci.malzenstwo)
        			INNER JOIN EGB_OsobaFizyczna ON
        			EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna3)
        			LEFT JOIN EGB_AdresZameldowania ON
        			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
    				UNION
    				SELECT
    				EGB_DzialkaEwidencyjna.idDzialki, 
    				EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
    				concat(EGB_UdzialWeWlasnosci.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
    				EGB_UdzialWeWlasnosci.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
    				EGB_UdzialWeWlasnosci.rodzajPrawa AS [RODZAJ WŁASNOŚCI],
    				'P' as [Typ osoby],
    				EGB_Instytucja.EGB_IdentyfikatorIIP, 
    				EGB_Instytucja.nazwaPelna AS Nazwa,
    				EGB_Instytucja.nazwaSkrocona AS [Krótka nazwa],
    				EGB_Instytucja.regon,
    				'' AS pierwszeImie, 
        			'' AS drugieImie,
                	'' AS pierwszyCzlonNazwiska,
        			'' AS drugiCzlonNazwiska,
        			'' AS imieOjca,
        			'' AS imieMatki,
        			'' AS pesel,
    				EGB_AdresZameldowania.ulica,
    				EGB_AdresZameldowania.numerPorzadkowy,
    				EGB_AdresZameldowania.numerLokalu,
    				EGB_AdresZameldowania.kodPocztowy,
    				EGB_AdresZameldowania.miejscowosc,
    				'' AS INNE
    				FROM ((((EGB_DzialkaEwidencyjna 
                    LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                    ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_UdzialWeWlasnosci ON
            		EGB_UdzialWeWlasnosci.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                	INNER JOIN EGB_Instytucja ON
            		EGB_Instytucja.EGB_IdentyfikatorIIP = EGB_UdzialWeWlasnosci.instytucja1)
        			LEFT JOIN EGB_AdresZameldowania ON
        			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_Instytucja.adresInstytucji)
        			UNION
                    SELECT
                    EGB_DzialkaEwidencyjna.idDzialki, 
                    EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
                    concat(EGB_UdzialWeWlasnosci.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
                    EGB_UdzialWeWlasnosci.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
                    EGB_UdzialWeWlasnosci.rodzajPrawa AS [RODZAJ WŁASNOŚCI],
                    'G' as [Typ osoby],
                    EGB_PodmiotGrupowy.EGB_IdentyfikatorIIP, 
                    EGB_PodmiotGrupowy.nazwaPelna AS Nazwa,
                    EGB_PodmiotGrupowy.nazwaSkrocona AS [Krótka nazwa],
                    '' AS regon,
                    '' AS pierwszeImie, 
                    '' AS drugieImie,
                    '' AS pierwszyCzlonNazwiska,
                    '' AS drugiCzlonNazwiska,
                    '' AS imieOjca,
                    '' AS imieMatki,
                    '' AS pesel,
                    '' AS ulica,
                    '' AS numerPorzadkowy,
                    '' AS numerLokalu,
                    '' AS kodPocztowy,
                    '' AS miejscowosc,
                    concat(EGB_PodmiotGrupowy.osobaFizyczna4, ' ',
                        EGB_PodmiotGrupowy.instytucja, ' ',
                        EGB_PodmiotGrupowy.malzenstwo3) AS INNE
                    FROM ((((EGB_DzialkaEwidencyjna 
                    LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                    ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                    INNER JOIN EGB_UdzialWeWlasnosci ON
                    EGB_UdzialWeWlasnosci.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                    INNER JOIN EGB_PodmiotGrupowy ON
                    EGB_PodmiotGrupowy.EGB_IdentyfikatorIIP = EGB_UdzialWeWlasnosci.podmiotGrupowy))
        			;'''


    dzialki_wlasciciele = get_query(cursor, selection)
    dzialki_wlasciciele2 = []

    RodzajPrawa = {1: "własność", 2: "władanie samoistne"}
    for dw in dzialki_wlasciciele:
        dw['RODZAJ WŁASNOŚCI'] = RodzajPrawa[int(dw['RODZAJ WŁASNOŚCI'])]
        dzialki_wlasciciele2.append(dw)

        if len(dw['INNE']) > 4:
            list_v = dw['INNE'].split(' ')
            list_value = ''
            for lv in list_v:
                if len(lv) < 4:
                    continue
                list_value = f"{list_value}'{lv}',"

            while ",," in list_value:
                list_value = list_value.replace(',,', ',')
            list_value = list_value.replace("''", '')
            if list_value.endswith(','):
                list_value = list_value[:-1]

            list_value = list_value.replace(',', ', ')

            selection = f'''SELECT
            						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
            						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
            						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
            						'' AS [Krótka nazwa],
            						'' AS regon,				
            						EGB_OsobaFizyczna.pierwszeImie, 
            						EGB_OsobaFizyczna.drugieImie,
            						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
            						EGB_OsobaFizyczna.drugiCzlonNazwiska,
            						EGB_OsobaFizyczna.imieOjca,
            						EGB_OsobaFizyczna.imieMatki,
            						EGB_OsobaFizyczna.pesel,
            						EGB_AdresZameldowania.ulica,
            						EGB_AdresZameldowania.numerPorzadkowy,
            						EGB_AdresZameldowania.numerLokalu,
            						EGB_AdresZameldowania.kodPocztowy,
            						EGB_AdresZameldowania.miejscowosc,
                                   '' AS INNE
                                   FROM EGB_OsobaFizyczna LEFT JOIN EGB_AdresZameldowania ON
            						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej WHERE
            					    EGB_OsobaFizyczna.EGB_IdentyfikatorIIP IN ({list_value})
            					   UNION
            					    SELECT
            						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
            						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
            						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
            						'' AS [Krótka nazwa],
            						'' AS regon,				
            						EGB_OsobaFizyczna.pierwszeImie, 
            						EGB_OsobaFizyczna.drugieImie,
            						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
            						EGB_OsobaFizyczna.drugiCzlonNazwiska,
            						EGB_OsobaFizyczna.imieOjca,
            						EGB_OsobaFizyczna.imieMatki,
            						EGB_OsobaFizyczna.pesel,
            						EGB_AdresZameldowania.ulica,
            						EGB_AdresZameldowania.numerPorzadkowy,
            						EGB_AdresZameldowania.numerLokalu,
            						EGB_AdresZameldowania.kodPocztowy,
            						EGB_AdresZameldowania.miejscowosc,
                                   '' AS INNE
                                   FROM ((EGB_Malzenstwo
            						INNER JOIN EGB_OsobaFizyczna ON
            						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna2)
            					   LEFT JOIN EGB_AdresZameldowania ON
            						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
            						 WHERE EGB_Malzenstwo.EGB_IdentyfikatorIIP IN ({list_value})
            					   UNION
            					   	SELECT
            						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
            						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
            						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
            						'' AS [Krótka nazwa],
            						'' AS regon,				
            						EGB_OsobaFizyczna.pierwszeImie, 
            						EGB_OsobaFizyczna.drugieImie,
            						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
            						EGB_OsobaFizyczna.drugiCzlonNazwiska,
            						EGB_OsobaFizyczna.imieOjca,
            						EGB_OsobaFizyczna.imieMatki,
            						EGB_OsobaFizyczna.pesel,
            						EGB_AdresZameldowania.ulica,
            						EGB_AdresZameldowania.numerPorzadkowy,
            						EGB_AdresZameldowania.numerLokalu,
            						EGB_AdresZameldowania.kodPocztowy,
            						EGB_AdresZameldowania.miejscowosc,
                                   '' AS INNE
                                   FROM ((EGB_Malzenstwo 
            						INNER JOIN EGB_OsobaFizyczna ON
            						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna3)
            					   LEFT JOIN EGB_AdresZameldowania ON
            						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
            						WHERE EGB_Malzenstwo.EGB_IdentyfikatorIIP IN ({list_value})
            					   UNION
            					   SELECT
            						EGB_Instytucja.EGB_IdentyfikatorIIP, 
            						EGB_Instytucja.nazwaPelna AS Nazwa,
            						EGB_Instytucja.nazwaSkrocona AS [Krótka nazwa],
            						EGB_Instytucja.regon,
            						'' AS pierwszeImie, 
            						'' AS drugieImie,
            						'' AS pierwszyCzlonNazwiska,
            						'' AS drugiCzlonNazwiska,
            						'' AS imieOjca,
            						'' AS imieMatki,
            						'' AS pesel,
            						EGB_AdresZameldowania.ulica,
            						EGB_AdresZameldowania.numerPorzadkowy,
            						EGB_AdresZameldowania.numerLokalu,
            						EGB_AdresZameldowania.kodPocztowy,
            						EGB_AdresZameldowania.miejscowosc,
                                   '' AS INNE
                                   FROM (EGB_Instytucja
            					   LEFT JOIN EGB_AdresZameldowania ON
            						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_Instytucja.adresInstytucji)
            						WHERE EGB_Instytucja.EGB_IdentyfikatorIIP IN ({list_value});'''

            # print(selection)
            persons = get_query(cursor, selection)
            # print(persons)

            for person in persons:
                for key, val in dw.items():
                    if key not in person.keys():
                        person[key] = val

                dzialki_wlasciciele2.append(person)


    # relacja = {'Działki_Właściciele': dzialki_wlasciciele2}

    selection = '''SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                   	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
       				concat(EGB_UdzialWeWladaniu.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
       				EGB_UdzialWeWladaniu.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
       				EGB_UdzialWeWladaniu.rodzajWladania AS [RODZAJ WŁASNOŚCI],
       				'F' as [Typ osoby],
                   	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
       				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
       				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
       				'' AS [Krótka nazwa],
       				'' AS regon,				
                   	EGB_OsobaFizyczna.pierwszeImie, 
           			EGB_OsobaFizyczna.drugieImie,
                   	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
           			EGB_OsobaFizyczna.drugiCzlonNazwiska,
           			EGB_OsobaFizyczna.imieOjca,
           			EGB_OsobaFizyczna.imieMatki,
           			EGB_OsobaFizyczna.pesel,
       				EGB_AdresZameldowania.ulica,
       				EGB_AdresZameldowania.numerPorzadkowy,
       				EGB_AdresZameldowania.numerLokalu,
       				EGB_AdresZameldowania.kodPocztowy,
       				EGB_AdresZameldowania.miejscowosc,
       				'' AS INNE
                       FROM ((((EGB_DzialkaEwidencyjna 
                       LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                       ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_UdzialWeWladaniu ON
               		EGB_UdzialWeWladaniu.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_OsobaFizyczna ON
               		EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_UdzialWeWladaniu.osobaFizyczna)
           			LEFT JOIN EGB_AdresZameldowania ON
           			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
           			UNION
           			SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                   	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej, 
       				concat(EGB_UdzialWeWladaniu.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
       				EGB_UdzialWeWladaniu.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
       				EGB_UdzialWeWladaniu.rodzajWladania AS [RODZAJ WŁASNOŚCI],
       				'M' as [Typ osoby],
                   	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
       				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
       				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
       				'' AS [Krótka nazwa],
       				'' AS regon,
                   	EGB_OsobaFizyczna.pierwszeImie, 
           			EGB_OsobaFizyczna.drugieImie,
                   	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
           			EGB_OsobaFizyczna.drugiCzlonNazwiska,
           			EGB_OsobaFizyczna.imieOjca,
           			EGB_OsobaFizyczna.imieMatki,
           			EGB_OsobaFizyczna.pesel,
       				EGB_AdresZameldowania.ulica,
       				EGB_AdresZameldowania.numerPorzadkowy,
       				EGB_AdresZameldowania.numerLokalu,
       				EGB_AdresZameldowania.kodPocztowy,
       				EGB_AdresZameldowania.miejscowosc,
       				'' AS INNE
                       FROM (((((EGB_DzialkaEwidencyjna 
                       LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                       ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_UdzialWeWladaniu ON
               		EGB_UdzialWeWladaniu.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_Malzenstwo ON
               		EGB_Malzenstwo.EGB_IdentyfikatorIIP = EGB_UdzialWeWladaniu.malzenstwo)
           			INNER JOIN EGB_OsobaFizyczna ON
           			EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna2)
           			LEFT JOIN EGB_AdresZameldowania ON
           			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
           			UNION
           			SELECT EGB_DzialkaEwidencyjna.idDzialki, 
                   	EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
       				concat(EGB_UdzialWeWladaniu.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
       				EGB_UdzialWeWladaniu.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
       				EGB_UdzialWeWladaniu.rodzajWladania AS [RODZAJ WŁASNOŚCI],
       				'M' as [Typ osoby],
                   	EGB_OsobaFizyczna.EGB_IdentyfikatorIIP, 
       				concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
       				EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
       				'' AS [Krótka nazwa],
       				'' AS regon,
                   	EGB_OsobaFizyczna.pierwszeImie, 
           			EGB_OsobaFizyczna.drugieImie,
                   	EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
           			EGB_OsobaFizyczna.drugiCzlonNazwiska,
           			EGB_OsobaFizyczna.imieOjca,
           			EGB_OsobaFizyczna.imieMatki,
           			EGB_OsobaFizyczna.pesel,
       				EGB_AdresZameldowania.ulica,
       				EGB_AdresZameldowania.numerPorzadkowy,
       				EGB_AdresZameldowania.numerLokalu,
       				EGB_AdresZameldowania.kodPocztowy,
       				EGB_AdresZameldowania.miejscowosc,
       				'' AS INNE
                       FROM (((((EGB_DzialkaEwidencyjna 
                       LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                       ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_UdzialWeWladaniu ON
               		EGB_UdzialWeWladaniu.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_Malzenstwo ON
               		EGB_Malzenstwo.EGB_IdentyfikatorIIP = EGB_UdzialWeWladaniu.malzenstwo)
           			INNER JOIN EGB_OsobaFizyczna ON
           			EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna3)
           			LEFT JOIN EGB_AdresZameldowania ON
           			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
       				UNION
       				SELECT
       				EGB_DzialkaEwidencyjna.idDzialki, 
       				EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
       				concat(EGB_UdzialWeWladaniu.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
       				EGB_UdzialWeWladaniu.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
       				EGB_UdzialWeWladaniu.rodzajWladania AS [RODZAJ WŁASNOŚCI],
       				'P' as [Typ osoby],
       				EGB_Instytucja.EGB_IdentyfikatorIIP, 
       				EGB_Instytucja.nazwaPelna AS Nazwa,
       				EGB_Instytucja.nazwaSkrocona AS [Krótka nazwa],
       				EGB_Instytucja.regon,
       				'' AS pierwszeImie, 
           			'' AS drugieImie,
                   	'' AS pierwszyCzlonNazwiska,
           			'' AS drugiCzlonNazwiska,
           			'' AS imieOjca,
           			'' AS imieMatki,
           			'' AS pesel,
       				EGB_AdresZameldowania.ulica,
       				EGB_AdresZameldowania.numerPorzadkowy,
       				EGB_AdresZameldowania.numerLokalu,
       				EGB_AdresZameldowania.kodPocztowy,
       				EGB_AdresZameldowania.miejscowosc,
       				'' AS INNE
       				FROM ((((EGB_DzialkaEwidencyjna 
                       LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                       ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_UdzialWeWladaniu ON
               		EGB_UdzialWeWladaniu.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                   	INNER JOIN EGB_Instytucja ON
               		EGB_Instytucja.EGB_IdentyfikatorIIP = EGB_UdzialWeWladaniu.instytucja1)
           			LEFT JOIN EGB_AdresZameldowania ON
           			EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_Instytucja.adresInstytucji)
           			UNION
                       SELECT
                       EGB_DzialkaEwidencyjna.idDzialki, 
                       EGB_JednostkaRejestrowaGruntow.idJednostkiRejestrowej,
                       concat(EGB_UdzialWeWladaniu.licznikUlamkaOkreslajacegoWartoscUdzialu,'/',
                       EGB_UdzialWeWladaniu.mianownikUlamkaOkreslajacegoWartoscUdzialu) AS Udzial,
                       EGB_UdzialWeWladaniu.rodzajWladania AS [RODZAJ WŁASNOŚCI],
                       'G' as [Typ osoby],
                       EGB_PodmiotGrupowy.EGB_IdentyfikatorIIP, 
                       EGB_PodmiotGrupowy.nazwaPelna AS Nazwa,
                       EGB_PodmiotGrupowy.nazwaSkrocona AS [Krótka nazwa],
                       '' AS regon,
                       '' AS pierwszeImie, 
                       '' AS drugieImie,
                       '' AS pierwszyCzlonNazwiska,
                       '' AS drugiCzlonNazwiska,
                       '' AS imieOjca,
                       '' AS imieMatki,
                       '' AS pesel,
                       '' AS ulica,
                       '' AS numerPorzadkowy,
                       '' AS numerLokalu,
                       '' AS kodPocztowy,
                       '' AS miejscowosc,
                       concat(EGB_PodmiotGrupowy.osobaFizyczna4, ' ',
                        EGB_PodmiotGrupowy.instytucja, ' ',
                        EGB_PodmiotGrupowy.malzenstwo3) AS INNE
                       FROM ((((EGB_DzialkaEwidencyjna 
                       LEFT JOIN EGB_JednostkaRejestrowaGruntow 
                       ON EGB_DzialkaEwidencyjna.JRG2 = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                       INNER JOIN EGB_UdzialWeWladaniu ON
                       EGB_UdzialWeWladaniu.JRG = EGB_JednostkaRejestrowaGruntow.EGB_IdentyfikatorIIP)
                       INNER JOIN EGB_PodmiotGrupowy ON
                       EGB_PodmiotGrupowy.EGB_IdentyfikatorIIP = EGB_UdzialWeWladaniu.podmiotGrupowy))
           			;'''

    dzialki_wladajacy = get_query(cursor, selection)
    dzialki_wladajacy2 = []

    RodzajWladania = {1: "użytkowanie wieczyste", 2: "trwaly zarząd", 3: "zarząd", 4: "użytkowanie",
                      5: "inny rodzaj władania", 6: "wykonywanie prawa wlasnosci SP i innych praw rzeczowych",
                      7: "gospodarowanie zasobem nieruchomosci SP Lub Gminy, Powiatu, Województwa",
                      8: "gospodarowanie gruntem SP pokrytym wodami powierzchniowymi",
                      9: "wykonywanie zadan zarzadcy dróg publicznych"}
    for dw in dzialki_wladajacy:
        dw['RODZAJ WŁASNOŚCI'] = RodzajWladania[int(dw['RODZAJ WŁASNOŚCI'])]

        dw['regon'] = dw['regon'].replace('000000000','')

        dzialki_wladajacy2.append(dw)

        if len(dw['INNE']) > 4:
            list_v = dw['INNE'].split(' ')
            list_value = ''
            for lv in list_v:
                if len(lv) < 4:
                    continue
                list_value = f"{list_value}'{lv}',"

            while ",," in list_value:
                list_value = list_value.replace(',,', ',')
            list_value = list_value.replace("''", '')
            if list_value.endswith(','):
                list_value = list_value[:-1]

            list_value = list_value.replace(',', ', ')

            # print(list_value)
            selection = f'''SELECT
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
						'' AS [Krótka nazwa],
						'' AS regon,				
						EGB_OsobaFizyczna.pierwszeImie, 
						EGB_OsobaFizyczna.drugieImie,
						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
						EGB_OsobaFizyczna.drugiCzlonNazwiska,
						EGB_OsobaFizyczna.imieOjca,
						EGB_OsobaFizyczna.imieMatki,
						EGB_OsobaFizyczna.pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM EGB_OsobaFizyczna LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej WHERE
					    EGB_OsobaFizyczna.EGB_IdentyfikatorIIP IN ({list_value})
					   UNION
					    SELECT
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
						'' AS [Krótka nazwa],
						'' AS regon,				
						EGB_OsobaFizyczna.pierwszeImie, 
						EGB_OsobaFizyczna.drugieImie,
						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
						EGB_OsobaFizyczna.drugiCzlonNazwiska,
						EGB_OsobaFizyczna.imieOjca,
						EGB_OsobaFizyczna.imieMatki,
						EGB_OsobaFizyczna.pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM ((EGB_Malzenstwo
						INNER JOIN EGB_OsobaFizyczna ON
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna2)
					   LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
						 WHERE EGB_Malzenstwo.EGB_IdentyfikatorIIP IN ({list_value})
					   UNION
					   	SELECT
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
						'' AS [Krótka nazwa],
						'' AS regon,				
						EGB_OsobaFizyczna.pierwszeImie, 
						EGB_OsobaFizyczna.drugieImie,
						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
						EGB_OsobaFizyczna.drugiCzlonNazwiska,
						EGB_OsobaFizyczna.imieOjca,
						EGB_OsobaFizyczna.imieMatki,
						EGB_OsobaFizyczna.pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM ((EGB_Malzenstwo 
						INNER JOIN EGB_OsobaFizyczna ON
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP = EGB_Malzenstwo.osobaFizyczna3)
					   LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej)
						WHERE EGB_Malzenstwo.EGB_IdentyfikatorIIP IN ({list_value})
					   UNION
					   SELECT
						EGB_Instytucja.EGB_IdentyfikatorIIP, 
						EGB_Instytucja.nazwaPelna AS Nazwa,
						EGB_Instytucja.nazwaSkrocona AS [Krótka nazwa],
						EGB_Instytucja.regon,
						'' AS pierwszeImie, 
						'' AS drugieImie,
						'' AS pierwszyCzlonNazwiska,
						'' AS drugiCzlonNazwiska,
						'' AS imieOjca,
						'' AS imieMatki,
						'' AS pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM (EGB_Instytucja
					   LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_Instytucja.adresInstytucji)
						WHERE EGB_Instytucja.EGB_IdentyfikatorIIP IN ({list_value});'''

            # print(selection)
            persons = get_query(cursor, selection)
            # print(persons)

            for person in persons:
                for key, val in dw.items():
                    if key not in person.keys():
                        person[key] = val

                dzialki_wladajacy2.append(person)


    # relacja['Działki_Władajacy'] = dzialki_wladajacy2

    relacja['Relacja'] = dzialki_wlasciciele2 + dzialki_wladajacy2

    selection = """ SELECT 
    				d.idDzialki AS Identyfikator,
    				d.numerKW AS [Numer KW],
    				d.poleEwidencyjne AS [Pole ewidencyne],
    				d.dokladnoscReprezentacjiPola AS [Precyzja],
    				jrg.idJednostkiRejestrowej AS JRG,
    				concat(adr.nazwaUlicy, ' ',
    				adr.numerPorzadkowy, ' ',
    				adr.numerLokalu, ';', 
    				adr.nazwaMiejscowosci) AS Adres
    				FROM 
    				((EGB_DzialkaEwidencyjna AS d
    				LEFT JOIN EGB_JednostkaRejestrowaGruntow AS jrg
                    ON d.JRG2 = jrg.EGB_IdentyfikatorIIP) LEFT JOIN
    				EGB_AdresNieruchomosci AS adr ON  adr.EGB_IdentyfikatorIIP = d.adresDzialki)
    			"""


    relacja['Działki'] = get_query(cursor, selection)

    selection = '''SELECT
						EGB_OsobaFizyczna.EGB_IdentyfikatorIIP,
						concat(EGB_OsobaFizyczna.pierwszyCzlonNazwiska, ' ' , EGB_OsobaFizyczna.drugiCzlonNazwiska, ' ', 
						EGB_OsobaFizyczna.pierwszeImie) AS Nazwa,
						'' AS [Krótka nazwa],
						'' AS regon,				
						EGB_OsobaFizyczna.pierwszeImie, 
						EGB_OsobaFizyczna.drugieImie,
						EGB_OsobaFizyczna.pierwszyCzlonNazwiska,
						EGB_OsobaFizyczna.drugiCzlonNazwiska,
						EGB_OsobaFizyczna.imieOjca,
						EGB_OsobaFizyczna.imieMatki,
						EGB_OsobaFizyczna.pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM EGB_OsobaFizyczna LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_OsobaFizyczna.adresOsobyFizycznej
					   UNION
					   SELECT
						EGB_Instytucja.EGB_IdentyfikatorIIP, 
						EGB_Instytucja.nazwaPelna AS Nazwa,
						EGB_Instytucja.nazwaSkrocona AS [Krótka nazwa],
						EGB_Instytucja.regon,
						'' AS pierwszeImie, 
						'' AS drugieImie,
						'' AS pierwszyCzlonNazwiska,
						'' AS drugiCzlonNazwiska,
						'' AS imieOjca,
						'' AS imieMatki,
						'' AS pesel,
						EGB_AdresZameldowania.ulica,
						EGB_AdresZameldowania.numerPorzadkowy,
						EGB_AdresZameldowania.numerLokalu,
						EGB_AdresZameldowania.kodPocztowy,
						EGB_AdresZameldowania.miejscowosc,
                       '' AS INNE
                       FROM (EGB_Instytucja
					   LEFT JOIN EGB_AdresZameldowania ON
						EGB_AdresZameldowania.EGB_IdentyfikatorIIP = EGB_Instytucja.adresInstytucji);'''

    relacja['Dane_osobowe'] = get_query(cursor, selection)


    selection = """ SELECT 
    				idPunktu AS ID,
    				pos,
    				sposobPozyskania AS SPD,
    				spelnienieWarunkowDokl AS ISD,
    				rodzajStabilizacji AS STB,
    				oznWMaterialeZrodlowym AS OZN,
    				dodatkoweInformacje AS [Informacje]
    				FROM
    				EGB_PunktGraniczny
    			"""

    values = get_query(cursor, selection)
    nvalues = []

    for val in values:
        nval = dict()
        nval['ID'] = val['ID']
        nval['Numer'] = val['ID'].split('.')[-1]
        spl = val['pos'].split(' ')
        x, y = float(spl[0]), float(spl[1])
        nval['x'] = x
        nval['y'] = y
        nval['SPD'] = val['SPD']
        nval['ISD'] = val['ISD']
        nval['STB'] = val['STB']
        nval['OZN'] = val['OZN']
        nval['Info'] = val['Informacje']
        nvalues.append(nval)


    relacja['Punkty_Graniczne'] = nvalues

    # TODO tabela użytki

    cursor = None
    conn.close()
    conn = None


    # save_xlsx(relacja, f"{path}-relacja")

    relacja['Użytki'] = uzytki

    save_xlsx(relacja, f"{path}-relacja")

    if not delete:
        os.remove(db_path)

def save_sqlite(bdict, path, tags):
    path = path + '.db'

    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)

    cursor = conn.cursor()

    create_table = ''
    insert_table = ''
    contents = ''
    j = 0
    for key, val in bdict.items():

        # print(f"loop: {j}")

        j += 1

        if key == 'PrezentacjaGraficzna':
            continue
        create_table = f"CREATE TABLE {key} ("
        insert_table = f"INSERT INTO {key} ("
        i = 0
        col: dict = bdict[key]


        # print(col)

        contents = col

        keyss = tags[key] # col[0].keys()
        for v in tags[key] :
            create_table += f"{v} TEXT, "
            insert_table += f"{v}, "
            i += 1

        create_table = create_table[:-2] + ");"

        # print(f"\nCreate table: {create_table}")
        cursor.execute(create_table)

        qm = "?, " * i
        insert_table = insert_table[:-2] + ") VALUES(" + qm[:-2] + ")"
        # print(f"Insert values: {insert_table}")

        jj = 0
        for con in contents:

            # print(f"loop: {j}, {jj}")
            jj += 1
            """try:
                rec_val = [vv.replace(":", ".") for vv in con.values()]
                #rec_val = [vv.replace("", "-") for vv in con.values()]
            except AttributeError:
                rec_val = [vv for vv in con.values()]"""

            rec_val2 = []
            for kk in keyss:
                if kk in con.keys():
                    rec_val2.append(con[kk])
                else:
                    rec_val2.append('')

            # print(j, len(rec_val2))

            # print(i, len(rec_val))
            cursor.executemany(insert_table, [rec_val2])
            """for rcv in rec_val:
                print(rcv)
                cursor.executemany(insert_table, rcv[:i])"""
    conn.commit()
    conn.close()


def get_query(cursor, selection: str) -> list:

    # print(selection[:20])

    try:
        values = cursor.execute(selection).fetchall()
    except Exception as er:
        print(er)
    # print(*values, sep='\n\n')
    heads = [v[0] for v in cursor.execute(selection).description]
    # print(heads, sep='\n\n')


    fvalues = []
    for v in values:
        fvalues.append(dict(zip(heads, v)))


    return fvalues

if __name__ == "__main__":
    ...