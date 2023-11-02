from fastapi import FastAPI, HTTPException, Query, Form

import sett
import services

app = FastAPI()

@app.get('/bienvenido')
def bienvenido():
    return 'Hola'

@app.get('/webhook')
def verificar_token(hub_verify_token: str = Query(...), hub_challenge: str = Query(None)):
    if hub_verify_token == sett.token and hub_challenge is not None:
        return hub_challenge
    else:
        raise HTTPException(status_code=403, detail='token incorrecto')

@app.post('/webhook')
def recibir_mensajes(body: dict):
    try:
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number, messageId, name)
        return 'enviado'

    except Exception as e:
        return HTTPException(status_code=500, detail='no enviado ' + str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

