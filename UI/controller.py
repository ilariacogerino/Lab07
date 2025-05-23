import flet as ft
from functools import lru_cache

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()

        mese = self._view.dd_mese.value #PRENDE GIA' IL NUMERO DEL MESE (NON IL LAVORE)

        if mese == None:
            self._view.create_alert("Selezionare un mese!!")
            self._view._page.update()

        #SITUAZIONI TORINO
        situazioniTorino = self._model.getSituazioniMese("Torino", mese)
        countTO = 0
        umiditaTO = 0
        for situazione in situazioniTorino:
            umiditaTO += situazione.Umidita
            countTO+=1
        mediaTO = umiditaTO/len(situazioniTorino)

        #SITUAZIONI MILANO
        situazioniMilano = self._model.getSituazioniMese("Milano", mese)
        countMI = 0
        umiditaMI = 0
        for situazione in situazioniMilano:
            umiditaMI += situazione.Umidita
            countMI += 1
        mediaMI = umiditaMI / countMI

        #SITUAZIONI GENOVA
        situazioniGenova = self._model.getSituazioniMese("Genova", mese)
        countGE = 0
        umiditaGE = 0
        for situazione in situazioniGenova:
            umiditaGE += situazione.Umidita
            countGE += 1
        mediaGE = umiditaGE / countGE

        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {round(mediaGE, 4)}"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {round(mediaMI, 4)}"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {round(mediaTO, 4)}"))

        self._view._page.update()

    @lru_cache(maxsize=None)
    def handle_sequenza(self, e):

        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value  # PRENDE GIA' IL NUMERO DEL MESE (NON IL LAVORE)

        if mese == None or mese == 0:
            self._view.create_alert("Selezionare un mese!!")
            self._view._page.update()

        self._view.lst_result.controls.append(ft.Text(f"Costo: {self._model.calcola_sequenza(mese)[1]}"))
        for sitauzione in self._model.calcola_sequenza(mese)[0]:
            self._view.lst_result.controls.append(ft.Text(sitauzione.__str__()))


        self._view._page.update()


    def read_mese(self, e):
        self._mese = int(e.control.value)

