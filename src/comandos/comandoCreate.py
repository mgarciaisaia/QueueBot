from src.configs.globalVariables import GlobalVariables
from src.configs.configs import Configs

from src.utils.utils import esMod
from src.utils.utils import cantidadDeParametrosEs
from src.utils.utils import printearErrorSinPermisos
from src.clases.colas import Colas

comandoCreate = Configs.comandoCreate
prefijoBot = Configs.prefijoBot


# Description: Crea un nueva cola y la agrega a la lista
# Access: Only Mods
async def manejarComandoCreate(mensaje, autorMensaje, tagAlAutor):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoCreate)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoCreate} nombreCola`"
        )
        return

    nombreCola = parametrosMensaje[2]

    if (Colas.existeCola(nombreCola)):
        await canalSpamComandos.send(
            f"Ya existe una cola con el nombre **{nombreCola}**!")
    else:
        Colas.agregarCola(nombreCola)
        await canalSpamComandos.send(
            f"{tagAlAutor} ha creado una nueva cola llamada: **{str(nombreCola)}**."
        )
        await Colas.enviarMensajeNuevoEnCola(nombreCola)
