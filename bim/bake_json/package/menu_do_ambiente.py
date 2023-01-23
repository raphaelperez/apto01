import json
from unidecode import unidecode


def bake_json(etapas_por_ambiente):
    dados_do_menu_do_ambiente = {}

    dados_do_menu_do_ambiente["apartamento"] = {}
    dados_do_menu_do_ambiente["apartamento"]["nome"] = "apartamento"
    dados_do_menu_do_ambiente["apartamento"]["etapas"] = []

    adicionado_ao_apartamento = []
    for ambiente in etapas_por_ambiente:
        dados_do_menu_do_ambiente[ambiente] = {}
        dados_do_menu_do_ambiente[ambiente]["nome"] = etapas_por_ambiente[ambiente]["nome"]
        dados_do_menu_do_ambiente[ambiente]["etapas"] = []
        for etapa in etapas_por_ambiente[ambiente]["etapas"]:
            dict = {"id": etapa["nome_curto"] + "-" + etapa["nome"], "nomeCurto": etapa["nome_curto"], "nome": etapa["nome"]}
            dict_apto = {"id": "apartamento-" + etapa["nome"], "nomeCurto": etapa["nome_curto"], "nome": etapa["nome"]}
            dados_do_menu_do_ambiente[ambiente]["etapas"].append(dict)

            if etapa["nome_curto"] not in adicionado_ao_apartamento:
                dados_do_menu_do_ambiente["apartamento"]["etapas"].append(dict_apto)
                adicionado_ao_apartamento.append(etapa["nome_curto"])

    json_do_menu_do_ambiente = "../../web/src/componentes/menu/menus/menuDoAmbiente.json"
    with open(json_do_menu_do_ambiente, "w") as f:
        json.dump(dados_do_menu_do_ambiente, f, indent=2)
