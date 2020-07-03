# -*- coding: utf-8 -*-
"""
_robocze fragmenty kodu
"""
#%%
import json
with open('bookmarks-2020-06-13.Dell.json','r',encoding='utf-8') as fj:
    tree0 = json.load(fj)
# szukam słownika najniższego poziomu (nie mającego klucza 'children' 
# i odczytuję wartośCI kluczy 'title' i 'uri')
a=tree0['children']     #   lista
tree1=a[0]              #   dict, Bookmarks Menu
tree2=a[1]              #   dict, Bookmarks Toolbar

test  = tree0['children'][0]['children'][12]['children'][8]
testB = tree0['children'][1]['children'][ 1]['children'][2]


if 'children' in [key for key in test]:
    test_t=test['title']
    test_u=test['uri']
else:
    test_t=None
    test_u=None

#print(tree1['root'])
for key in tree1:
    #print(key,type(key),key=='title')
    if key == 'title':
        print(key, tree1[key])

#for key in tree1.keys():
#    print(key)
    
#for key,val in tree1.items():
    #print(key)
    #print(val)
#%%
import pickle 
# Pickle the 'tree0' dictionary using the highest protocol available into file 'tree0.pickl'
with open('tree0.pickle', 'wb') as f: 
      pickle.dump(tree0, f, pickle.HIGHEST_PROTOCOL) 

#%%
import datetime as dt
import time as tm

#dt.datetime.fromtimestamp(tm.time())

dtnow = dt.datetime.fromtimestamp(tm.time())
dtnow

dtnow.year, dtnow.month, dtnow.day, dtnow.hour, dtnow.minute, dtnow.second # get year, month, day, etc.from a datetime
#%%
x = lambda a : a + 10
print(x(5)) 

add = lambda a,b: a+b
print(add(3,6))
#%%
import numpy as np
r=np.array(range(36))
r2=np.reshape(r,(6,6))

w1=r.reshape(36)[::7]
w2=range(36)[::7]
r2[2:4,2:4]
#%%
people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']

def split_title_and_name(person):
    return person.split()[0] + ' ' + person.split()[-1]

#option 1
for person in people:
  print(split_title_and_name(person))
  #print(split_title_and_name(person) == (lambda x: x.split()[0] + ' ' + x.split()[-1])(person))
  #print(   split_title_and_name(person) == (lambda x:x.split()[0]+' '+x.split()[-1](person))      )
  print( (lambda x:x.split()[0]+' '+x.split()[-1]) (person)  )

#option 2
#list(map(split_title_and_name, people)) == list(map(lambda x:x.split()[0]+' '+x.split()[-1]   , people ))
#%%
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

answer = [a+b+c+d for a in lowercase for b in lowercase for c in digits for d in digits]
print (answer)

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
def z_wark(dmpkrek=list(),dmpkattrcols=list()): 
# na wejściu listy: (rekord słownika DMPK) (lista DMPKATTRCOLS atrybutów kolumnowych)
    warunek = dmpkrek[5]
    reszta  = dmpkrek[6:-1]
    ind=0
    dod=''
    for opw,wreg in zip(reszta[0::2],reszta[1::2]): # operator warunku i wyrażenie regularne
        if opw=='P':
            op=' and'
        elif opw=='N':
            op=' and not'
        whenk = op + ' regexp_like(' + dmpkattrcols[ind] + ',' + "'"+wreg +"'"+')'
        dod = dod + whenk
        ind+=1
    dodatek = warunek + dod
    return dodatek # np. and ID_POZ regexp '^(190|192)$'

dmpkattr=['A0','A1','A2','A3','CZY_WARUNEK','WIDP','ID_POZ','WTEST','TESTKOL','KOMENTARZ']
dmpkattrcols=['ID_POZ','TESTKOL']
rek = ['0','1','2','3','2','nr_klienta6 is null','P','^(190|192)$','P','.*','test']
#print(rek[6:-1])
print(z_wark(rek,dmpkattrcols))

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