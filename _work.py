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
