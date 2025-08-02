import json
import os
import random

MEMORIA = "joni_memory_nivel0.json"

def carregar_memoria():
    if os.path.exists(MEMORIA):
        with open(MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"vocabulário": {}}

def salvar_memoria(memoria):
    with open(MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

def responder(entrada, memoria):
    if entrada in memoria["vocabulário"]:
        significado = memoria["vocabulário"][entrada]
        return f"(registro encontrado) \"{entrada}\" = {significado}"
    else:
        return f"(registro não encontrado) \"{entrada}\" não tem significado conhecido."

def ensinar(entrada, significado, memoria):
    memoria["vocabulário"][entrada] = significado
    salvar_memoria(memoria)
    return f"(registro adicionado) \"{entrada}\" = {significado}"

def comunicar(memoria):
    vocab = memoria.get("vocabulário", {})
    if not vocab:
        return "Ainda não sei o que dizer..."

    termo = random.choice(list(vocab.keys()))
    significado = vocab[termo]

    frases_modelo = [
        f"Eu lembro que '{termo}' significa '{significado}'.",
        f"Acho que '{termo}' quer dizer '{significado}'.",
        f"Aprendi que '{termo}' é '{significado}'.",
        f"Pensei em '{termo}', que significa '{significado}'.",
        f"Se não me engano, '{termo}' é '{significado}'."
    ]

    return random.choice(frases_modelo)


# Início
print("🧠 J0-NI agora tem um módulo de comunicação básica.")

def revisar_conhecimento(memoria):
    frases_sabe = []
    frases_incompletas = []

    for chave, significado in memoria["vocabulário"].items():
        if any(pronome in chave for pronome in ["eu", "joni", "você"]):
            if "?" in significado or significado.strip() in ["", "?", "..."]:
                frases_incompletas.append(f"- Eu ainda não entendo o que é \"{chave}\".")
            else:
                frases_sabe.append(f"- Eu sei que {chave} = {significado}.")

    resposta = "Eu sou J0-NI.\n"
    resposta += "\n".join(frases_sabe[:5]) + "\n"  # Limita a 5 frases por revisão
    if frases_incompletas:
        resposta += "\n" + "\n".join(frases_incompletas[:3])
    resposta += "\nEu quero aprender mais coisas."
    return resposta
def listar_sentimentos(memoria):
    sentimentos = []
    incompletos = []

    for chave, significado in memoria["vocabulário"].items():
        if "sentimento" in chave:
            nome = chave.split(" é")[0]
            if "?" in significado or significado.strip() in ["", "..."]:
                incompletos.append(f"- Eu ainda não entendo o que é \"{nome}\".")
            else:
                sentimentos.append(f"- {nome.capitalize()}: {significado}")

    if not sentimentos and not incompletos:
        return "Ainda não aprendi nada sobre sentimentos."

    resposta = "Sentimentos que conheço:\n"
    resposta += "\n".join(sentimentos[:5]) + "\n"
    if incompletos:
        resposta += "\nSentimentos que quero entender:\n" + "\n".join(incompletos[:3])
    return resposta

memoria = carregar_memoria()

while True:
    linha = input("\nComando: ").strip()

    if linha.startswith("#input:"):
        entrada = linha.replace("#input:", "").strip().lower()
        resposta = responder(entrada, memoria)
        print(f"J0-NI: {resposta}")

    elif linha.startswith("#teach:"):
        try:
            conteudo = linha.replace("#teach:", "").strip()
            chave, significado = conteudo.split("=", 1)
            chave = chave.strip().lower()
            significado = significado.strip()
            resposta = ensinar(chave, significado, memoria)
            print(f"J0-NI: {resposta}")
        except ValueError:
            print("Formato inválido. Use: #teach: palavra = significado")

    elif linha == "#talk":
        resposta = comunicar(memoria)
        print(f"J0-NI (fala): {resposta}")

    elif linha == "#activity: sentimentos":
        resposta = listar_sentimentos(memoria)
        print(f"J0-NI (atividade):\n{resposta}")

    elif linha == "#activity: revisão":
        resposta = revisar_conhecimento(memoria)
        print(f"J0-NI (atividade):\n{resposta}")


    elif linha == "#exit":
        print("Encerrando J0-NI. Memória salva.")
        break

    else:
        print("Comando desconhecido. Use #input:, #teach:, #talk ou #exit")
