import json
from unidecode import unidecode


def bake_json(ifc_etapas_por_id, ifc_ambientes, etapas_por_ambiente):
    dados_do_menu_do_ambiente = {}

    dados_do_menu_do_ambiente["apartamento"] = {}
    dados_do_menu_do_ambiente["apartamento"]["nome"] = "apartamento"
    dados_do_menu_do_ambiente["apartamento"]["etapas"] = []

    # adicionado_ao_apartamento = []
    # for ifc_ambiente in ifc_ambientes:
    #     id_do_ambiente = ifc_ambiente.Name
    #     nome_do_ambiente = ifc_ambiente.LongName
    #     nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))
    #     dados_do_menu_do_ambiente[nome_curto_do_ambiente] = {}
    #     dados_do_menu_do_ambiente[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
    #     dados_do_menu_do_ambiente[nome_curto_do_ambiente]["etapas"] = []

    #     for id in ifc_etapas_por_id:
    #         nome_da_etapa = ifc_etapas_por_id[id]["etapa"].Name
    #         nome_curto_da_etapa = unidecode(nome_da_etapa.lower().replace(" ", ""))
    #         etapa = {"id": id_do_ambiente + nome_da_etapa, "nomeCurto": nome_curto_da_etapa, "nome": nome_da_etapa}
    #         dados_do_menu_do_ambiente[nome_curto_do_ambiente]["etapas"].append(etapa)
    #         if nome_curto_da_etapa not in adicionado_ao_apartamento:
    #             dados_do_menu_do_ambiente["apartamento"]["etapas"].append(etapa)

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

    json_do_menu_do_ambiente = "../../web/src/components/menu/menus/menuDoAmbiente.json"
    with open(json_do_menu_do_ambiente, "w") as f:
        json.dump(dados_do_menu_do_ambiente, f, indent=2)
