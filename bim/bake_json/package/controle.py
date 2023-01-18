import json
from unidecode import unidecode


def bake_json(etapas_por_ambiente):
    dados_do_controle = {}
    dados_do_controle["apartamento"] = []

    for ambiente in etapas_por_ambiente:
        nome_do_ambiente = etapas_por_ambiente[ambiente]["nome_curto"]
        dados_do_controle[nome_do_ambiente] = []

        for etapa in etapas_por_ambiente[ambiente]["etapas"]:
            nome_da_etapa = etapa["nome_curto"]
            dados_do_controle[nome_do_ambiente].append(nome_da_etapa)
            if nome_da_etapa not in dados_do_controle["apartamento"]:
                dados_do_controle["apartamento"].append(nome_da_etapa)

    json_do_controle = "../../web/src/components/controle/controle.json"
    with open(json_do_controle, "w") as f:
        json.dump(dados_do_controle, f, indent=2)
