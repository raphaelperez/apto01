import json
from unidecode import unidecode


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    dados_de_demolicoes = {}
    dados_de_demolicoes["projeto"] = ifc_projeto[0].LongName

    dados_de_demolicoes["apartamento"] = {}
    dados_de_demolicoes["apartamento"]["nome"] = ifc_projeto[0].LongName
    dados_de_demolicoes["apartamento"]["itens"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        if nome_da_etapa == "Demolições":

            for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                tipos_adicionados = []
                tmp = {}
                for obj in ifc_sub_etapa.OperatesOn[0].RelatedObjects:
                    tipo_do_obj = obj.ObjectType

                    if tipo_do_obj not in tipos_adicionados:
                        tmp[tipo_do_obj] = {
                            "id": "apartamento-" + tipo_do_obj,
                            "tipo": tipo_do_obj,
                            "area": obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue,
                        }
                        tipos_adicionados.append(tipo_do_obj)
                    elif tipo_do_obj in tipos_adicionados:
                        tmp[tipo_do_obj]["area"] += obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue

                for tipo in tipos_adicionados:
                    tmp[tipo]["area"] = int(round(tmp[tipo]["area"], 0))
                    dados_de_demolicoes["apartamento"]["itens"].append(tmp[tipo])

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            dados_de_demolicoes[nome_curto_do_ambiente] = {}
            dados_de_demolicoes[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            dados_de_demolicoes[nome_curto_do_ambiente]["itens"] = []

            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name

                if nome_da_etapa == "Demolições":

                    for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                        ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                        tipos_adicionados = []
                        tmp = {}
                        for obj in ifc_sub_etapa.OperatesOn[0].RelatedObjects:
                            tipo_do_obj = obj.ObjectType
                            nome_do_ambiente_do_obj = obj.ContainedInStructure[0].RelatingStructure.LongName

                            if tipo_do_obj not in tipos_adicionados and nome_do_ambiente_do_obj == nome_do_ambiente:
                                tmp[tipo_do_obj] = {
                                    "id": nome_curto_do_ambiente + "-" + tipo_do_obj,
                                    "tipo": tipo_do_obj,
                                    "area": obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue,
                                }
                                tipos_adicionados.append(tipo_do_obj)
                            elif tipo_do_obj in tipos_adicionados and nome_do_ambiente_do_obj == nome_do_ambiente:
                                tmp[tipo_do_obj]["area"] += obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue

                        for tipo in tipos_adicionados:
                            tmp[tipo]["area"] = int(round(tmp[tipo]["area"], 0))
                            dados_de_demolicoes[nome_curto_do_ambiente]["itens"].append(tmp[tipo])

    json_de_demolicoes = "../../web/src/components/painel/contextos/demolicoes.json"
    with open(json_de_demolicoes, "w") as f:
        json.dump(dados_de_demolicoes, f, indent=2)
