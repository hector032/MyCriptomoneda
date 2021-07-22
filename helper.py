import sqlite3
from mycripto.dataaccess import *

dbManager = DBmanager()

def totalMovimientos():        
    query = "SELECT * FROM movimientos WHERE 1=1"    
    print (query)
    movimientos = dbManager.consultaMuchasSQL(query,[])

    return movimientos