import json
from unidecode import unidecode


def gera_dicionario_item(obj):
    item = {}

    item["item"] = obj.Description
    item["pedras"] = []
    item["acessorios"] = []

    pedras = {}
    pedras_adicionadas = []
    for parte in obj.IsDecomposedBy[0].RelatedObjects:
        if parte.is_a() == "IfcSanitaryTerminal":
            acessorio = {}
            acessorio["nome"] = parte.Name
            acessorio["fabricante"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue
            acessorio["especificacao"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue
            acessorio["descricao"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[2].NominalValue.wrappedValue
            acessorio["codigo"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[3].NominalValue.wrappedValue
            acessorio["precoUnit"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[4].NominalValue.wrappedValue
            acessorio["url"] = parte.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[5].NominalValue.wrappedValue
            acessorio["imgSource"] = (
                "./img/"
                + unidecode(acessorio["fabricante"].lower().replace(" ", ""))
                + "-"
                + unidecode(acessorio["especificacao"].lower().replace(" ", ""))
                + ".jpg"
            )

            item["acessorios"].append(acessorio)

        elif parte.is_a() == "IfcPlate":
            ifc_material = parte.HasAssociations[0].RelatingMaterial
            nome_da_pedra = ifc_material.Name

            perimetro = 1
            largura = 1
            for propriedade in parte.IsDefinedBy[0].RelatingPropertyDefinition.Quantities:
                if propriedade.Name == "Perimeter":
                    perimetro = propriedade.LengthValue
                elif propriedade.Name == "Width":
                    largura = propriedade.LengthValue

            area_da_pedra = largura * (perimetro - (2 * largura)) / 2

            if nome_da_pedra not in pedras_adicionadas:
                pedras[nome_da_pedra] = {}
                pedras[nome_da_pedra]["nome"] = nome_da_pedra
                pedras[nome_da_pedra]["tipoDaPedra"] = ifc_material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                pedras[nome_da_pedra]["especificacao"] = ifc_material.HasProperties[0].Properties[1].NominalValue.wrappedValue
                pedras[nome_da_pedra]["precoUnit"] = ifc_material.HasProperties[0].Properties[2].NominalValue.wrappedValue
                pedras[nome_da_pedra]["area"] = area_da_pedra
                pedras[nome_da_pedra]["imgSource"] = (
                    "./img/"
                    + unidecode(pedras[nome_da_pedra]["tipoDaPedra"].lower().replace(" ", ""))
                    + "-"
                    + unidecode(pedras[nome_da_pedra]["especificacao"].lower().replace(" ", ""))
                    + ".jpg"
                )
                pedras_adicionadas.append(nome_da_pedra)
            elif nome_da_pedra in pedras_adicionadas:
                pedras[nome_da_pedra]["area"] += area_da_pedra

    for pedra in pedras_adicionadas:
        pedras[pedra]["area"] = round(pedras[pedra]["area"], 1)
        item["pedras"].append(pedras[pedra])

    return item


def gera_dicionario_item_geral(itens):
    item_geral = {}
    item_geral["item"] = "Geral"
    item_geral["pedras"] = []
    item_geral["acessorios"] = []
    pedras_adicionadas = []
    acessorios_adicionados = []
    pedras = {}
    acessorios = {}
    for item in itens:
        for pedra in item["pedras"]:
            if pedra["nome"] not in pedras_adicionadas:
                pedras[pedra["nome"]] = {}
                pedras[pedra["nome"]]["nome"] = pedra["nome"]
                pedras[pedra["nome"]]["tipoDaPedra"] = pedra["tipoDaPedra"]
                pedras[pedra["nome"]]["especificacao"] = pedra["especificacao"]
                pedras[pedra["nome"]]["precoUnit"] = pedra["precoUnit"]
                pedras[pedra["nome"]]["area"] = pedra["area"]
                pedras[pedra["nome"]]["imgSource"] = pedra["imgSource"]
                pedras_adicionadas.append(pedra["nome"])
            else:
                pedras[pedra["nome"]]["area"] += pedra["area"]
        for acessorio in item["acessorios"]:
            if acessorio["nome"] not in acessorios_adicionados:
                acessorios[acessorio["nome"]] = {}
                acessorios[acessorio["nome"]]["nome"] = acessorio["nome"]
                acessorios[acessorio["nome"]]["fabricante"] = acessorio["fabricante"]
                acessorios[acessorio["nome"]]["especificacao"] = acessorio["especificacao"]
                acessorios[acessorio["nome"]]["descricao"] = acessorio["descricao"]
                acessorios[acessorio["nome"]]["codigo"] = acessorio["codigo"]
                acessorios[acessorio["nome"]]["precoUnit"] = acessorio["precoUnit"]
                acessorios[acessorio["nome"]]["url"] = acessorio["url"]
                acessorios[acessorio["nome"]]["imgSource"] = acessorio["imgSource"]
                acessorios_adicionados.append(acessorio["nome"])

    for pedra in pedras_adicionadas:
        (pedras[pedra]["area"]) = round((pedras[pedra]["area"]), 1)
        item_geral["pedras"].append(pedras[pedra])

    for acessorio in acessorios_adicionados:
        item_geral["acessorios"].append(acessorios[acessorio])

    return item_geral


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    dados_de_marmoraria = {}
    dados_de_marmoraria["projeto"] = ifc_projeto[0].LongName

    dados_de_marmoraria["apartamento"] = {}
    dados_de_marmoraria["apartamento"]["nome"] = ifc_projeto[0].LongName
    dados_de_marmoraria["apartamento"]["itens"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        if nome_da_etapa == "Marmoraria":

            for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                for rel in ifc_sub_etapa.HasAssignments:
                    obj = rel.RelatingProduct

                    if obj.is_a() == "IfcElementAssembly":
                        item = gera_dicionario_item(obj)
                        dados_de_marmoraria["apartamento"]["itens"].append(item)

    item_geral = gera_dicionario_item_geral(dados_de_marmoraria["apartamento"]["itens"])
    dados_de_marmoraria["apartamento"]["itens"].append(item_geral)

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            dados_de_marmoraria[nome_curto_do_ambiente] = {}
            dados_de_marmoraria[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            dados_de_marmoraria[nome_curto_do_ambiente]["itens"] = []

            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name

                if nome_da_etapa == "Marmoraria":

                    for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                        ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                        for rel in ifc_sub_etapa.HasAssignments:
                            obj = rel.RelatingProduct

                            if obj.is_a() == "IfcElementAssembly" and obj.ContainedInStructure[0].RelatingStructure.LongName == nome_do_ambiente:
                                item = gera_dicionario_item(obj)
                                dados_de_marmoraria[nome_curto_do_ambiente]["itens"].append(item)

            item_geral = gera_dicionario_item_geral(dados_de_marmoraria[nome_curto_do_ambiente]["itens"])
            dados_de_marmoraria[nome_curto_do_ambiente]["itens"].append(item_geral)

    json_de_marmoraria = "../../web/src/components/painel/contextos/marmoraria.json"
    with open(json_de_marmoraria, "w") as f:
        json.dump(dados_de_marmoraria, f, indent=2)
