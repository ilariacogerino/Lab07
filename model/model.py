import copy

from database.meteo_dao import MeteoDao
from model import situazione


class Model:
    def __init__(self):
        self.dao = MeteoDao()
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []

    def getSituazioniMese(self, citta, mese):
        situa = self.dao.get_sitazioni_mese(citta, mese)
        return situa

    def calcola_sequenza (self, mese):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = self.dao.get_situazioni_meta_mese(mese)
        self.ricorsione([], situazioni) #do il via alla mia ricorsione (passo un parziale vuoto e i dati)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.Data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidata, parziale):
        #vincolo dei 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.Localita == candidata.Localita:
                counter += 1
        if counter >= 6: #non posso più fermarmi in quella località, ci sono già stato 6 giorni
            return False

        #vincolo sulla permanenza
            # 1) lunghezza di parziale < 3, il candidato dev'essere per forza uguale al primo elemento di parziale
        if len(parziale) == 0: #è la prima città in cui mi fermo
            return True
        if len(parziale)<3:
            if candidata.Localita != parziale[0].Localita: #non ci sono stata tre giorni di fila, non va bene
                return False

            # 2) Le tre situazioni precedenti non sono tutte uguali
        else:
            if parziale[-3].Localita != parziale[-2].Localita or parziale[-3].Localita != parziale[-1].Localita or \
                    parziale[-1].Localita != parziale[-2].Localita:
                if parziale[-1].Localita != candidata.Localita:
                    return False
        # altrimenti OK
        return True

    def calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidità
        for situazione in parziale:
            costo += situazione.Umidita
        return costo

    def ricorsione(self, parziale, lista_situazioni):
        if len(parziale) == 15:    #condizione terminale
            self.n_soluzioni += 1
            costo = self.calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale) #effettua una copia profonda di parziale
        else:   #condizione ricorsiva
            # cercare le città per il giorno che mi serve
            candidate = self.trova_possibili_step(parziale, lista_situazioni) #lista di giorni possibili
            # provo ad aggiungere una di queste città e vado avanti
            for candidata in candidate:
                if self.is_admissible(candidata, parziale):
                    parziale.append(candidata)
                    self.ricorsione(parziale, lista_situazioni)
                    parziale.pop() #backtracking

        return self.soluzione_ottima, self.costo_ottimo