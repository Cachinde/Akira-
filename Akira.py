import pywhatkit
import time
import sqlite3
import requests
import openai

# Configuração da OpenAI
OPENAI_API_KEY = "SUA_API_KEY_OPENAI"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# Criar Banco de Dados
def criar_tabela():
    with sqlite3.connect("akira.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS interacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            mensagem TEXT,
            resposta TEXT,
            estilo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

criar_tabela()

# Função para salvar interações
def salvar_interacao(usuario, mensagem, resposta, estilo):
    with sqlite3.connect("akira.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO interacoes (usuario, mensagem, resposta, estilo) VALUES (?, ?, ?, ?)", 
                       (usuario, mensagem, resposta, estilo))
        conn.commit()

# Função para interagir com a OpenAI
def call_openai_api(prompt):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7,
        "top_p": 1
    }
    response = requests.post(OPENAI_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return "Erro na API OpenAI"

# Função para enviar mensagem no WhatsApp
def enviar_mensagem_whatsapp(numero, mensagem):
    try:
        pywhatkit.sendwhatmsg_instantly(numero, mensagem)
        print(f"✅ Mensagem enviada para {numero}: {mensagem}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

# Simulação de recebimento de mensagens
contatos_monitorados = ["+5511999999999"]

def verificar_mensagens_whatsapp():
    print("📩 Verificando mensagens no WhatsApp...")
    for numero in contatos_monitorados:
        mensagem_recebida = "Olá Akira, como você está?"
        print(f"📩 Mensagem recebida de {numero}: {mensagem_recebida}")
        resposta = call_openai_api(mensagem_recebida)
        enviar_mensagem_whatsapp(numero, resposta)
    return "Verificação concluída."

if __name__ == "__main__":
    while True:
        verificar_mensagens_whatsapp()
        time.sleep(60)
