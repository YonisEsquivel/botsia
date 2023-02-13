import mysql.connector

class Conexion(object):
    def __init__(self):
        self.connected=0
        self.error=""
    
    def mysqlConnect(self):
        try:
            self.db = mysql.connector.connect(host="localhost",user="root",passwd="",db="dbbotsia")
            self.cursor = self.db.cursor(dictionary=True)
            self.connected=1
            return self.cursor
        except Exception as e:
            print("Error: %s" % str(e))
        except:
            self.error="Error desconocido en la conexion"
        return False
    
    def prepare(self,sql,cnx):
        try:
            if self.connected:
                sql_part = sql.split(" ")
                #print(sql_part[0].upper())
                cnx.execute(sql)
                if sql_part[0].upper() == "SELECT":
                    res = cnx.fetchall()
                elif sql_part[0].upper() =="INSERT":
                    res = {"lastID":cnx.lastrowid}
                else:
                    res = True
                
                if res:
                    return res
                else:
                    return False
            else:
                print("error no conectado")
                return False
        except Exception as e:
            print("Error funcion prepare: {}".format(e))
            return False

    def ejecutar(self):
        self.db.commit()
    
    def retrocede(self):
        self.db.rollback()
        
    def mysqlClose(self):
        self.connected=0
        try:
            self.cursor.close()
        except:pass
        try:
            self.db.close()
        except:pass