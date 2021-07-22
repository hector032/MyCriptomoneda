import re
from mycripto.dataaccess import *
from mycripto.forms import *
from mycripto.views import *
from flask import jsonify, render_template, request, redirect, url_for, flash


dbManager = DBmanager()


def verificar_saldo_por_moneda(moneda):
    saldo = 0
    query = "SELECT * from movimientos where moneda_to=?;" 
    compras = dbManager.consultaMuchasSQL(query, [moneda])

    query = "SELECT * From movimientos WHERE moneda_from=?;" 
    ventas = dbManager.consultaMuchasSQL(query, [moneda])

    for suma in compras:
        saldo += suma['cantidad_to']
    for resta in ventas:
        saldo -= resta['cantidad_from']

    return saldo


def saldo_euros_invertidos():
    query =  "SELECT sum(cantidad_to) - sum(cantidad_from) as saldo_euros_ivertidos FROM movimientos WHERE moneda_to='EUR' or moneda_from = ?;"
    parametros = ['EUR']
    resultado = dbManager.consultaMuchasSQL(query,parametros)
    if len(resultado) > 0 :
        return resultado[0]['saldo_euros_ivertidos']        
    else:
        return[]
    

def total_euros_invertidos():
    query =  "SELECT sum(cantidad_from) as total_euros_invertidos FROM movimientos WHERE moneda_from = ?;"
    parametros = ['EUR']
    resultado = dbManager.consultaMuchasSQL(query,parametros)

    if len(resultado) > 0 :
        return resultado[0]['total_euros_invertidos']        
    else:
        return[]

def valor_todas_criptos_euros():
    formulario=MovimientosForm()
    valorEnEuroPorCriptoMoneda = 0
    criptomonedas = ['EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM','TRX','BTC','XRP','BCH','USDT','BSV','ADA']
    for moneda in criptomonedas:
        query =  "SELECT sum(cantidad_to) - sum(cantidad_from) AS valor_todas_criptos_euros FROM movimientos WHERE moneda_from =? AND moneda_to =?;"
        resultado = dbManager.consultaMuchasSQL(query,[moneda,moneda])
        
        if len(resultado) > 0 :
            saldo_por_moneda=resultado[0]['valor_todas_criptos_euros']

            #Hacemos la llamada a la APi para aplicar el convert
            url_convert = api.URL_CRIPTO
            parameters = {
                    'amount':saldo_por_moneda,
                    'symbol':moneda,
                    'convert':'EUR'
            }
            try:
                    response = requests.get(url_convert, params = parameters)
                    if response.status_code==200:
                        data=response.json()
                        if data["status"]["error_code"] != 0:
                            flash("Error de conversion en la API: " + data["status"]["error_message"])
                            return render_template('status.html', form = formulario)
                        else:                            
                            valorEnEuroPorCriptoMoneda += data["data"]["quote"][moneda]["price"]                
            except (ConnectionError) as e:
                print(e)
    return valorEnEuroPorCriptoMoneda

