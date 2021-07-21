from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date, datetime

def fechaFormateada():
    fecha=datetime.now()
    return(fecha.strftime("%dd/%mm/%yyyy"))


class MovimientosForm(FlaskForm):

    id=HiddenField()
    
    fecha = StringField("fecha",default=fechaFormateada())

    hora = StringField("hora")

    moneda_from = SelectField("moneda from", choices=[("EUR"),("ETH"),("LTC"),("BNB"),
        ("EOS"),("XLM"),("TRX"),("BTC"),("XRP"),("BCH"),("USDT"),("BSV"),("ADA")])

    cantidad_from=FloatField("Cantidad",validators=[DataRequired("debes introducir un numero que sea mayor que 0")])

    moneda_to = SelectField("moneda to", choices=[("EUR"),("ETH"),("LTC"),("BNB"),
        ("EOS"),("XLM"),("TRX"),("BTC"),("XRP"),("BCH"),("USDT"),("BSV"),("ADA")])
    
    cantidad_to = FloatField("Cantidad")

    pu=FloatField("Precio por unidad")

    submit=SubmitField("Aceptar")

    calcular_cripto=SubmitField("Calcular")

