# -*- coding: utf-8 -*-
"""
_robocze fragmenty kodu
"""
#%%

import time, datetime
a = datetime.datetime.now()
time.sleep(0.5)
b = datetime.datetime.now()
delta = b - a
print(delta)
print(delta.total_seconds())
#%%

import time
z  = time.gmtime()
z4 = time.gmtime()[4]
z5 = time.gmtime()[5]
z6 = time.gmtime()[6]
print(time.strftime("%Y-%m-%d at %H:%M:%S (%a)"))
#%%
def dodaj (linia, zapytanie):
    global numer_linii
    try:
        numer_linii
    except:
        numer_linii=1
    zapytanie.append((numer_linii,linia))
    numer_linii+=1
    return zapytanie
#%%
warunek = 'nr_klienta6 is null'
a=['0','1','2','3','4','5','P', '^(190|192)$', 'do testu DSQL:2']
koldmpk=['ID_POZYCJI_RAPORTOWEJ']

ind=0
for i,j in zip(a[6::2],a[7::2]):
#    print(i,j)
    linia1=str()
    if i=='P':
        op = 'and'
    elif i=='N':
        op = 'and not '
    else:
        op = '*ERR*'
    linia1='when '+warunek+" "+op+" regexp_like("+koldmpk[ind]+",'"+j+"')"
    print(linia1)
#oper='P'	
#wart='^(190|192)$'
#%%
def z_wark(dmpkrek=list()): # na wejściu lista (rekord słownika DMPK)
    warunek = dmpkrek[5]
    reszta  = dmpkrek[6:-1]
    ind=0
    for opw,war in zip(reszta[0::2],reszta[1::2]):
        if opw=='P':
            op='and'
        elif opw=='N':
            op='and not'
        whenk = op + war
    ind+=1
    dodatek = warunek + ' **regexp** ' + whenk #  to_do: wykorzystanie dmpkattrcols[ind]
    return dodatek # np. and ID_POZ regexp '^(190|192)$'

dmpkattr=['A0','A1','A2','A3','CZY_WARUNEK','WIDP','ID_POZ','KOMENTARZ']
dmpkattrcols=['ID_POZ']
rek = ['0','1','2','3','2','nr_klienta6 is null','P','^(190|192)$','test']
#print(rek[6:-1])
print(z_wark(rek))

#%%
# zamiast *** rekord_slownika[5] *** będzie to samo z dodanym rekord_slownika_kolumnowe(rekord_slownika)

for rekord_slownika in dmpk:
    if rekord_slownika[4]==2:
        rekord = list(rekord_slownika)
        print(rekord[0:3],rekord[5],rekord[6:-1])
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
dmpk=z_bazy('select * from '+slownik_w_bazie)
sql="SELECT   table_name, column_name                          \
     FROM     all_tab_columns                                  \
     WHERE    owner='BSF' and table_name='"+slownik_w_bazie+"' \
     ORDER BY column_id"
cols  = z_bazy(sql)
dmpkattr = [rekord[1] for rekord in cols]
dmpkattrcols = list()
for i in zip(dmpkattr[7::2]):
    dmpkattrcols.append(i[0])
#podwójna pętla: po rekordach słownika, po atrybutach kolumnowych
#będzie użyta przy wyborze i w klauzuli case
for rekord in dmpk:
    # zaczynam od atrybutu nr 6
    i=6
    for attr in dmpkattrcols:
        atrybut =attr
        operator=rekord[i]
        wartosc =rekord[i+1][0:20]
        print(atrybut,operator,wartosc)