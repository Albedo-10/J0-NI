import json
import os

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

# Início
print("🧠 J0-NI foi inicializada no NÍVEL 0. Ela não entende nada até que você ensine.")

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

    elif linha == "#exit":
        print("Encerrando J0-NI. Memória salva.")
        break

    else:
        print("Comando desconhecido. Use #input: ou #teach:")
