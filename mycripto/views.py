from sqlite3.dbapi2 import Time
from mycripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from datetime import date, time, datetime
from mycripto.forms import MovimientosForm
import sqlite3
from mycripto import api
from mycripto.dataaccess import *
import json
import requests
import helper
from mycripto.saldos import *



dbManager = DBmanager()


@app.route('/', methods=["GET", "POST"])
def index():
    query = "SELECT * FROM movimientos WHERE 1=1"    
    movimientos = dbManager.consultaMuchasSQL(query,[])

    if not movimientos:
        flash("no hay datos aún")
        
    print(helper.totalMovimientos)
    print("hola")
    for d in movimientos:
        pu =d["cantidad_from"]/d["cantidad_to"]
        d["pu"] = pu

    return render_template('movimientos.html', datos = movimientos)


@app.route('/compra', methods=["GET", "POST"])
def compra():
    formulario=MovimientosForm()

    if request.method == "GET":
        return render_template('purchase.html',form=formulario)

    else:
        if formulario.submit.data == True:
            if formulario.validate():
                        
                query="INSERT INTO movimientos (fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?)"
                print(query)
                try:
                    dbManager.modificaTablaSQL(query,
                        [
                            datetime.now().strftime('%Y-%m-%d'), 
                            datetime.now().strftime('%H:%M:%S'), 
                            formulario.moneda_from.data,
                            formulario.cantidad_from.data,
                            formulario.moneda_to.data, 
                            formulario.cantidad_to.data
                        ]
                    )
                                                            
                except sqlite3.Error as el_error:
                    
                    print("Error en SQL INSERT", el_error)
                    flash("se ha producido un error en la bddd. Pruebe en unos minutos", "error")
                    return render_template('movimientos.html', form=formulario)
                
                return redirect(url_for('index'))
            else:
                return render_template('purchase.html', form=formulario)
        
        elif formulario.calcular_cripto.data == True:

            query = "SELECT * FROM movimientos WHERE 1=1"    
            movimientos = dbManager.consultaMuchasSQL(query,[])
            
            #Verificamos que no tengamos la misma moneda                
            if formulario.moneda_from.data == formulario.moneda_to.data:
                flash("no puedes tranformar una critomoneda en la misma cripto")
                return render_template('purchase.html', form=formulario)            
            #Verificamos que no sea un string o lagun simbolo o este separado por comas ( , )

            #Verificamos que la cantidad from no sea menor o igual a 0
            elif formulario.cantidad_from.data <= 0:
                flash("la cantidad tiene que ser mayor que 0")
                return render_template('purchase.html', form=formulario)

            #Verificamos movimientos y que no sea EUR lera vez
            if not movimientos and formulario.moneda_from.data !='EUR':
                flash("No tienes criptomonedas aún, primero deberas hacer una inversion con EUROS.")
                return render_template('purchase.html', form=formulario)
            #verificamos saldo 

            else:
                query = "SELECT * From movimientos WHERE moneda_to=?;"
                monedaFrom = formulario.moneda_from.data
                datos = [monedaFrom]
                resultado = dbManager.consultaMuchasSQL(query, datos)
                saldo=verificar_saldo_por_moneda(monedaFrom)
                if saldo < float(formulario.cantidad_from.data):
                    flash("Tienes {} {}, para realizar la compra de {} necesitas mas {}" . format(saldo, monedaFrom,  formulario.moneda_to.data, monedaFrom))
                    return render_template('purchase.html', form=formulario)



            #Hacemos la llamada a la APi para aplicar el convert
            url_convert = api.URL_CRIPTO
            parameters = {
                'amount':formulario.cantidad_from.data,
                'symbol':formulario.moneda_from.data,
                'convert':formulario.moneda_to.data
            }
            formulario.cantidad_from.data
            print(url_convert)
            print(parameters)
            try:
                    response = requests.get(url_convert, params = parameters)
                    if response.status_code==200:
                        data=response.json()
                        if data["status"]["error_code"] != 0:
                            flash("Error de conversion en la API: " + data["status"]["error_message"])
                            return render_template('purchase.html', form = formulario)
                        else:                            
                            cantidadFinal= data["data"]["quote"][formulario.moneda_to.data]["price"]
                            pu=formulario.cantidad_from.data / cantidadFinal

                    return render_template('purchase.html', form = formulario, cantidadFinal = cantidadFinal, precioUnidad=pu)

            except (ConnectionError) as e:
                print(e)


@app.route('/status')
def status():
    formulario=MovimientosForm()
    
    invertido=total_euros_invertidos()
    euros_invertidos= saldo_euros_invertidos()
    valor_criptos=valor_todas_criptos_euros()    
    valor_Actual = invertido+euros_invertidos+valor_criptos
    return render_template('status.html', form = formulario,inversion=invertido,valorActual=valor_Actual)