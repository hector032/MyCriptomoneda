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
    criptomonedas = [ 'ETH', 'LTC', 'BNB', 'EOS', 'XLM','TRX','BTC','XRP','BCH','BSV','ADA']
    for moneda in criptomonedas:

        query1 =  "SELECT sum(cantidad_to) as total_to FROM movimientos WHERE moneda_to =? ;"
        resultado1 = dbManager.consultaMuchasSQL(query1,[moneda])

        query2= "SELECT sum(cantidad_from) as total_from FROM movimientos WHERE moneda_from =? ;" 
        resultado2 = dbManager.consultaMuchasSQL(query2,[moneda])
        
        compras = 0
        if len(resultado1) > 0 and resultado1[0]['total_to'] != None   :
            compras = resultado1[0]['total_to']
    
        ventas = 0
        if len(resultado2) > 0 and resultado2[0]['total_from'] != None :
            ventas = resultado2[0]['total_from']
        
        saldo_por_moneda = 0
        if compras > 0 or ventas > 0:       
            saldo_por_moneda=compras - ventas
        
        if saldo_por_moneda > 0:
            
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
                                #print (data)                     
                                valorEnEuroPorCriptoMoneda += data["data"]["quote"]["EUR"]["price"]                
                except (ConnectionError) as e:
                    print(e)
    return valorEnEuroPorCriptoMoneda

