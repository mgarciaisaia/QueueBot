import os
import discord

from configs import Configs
from globalVariables import GlobalVariables
from colas import Colas

from comandoCreate import manejarComandoCreate
from comandoAll import manejarComandoAll
from comandoAdd import manejarComandoAdd
from comandoDelete import manejarComandoDelete
from comandoList import manejarComandoList
from comandoNext import manejarComandoNext
from comandoRemove import manejarComandoRemove
from comandoHelp import manejarComandoHelp

# Datos administrativos del bot
cliente = discord.Client()
TOKEN = os.environ['TOKEN']

# Configs
canalSpamComandosID = Configs.canalSpamComandosID
canalOutputBotID = Configs.canalOutputBotID

prefijoBot = Configs.prefijoBot

comandoCreate = Configs.comandoCreate
comandoList = Configs.comandoList
comandoNext = Configs.comandoNext
comandoDelete = Configs.comandoDelete
comandoAdd = Configs.comandoAdd
comandoRemove = Configs.comandoRemove
comandoHelp = Configs.comandoHelp
comandoAll = Configs.comandoAll

canalSpamComandos = None


async def chequearIntegridadDeMensaje(mensaje, autorMensaje):
    if len(mensaje.split(" ", 7)) > 3:
        await canalSpamComandos.send(
            f"**[Error]** Ha ocurrido un error al procesar la solicitud de {str(autorMensaje)}. Por favor intente nuevamente."
        )


# Evento de inicializacion
@cliente.event
async def on_ready():
    global canalSpamComandos

    # Cargo los canales donde el bot hablara
    canalOutputBot = cliente.get_channel(canalOutputBotID)
    canalSpamComandos = cliente.get_channel(canalSpamComandosID)

    GlobalVariables.canalOutputBot = canalOutputBot
    GlobalVariables.canalSpamComandos = canalSpamComandos

    if canalSpamComandos is None:
        print("[ERROR] No se pudo encontrar el canal 'canalSpamComandos'")
    if canalOutputBot is None:
        print("[ERROR] No se pudo encontrar el canal 'canalOutputBot'")

    print('[Info] El bot ha sido cargado como el usurio: {0.user}'.format(
        cliente))
    await canalOutputBot.send(
        "El bot ha sido inicializado correctamente como el usuario **{0.user}**".format(cliente))


# Evento de mensaje recibido
@cliente.event
async def on_message(message):
    # Cancelo la operacion si el mensaje es enviado por el mismo bot
    if message.author == cliente.user:
        return

    mensajeSeparado = message.content.split(" ", 5)

    # Si no me invocaron ignoro el mensaje
    if not mensajeSeparado[0] == prefijoBot:
        return

    # Si no inserto ningun segundo parametro
    if len(mensajeSeparado) == 1:
        await message.channel.send(
            f"Debes insertar algun comando. Usa `{prefijoBot} {comandoHelp}` para una lista de comandos."
        )
        return

    # Variables necesarias
    mensaje = message.content
    autorMensaje = message.author
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    print("[Mensaje recibido] " + mensaje)

    if mensajeSeparado[1] == comandoCreate:
        await manejarComandoCreate(mensaje, autorMensaje, tagAlAutor)
    elif mensajeSeparado[1] == comandoList:
        await manejarComandoList(mensaje, autorMensaje)
    elif mensajeSeparado[1] == comandoNext:
        await manejarComandoNext(mensaje, autorMensaje)
    elif mensajeSeparado[1] == comandoDelete:
        await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor)
    elif mensajeSeparado[1] == comandoAdd:
        await manejarComandoAdd(mensaje, autorMensaje, tagAlAutor)
    elif mensajeSeparado[1] == comandoRemove:
        await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor)
    elif mensajeSeparado[1] == comandoHelp:
        await manejarComandoHelp()
    elif mensajeSeparado[1] == comandoAll:
        await manejarComandoAll(autorMensaje)
    else:
        await message.channel.send(
            f"Comando no existente. Usa `{prefijoBot} {comandoHelp}` para una lista de comandos."
        )


# Evento de reaccion recibida
@cliente.event
async def on_reaction_add(reaction, user):
    # No hago nada con cualquier reaccion hecha por el bot
    # Y Chequeo si la reaccion es a un mensaje enviado por el bot
    if user == cliente.user or not Colas.esAlgunaReaccionDeCola(reaction.message):
        return

    mensaje = prefijoBot + " "
    autorMensaje = user
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    # Variables necesarias
    nombreCola = reaction.message.embeds[0].title.split(" ",
                                                        2)[1].split(":", 1)[0]
    emoji = reaction.emoji

    # Remuevo la reaccion generada por el usuario
    await reaction.remove(user)

    if emoji == '👍':
        mensaje += comandoAdd + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje, autorMensaje)
        print("[Add] " + mensaje)

        await manejarComandoAdd(mensaje, autorMensaje, tagAlAutor)
    elif emoji == '👎':
        mensaje += comandoRemove + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje, autorMensaje)
        print("[Remove] " + mensaje)

        await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor)
    elif emoji == '➡️':
        mensaje += comandoNext + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje, autorMensaje)
        print("[Next] " + mensaje)

        await manejarComandoNext(mensaje, autorMensaje)
    elif emoji == '❌':
        mensaje += comandoDelete + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje, autorMensaje)
        print("[Delete] " + mensaje)

        await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor)


# Corre el bot
cliente.run(TOKEN)
