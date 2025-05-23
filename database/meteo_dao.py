from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_sitazioni_mese(citta, mese):
        cnx = DBConnect.get_connection()
        situazioni = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select Localita, Data, Umidita
                        from situazione s 
                        where Localita = %s and month(s.Data) = %s"""
            cursor.execute(query, (citta, mese))

            for row in cursor:
                situazioni.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))

            cursor.close()
            cnx.close()
        return situazioni

    @staticmethod
    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                            FROM situazione s
                            WHERE MONTH(s.Data)=%s AND DAY(s.Data)<=15 
                            ORDER BY s.Data ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result