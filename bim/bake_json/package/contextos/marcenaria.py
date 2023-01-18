import json
from unidecode import unidecode


def gera_dicionario_item(obj):
    item = {}

    item["item"] = obj.Description
    item["mdfs"] = []
    item["acessorios"] = []

    mdfs = {}
    mdf_adicionado = []
    for parte in obj.IsDecomposedBy[0].RelatedObjects:
        if parte.is_a() == "IfcPlate":
            ifc_material = parte.HasAssociations[0].RelatingMaterial
            material_do_mdf = ifc_material.Name

            perimetro = 1
            largura = 1
            for propriedade in parte.IsDefinedBy[0].RelatingPropertyDefinition.Quantities:
                if propriedade.Name == "Perimeter":
                    perimetro = propriedade.LengthValue
                elif propriedade.Name == "Width":
                    largura = propriedade.LengthValue

            area = largura * (perimetro - (2 * largura)) / 2

            if material_do_mdf not in mdf_adicionado:
                mdfs[material_do_mdf] = {}
                mdfs[material_do_mdf]["nome"] = material_do_mdf
                mdfs[material_do_mdf]["fabricante"] = ifc_material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                mdfs[material_do_mdf]["especificacao"] = ifc_material.HasProperties[0].Properties[1].NominalValue.wrappedValue
                mdfs[material_do_mdf]["espessura"] = ifc_material.HasProperties[0].Properties[2].NominalValue.wrappedValue
                mdfs[material_do_mdf]["precoUnit"] = ifc_material.HasProperties[0].Properties[3].NominalValue.wrappedValue
                mdfs[material_do_mdf]["url"] = ifc_material.HasProperties[0].Properties[4].NominalValue.wrappedValue
                mdfs[material_do_mdf]["area"] = area
                mdfs[material_do_mdf]["imgSource"] = (
                    "./img/"
                    + unidecode(mdfs[material_do_mdf]["fabricante"].lower().replace(" ", ""))
                    + "-"
                    + unidecode(mdfs[material_do_mdf]["especificacao"].lower().replace(" ", ""))
                    + ".jpg"
                )
                mdf_adicionado.append(material_do_mdf)
            elif material_do_mdf in mdf_adicionado:
                mdfs[material_do_mdf]["area"] += area

    for mdf in mdf_adicionado:
        (mdfs[mdf]["area"]) = round((mdfs[mdf]["area"]), 1)
        item["mdfs"].append(mdfs[mdf])

    return item


def gera_dicionario_item_geral(itens):
    item_geral = {}
    item_geral["item"] = "Geral"
    item_geral["mdfs"] = []
    item_geral["acessorios"] = []
    mdfs_adicionados = []
    mdfs = {}
    for item in itens:
        for mdf in item["mdfs"]:
            if mdf["nome"] not in mdfs_adicionados:
                mdfs[mdf["nome"]] = {}
                mdfs[mdf["nome"]]["nome"] = mdf["nome"]
                mdfs[mdf["nome"]]["fabricante"] = mdf["fabricante"]
                mdfs[mdf["nome"]]["especificacao"] = mdf["especificacao"]
                mdfs[mdf["nome"]]["espessura"] = mdf["espessura"]
                mdfs[mdf["nome"]]["precoUnit"] = mdf["precoUnit"]
                mdfs[mdf["nome"]]["url"] = mdf["url"]
                mdfs[mdf["nome"]]["area"] = mdf["area"]
                mdfs[mdf["nome"]]["imgSource"] = mdf["imgSource"]
                mdfs_adicionados.append(mdf["nome"])
            else:
                mdfs[mdf["nome"]]["area"] += mdf["area"]

    for mdf in mdfs_adicionados:
        (mdfs[mdf]["area"]) = round((mdfs[mdf]["area"]), 1)
        item_geral["mdfs"].append(mdfs[mdf])

    return item_geral


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    dados_de_marcenaria = {}
    dados_de_marcenaria["projeto"] = ifc_projeto[0].LongName

    dados_de_marcenaria["apartamento"] = {}
    dados_de_marcenaria["apartamento"]["nome"] = ifc_projeto[0].LongName
    dados_de_marcenaria["apartamento"]["itens"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        if nome_da_etapa == "Marcenaria":

            for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                for rel in ifc_sub_etapa.HasAssignments:
                    obj = rel.RelatingProduct

                    if obj.is_a() == "IfcElementAssembly":
                        item = gera_dicionario_item(obj)
                        dados_de_marcenaria["apartamento"]["itens"].append(item)

    item_geral = gera_dicionario_item_geral(dados_de_marcenaria["apartamento"]["itens"])
    dados_de_marcenaria["apartamento"]["itens"].append(item_geral)

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            dados_de_marcenaria[nome_curto_do_ambiente] = {}
            dados_de_marcenaria[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            dados_de_marcenaria[nome_curto_do_ambiente]["itens"] = []

            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name

                if nome_da_etapa == "Marcenaria":

                    for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                        ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]

                        for rel in ifc_sub_etapa.HasAssignments:
                            obj = rel.RelatingProduct

                            if obj.is_a() == "IfcElementAssembly" and obj.ContainedInStructure[0].RelatingStructure.LongName == nome_do_ambiente:
                                item = gera_dicionario_item(obj)
                                dados_de_marcenaria[nome_curto_do_ambiente]["itens"].append(item)

            item_geral = gera_dicionario_item_geral(dados_de_marcenaria[nome_curto_do_ambiente]["itens"])
            dados_de_marcenaria[nome_curto_do_ambiente]["itens"].append(item_geral)

    json_de_marcenaria = "../../web/src/components/painel/contextos/marcenaria.json"
    with open(json_de_marcenaria, "w") as f:
        json.dump(dados_de_marcenaria, f, indent=2)
