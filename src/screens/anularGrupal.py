# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from db import controlador
from lib import impresora
from src.settings import user_session, UNIDAD
from src.alerts import ConfirmPopup, WarningPopup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class AnularGrupalScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para anular los tickets del usuario"""
        self.data = {}
        self.user = user_session.get_user()
        super(AnularGrupalScreen, self).__init__(**kwargs)

    def validar_anulacion(self):
        """Verifica que el numero ingresado corresponda a un ticket valido
        para el usuario y que sea antes de la hora máxima permitida."""
        if self.ids.id_ticket.text:
            if not self.ids.id_ticket.text.isdigit():
                self.ids.id_ticket.text = ""
                self.ids.id_ticket.focus = True
                mensaje = "\rEl código del ticket\r\n solo tiene números."
                WarningPopup(mensaje).open()
            else:
                fecha = controlador.has_ticket_grupal(self.ids.id_ticket.text)
                if fecha:
                    return fecha.strftime('%d/%m/%Y')  # anular
                else:
                    self.ids.id_ticket.text = ""
                    self.ids.id_ticket.focus = True
                    mensaje = "El código del ticket\r\n no es valido."
                    WarningPopup(mensaje).open()
        else:
            self.ids.id_ticket.text = ""
            self.ids.id_ticket.focus = True
            mensaje = "\rEl código del ticket\r\n no puede estar vacío."
            WarningPopup(mensaje).open()

    def confirmacion(self):
        Window.release_all_keyboards()
        self.fecha = self.validar_anulacion()
        if self.fecha:
            self.popup = ConfirmPopup(
                text='\rSeguro deseas anular el ticket\r\n del día %s?' %
                    (self.fecha)
            )
            self.popup.bind(on_answer=self._on_answer)
            self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.anular_ticket_grupal()
        self.ids.id_ticket.text = ""
        self.popup.dismiss()

    def anular_ticket_grupal(self):
        """Anula el ticket de acuerdo al id ingresado"""
        id_ticket = int(self.ids.id_ticket.text)
        controlador.anular_ticket_grupal(id_ticket, self.user, UNIDAD)

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.manager.current = 'servicios'
        self.manager.remove_widget(self.manager.get_screen('anular_grupal'))
