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



dbManager = DBmanager()


@app.route('/', methods=["GET", "POST"])
def index():

    query = "SELECT * FROM movimientos WHERE 1=1"
    datos=[]
    movimientos = dbManager.consultaMuchasSQL(query,datos)
    print(query)
    
    if not movimientos:
        flash("no hay datos aún")
    
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
                    fecha = datetime.now().strftime('%Y-%m-%d')
                    hora = datetime.now().strftime('%H:%M:%S')
                    dbManager.modificaTablaSQL(query,[fecha, hora,  formulario.moneda_from.data, formulario.cantidad_from.data , formulario.moneda_to.data, 
                                                                    formulario.cantidad_to.data])
                                                            
                except sqlite3.Error as el_error:
                    
                    print("Error en SQL INSERT", el_error)
                    flash("se ha producido un error en la bddd. Pruebe en unos minutos", "error")
                    return render_template('movimientos.html', form=formulario)
                
                return redirect(url_for('index'))
            else:
                return render_template('purchase.html', form=formulario)
        
        elif formulario.calcular_cripto.data == True:

            url_convert = api.URL_CRIPTO
            parameters = {
                'amount':formulario.cantidad_from.data,
                'symbol':formulario.moneda_from.data,
                'convert':formulario.moneda_to.data
            }
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
            
