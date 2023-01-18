import json
from unidecode import unidecode


def gera_lista_per(ifc_sub_etapa, nome_do_ambiente):
    lista_per = []
    materiais_adicionados = []
    dict_per = {}
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        if nome_do_ambiente == "apartamento" or nome_do_ambiente == ifc_obj.ContainedInStructure[0].RelatingStructure.LongName:
            ifc_material = ifc_obj.HasAssociations[0].RelatingMaterial
            nome_do_material = ifc_material.Name
            if nome_do_material not in materiais_adicionados:
                dict_per[nome_do_material] = {
                    "id": "APTO-" + ifc_material.Name,
                    "nome": ifc_material.Name,
                    "tipo": ifc_material.Category,
                    "area": ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue,
                    "fabricante": ifc_material.HasProperties[0].Properties[0].NominalValue.wrappedValue,
                    "especificacao": ifc_material.HasProperties[0].Properties[1].NominalValue.wrappedValue,
                    "tipoDeMaterial": ifc_material.HasProperties[0].Properties[2].NominalValue.wrappedValue,
                    "precoUnitario": ifc_material.HasProperties[0].Properties[3].NominalValue.wrappedValue,
                    "url": ifc_material.HasProperties[0].Properties[4].NominalValue.wrappedValue,
                }
                dict_per[nome_do_material]["imgSource"] = (
                    "./img/"
                    + unidecode(dict_per[nome_do_material]["fabricante"].lower().replace(" ", "_"))
                    + "-"
                    + unidecode(dict_per[nome_do_material]["especificacao"].lower().replace(" ", "_"))
                    + ".jpg"
                )
                materiais_adicionados.append(nome_do_material)
            else:
                area = ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue
                dict_per[nome_do_material]["area"] += area
            dict_per[nome_do_material]["area"] = round(dict_per[nome_do_material]["area"], 0)

    for mat in materiais_adicionados:
        lista_per.append(dict_per[mat])

    return lista_per


def gera_lista_pinturas(ifc_sub_etapa, nome_do_ambiente):
    lista_pinturas = []
    materiais_adicionados = []
    dict_pinturas = {}
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        if nome_do_ambiente == "apartamento" or nome_do_ambiente == ifc_obj.ContainedInStructure[0].RelatingStructure.LongName:
            ifc_material = ifc_obj.HasAssociations[0].RelatingMaterial
            nome_do_material = ifc_material.Name
            if nome_do_material not in materiais_adicionados:
                dict_pinturas[nome_do_material] = {
                    "id": "APTO-" + ifc_material.Name,
                    "nome": ifc_material.Name,
                    "tipo": ifc_material.Category,
                    "area": ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue,
                    "fabricante": ifc_material.HasProperties[0].Properties[0].NominalValue.wrappedValue,
                    "especificacao": ifc_material.HasProperties[0].Properties[1].NominalValue.wrappedValue,
                    "tipoDeMaterial": ifc_material.HasProperties[0].Properties[2].NominalValue.wrappedValue,
                    "precoUnitario": ifc_material.HasProperties[0].Properties[3].NominalValue.wrappedValue,
                    "url": ifc_material.HasProperties[0].Properties[4].NominalValue.wrappedValue,
                }
                dict_pinturas[nome_do_material]["imgSource"] = (
                    "./img/"
                    + unidecode(dict_pinturas[nome_do_material]["fabricante"].lower().replace(" ", "_"))
                    + "-"
                    + unidecode(dict_pinturas[nome_do_material]["especificacao"].lower().replace(" ", "_"))
                    + ".jpg"
                )
                materiais_adicionados.append(nome_do_material)
            else:
                area = ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue
                dict_pinturas[nome_do_material]["area"] += area
            dict_pinturas[nome_do_material]["area"] = round(dict_pinturas[nome_do_material]["area"], 0)

    for mat in materiais_adicionados:
        lista_pinturas.append(dict_pinturas[mat])

    return lista_pinturas


def gera_lista_forros(ifc_sub_etapa, nome_do_ambiente):
    lista_forros = []
    materiais_adicionados = []
    dict_forros = {}
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        if nome_do_ambiente == "apartamento" or nome_do_ambiente == ifc_obj.ContainedInStructure[0].RelatingStructure.LongName:
            nome_do_forro = ifc_obj.Name
            tipo_do_forro = ifc_obj.Description
            if nome_do_forro not in materiais_adicionados:
                dict_forros[nome_do_forro] = {
                    "id": "APTO-" + nome_do_forro,
                    "nome": nome_do_forro,
                    "tipo": tipo_do_forro,
                    "area": ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue,
                }
                dict_forros[nome_do_forro]["imgSource"] = "./img/" + unidecode(tipo_do_forro.lower().replace(" ", "_")) + ".jpg"
                materiais_adicionados.append(nome_do_forro)
            else:
                area = ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue
                dict_forros[nome_do_forro]["area"] += area
            dict_forros[nome_do_forro]["area"] = round(dict_forros[nome_do_forro]["area"], 0)

    print(dict_forros)
    print(materiais_adicionados)

    for mat in materiais_adicionados:
        lista_forros.append(dict_forros[mat])

    return lista_forros


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    dados_do_painel_de_contexto = {}
    dados_do_painel_de_contexto["projeto"] = ifc_projeto[0].Name
    dados_do_painel_de_contexto["apartamento"] = {}
    dados_do_painel_de_contexto["apartamento"]["nome"] = ifc_projeto[0].Name
    dados_do_painel_de_contexto["apartamento"]["itens"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        if nome_da_etapa == "Cobrimentos":
            obj_per = {}
            obj_pinturas = {}
            obj_forros = {}

            for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]
                nome_da_sub_etapa = ifc_sub_etapa.Name

                if nome_da_sub_etapa == "Pisos e Revestimentos":
                    obj_per["item"] = "Pisos e Revestimentos"
                    obj_per["pers"] = gera_lista_per(ifc_sub_etapa, "apartamento")

                elif nome_da_sub_etapa == "Pinturas":
                    obj_pinturas["item"] = "Pinturas"
                    obj_pinturas["pinturas"] = gera_lista_pinturas(ifc_sub_etapa, "apartamento")

                elif nome_da_sub_etapa == "Forros":
                    obj_forros["item"] = "Forros"
                    obj_forros["forros"] = gera_lista_forros(ifc_sub_etapa, "apartamento")

            dados_do_painel_de_contexto["apartamento"]["itens"].append(obj_per)
            dados_do_painel_de_contexto["apartamento"]["itens"].append(obj_pinturas)
            dados_do_painel_de_contexto["apartamento"]["itens"].append(obj_forros)

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            dados_do_painel_de_contexto[nome_curto_do_ambiente] = {}
            dados_do_painel_de_contexto[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            dados_do_painel_de_contexto[nome_curto_do_ambiente]["itens"] = []

            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name

                if nome_da_etapa == "Cobrimentos":
                    obj_per = {}
                    obj_pinturas = {}
                    obj_forros = {}

                    for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                        ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]
                        nome_da_sub_etapa = ifc_sub_etapa.Name

                        if nome_da_sub_etapa == "Pisos e Revestimentos":
                            obj_per["item"] = "Pisos e Revestimentos"
                            obj_per["pers"] = gera_lista_per(ifc_sub_etapa, nome_do_ambiente)

                        elif nome_da_sub_etapa == "Pinturas":
                            obj_pinturas["item"] = "Pinturas"
                            obj_pinturas["pinturas"] = gera_lista_pinturas(ifc_sub_etapa, nome_do_ambiente)

                        elif nome_da_sub_etapa == "Forros":
                            obj_forros["item"] = "Forros"
                            obj_forros["forros"] = gera_lista_forros(ifc_sub_etapa, nome_do_ambiente)

                    dados_do_painel_de_contexto[nome_curto_do_ambiente]["itens"].append(obj_per)
                    dados_do_painel_de_contexto[nome_curto_do_ambiente]["itens"].append(obj_pinturas)
                    dados_do_painel_de_contexto[nome_curto_do_ambiente]["itens"].append(obj_forros)

    json_do_painel_de_contexto = "../../web/src/components/painel/contextos/cobrimentos.json"
    with open(json_do_painel_de_contexto, "w") as f:
        json.dump(dados_do_painel_de_contexto, f, indent=2)
