import json
from unidecode import unidecode


def bake_json(etapas_por_ambiente):
    dados_do_controle = {}
    dados_do_controle["apartamento"] = []

    adicionado_a_apartamento = []
    for ambiente in etapas_por_ambiente:
        dados_do_controle[ambiente] = []
        for etapa in etapas_por_ambiente[ambiente]["etapas"]:
            nome_curto_da_etapa = etapa["nome_curto"]
            dados_do_controle[ambiente].append(nome_curto_da_etapa)
            if nome_curto_da_etapa not in adicionado_a_apartamento:
                dados_do_controle["apartamento"].append(nome_curto_da_etapa)
                adicionado_a_apartamento.append(nome_curto_da_etapa)

    json_do_controle = "../../web/src/componentes/controle/controle.json"
    with open(json_do_controle, "w") as f:
        json.dump(dados_do_controle, f, indent=2)
