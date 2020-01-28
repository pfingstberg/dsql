# -*- coding: utf-8 -*-
"""
Przetwarzanie słownika D_MAP_PRODUKTY_KORPO do kodu SQL potrzebnego 
w procesie indeksacji produktowej MIS BD
Na potrzeby prototypu słownik jest okrojony do jednej kolumny warunków
Nazwa słownika w bazie w prototypie 'TD_DMPK'
Słownik wczytywany jest do listy tupli 'lista_rekordow' i sortowany do 'dmpk'
Tworzony kod ma służyć do oflagowania rekordów P05 wartością SCIEZKA
oraz przypisać SID_PRODUKTU_MBD, PRIORYTET, PRIORYTET_MAPOWANIA_PROD 
SCIEZKA=2 gdy CZY_WARUNEK=2 /potrzebny postproces indeksacji prod. po kolumnach/
"""
#%%
def z_bazy(sql):
    import cx_Oracle
    con = cx_Oracle.connect('bsf/bsf@localhost:1521/xe',encoding="UTF-8")
    curs = con.cursor()         # pusty kursor
    curs.execute(sql)
    lista_rekordow  = list()    # pusta lista na rekordy
    for rekord in curs:
        lista_rekordow.append(rekord)
    con.close()
    return lista_rekordow
#%%
slownik_w_bazie = 'TD_DMPK' # nazwa słownika w bazie Oracle
tabela_w_bazie  = 'TD_P05'  # nazwa tabeli w bazie

dmpk = z_bazy('select * from '+slownik_w_bazie)
dmpk=sorted(dmpk, key=lambda tup:(tup[4],tup[0],tup[1]))
# słownik jest posortowany po CZY_WARUNEK, PRIORYTET, PRIORYTET_MAPOWANIA_PROD
sql="select TABLE_NAME, COLUMN_NAME from all_tab_columns \
             where owner='BSF' and table_name='"+tabela_w_bazie+"' order by column_id"
cols = z_bazy(sql)
tabela_attr = [rekord[1] for rekord in cols]
#%%
def dodaj (linia, zapytanie):
    global numer_linii
    zapytanie.append((numer_linii,linia))
    numer_linii+=1
    return zapytanie
#%%
"""
konstruowanie tekstu zapytania z rekordów słownika CZY_WARUNEK=1 (podproces P05F1)
select 
*
from BAZA.TABELA
where HDB_ID_BATCH_EXEC = :batch and (
DWARUNEK_01 or
DWARUNEK_02 or
...
DWARUNEK_0n);
"""
BAZA   ='edhd_mis_dmmis_dmi50_rl_temp' # nazwa bazy/schematu
TABELA ='P_M_FAKTY_KORPO_P05'          # nazwa tabeli
BAZA   ='BSF'                          # !! testowo nazwa bazy/schematu
TABELA ='TD_P05'                       # !! testowo nazwa tabeli
BATCH  ='MKM_20190731_005'             # numer batcha
ATRLIS = tabela_attr

zapytanie = list()
numer_linii=1

dodaj('select ',zapytanie)
# -----------------------------------------------------------------------------
for a in ATRLIS:                    # dołączenie do tekstu zapytania wszystkich atrybutów z ATRLIS
    if ATRLIS.index(a) == 0:
        atr='     ' + a
    else:
        atr='  ,  ' + a
    dodaj(atr,zapytanie)
#%%
ile1=sum(rekord_slownika[4]==1 for rekord_slownika in dmpk)
ile2=sum(rekord_slownika[4]==2 for rekord_slownika in dmpk)
# -----------------------------------------------------------------------------!! WRK
# dodanie klauzuli case z której wychodzi SID_PRODUKTU_MBD z sufiksem _F(pozostałe atrybuty produktowe analogicznie)
dodaj('  ,  case',zapytanie)        # dołączenie do tekstu zapytania 'case'
if ile2>0:
    for rekord_slownika in dmpk:
        if rekord_slownika[4] == 2:     # (tylko rekordy słownika mające CZY_WARUNEK=2)
            dodaj('         when '+rekord_slownika[5]+' then '+rekord_slownika[2],zapytanie)
    dodaj('         else null',zapytanie)
else:
    dodaj('         when 1=1 then null',zapytanie)
dodaj('     end as SID_PRODUKTU_MBD_F',zapytanie) # dołączenie do tekstu zapytania 'end as SID_PRODUKTU_MBD_F'
#------------------------------------------------------------------------------
# dodanie klauzuli case z której wychodzi PRIORYTET z sufiksem _F
dodaj('  ,  case',zapytanie)        # dołączenie do tekstu zapytania 'case'
if ile1>0:
    for rekord_slownika in dmpk:
        if rekord_slownika[4] == 2:     # (tylko rekordy słownika mające CZY_WARUNEK=2)
            dodaj('         when '+rekord_slownika[5]+' then '+str(rekord_slownika[0]),zapytanie)
    dodaj('         else null',zapytanie)
else:
    dodaj('         when 1=1 then null',zapytanie)
dodaj('     end as PRIORYTET_F',zapytanie) # dołączenie do tekstu zapytania 'end as PRIORYTET_F'

#------------------------------------------------------------------------------
dodaj('  ,  2   as SCIEZKA',zapytanie)  # bo warunek CZY_WARUNEK porównujemy z 2
dodaj('from ',zapytanie)            # dołączenie do tekstu zapytania 'from'
dodaj(BAZA+'.'+TABELA,zapytanie)    # dołączenie do tekstu zapytania nazwy schematu i tabeli
dodaj("where HDB_ID_BATCH_EXEC='"+BATCH+"' and (1=0",zapytanie) # dołączenie do tekstu zapytania 'where ...'
for rekord_slownika in dmpk:     # dołączenie do tekstu zapytania warunków WARUNEK ze słownika
    if rekord_slownika[4] == 2:     # (tylko rekordy słownika mające CZY_WARUNEK=1)
        dodaj('or '+rekord_slownika[5],zapytanie)
dodaj(')\n;',zapytanie)             # dołączenie do tekstu zapytania ');'
#%%
# zapisanie tekstu zapytania P05F1 do pliku
with open('P05F2.sql','w') as plik:
    for linia in zapytanie:
        plik.write(linia[1]+'\n')
