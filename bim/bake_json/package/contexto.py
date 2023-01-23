import json
from unidecode import unidecode


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_project):
    dados_do_contexto = {}

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome = ifc_ambiente.LongName
            nome_curto = unidecode(nome.lower().replace(" ", ""))
            dados_do_contexto[nome_curto] = nome

    for i in range(len(ifc_etapas_por_id)):
        etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome = etapa.Name
        nome_curto = unidecode(nome.lower().replace(" ", ""))
        dados_do_contexto[nome_curto] = nome

    dados_do_contexto["projeto"] = ifc_project[0].Name

    dados_do_contexto["apartamento"] = "Apartamento"

    json_do_contexto = "../../web/src/componentes/contexto/contexto.json"
    with open(json_do_contexto, "w") as f:
        json.dump(dados_do_contexto, f, indent=2)
