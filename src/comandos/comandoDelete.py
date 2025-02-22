from src.configs.globalVariables import GlobalVariables
from src.configs.configs import Configs

from src.utils.utils import esMod
from src.utils.utils import cantidadDeParametrosEs
from src.utils.utils import printearErrorSinPermisos
from src.clases.colas import Colas

comandoDelete = Configs.comandoDelete
prefijoBot = Configs.prefijoBot


# Description: Eliminar una cola
# Access: Only Mods
async def manejarComandoDelete(mensaje, autorMensaje, tagAlAutor):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoDelete)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: {prefijoBot} {comandoDelete} nombreCola`."
        )
        return

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        await Colas.eliminarMensajeEnCola(nombreCola)
        Colas.quitarCola(nombreCola)
        await canalSpamComandos.send(
            f"{tagAlAutor} ha eliminado la cola **{nombreCola}**.")
