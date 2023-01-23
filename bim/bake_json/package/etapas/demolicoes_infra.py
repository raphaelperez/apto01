import json
from unidecode import unidecode


def per(ifc_sub_etapa, nome_do_ambiente):
    per = {}
    per["id"] = nome_do_ambiente + "-demolicoes-per"
    per["tipo"] = "Pisos e Revestimentos"
    per["area"] = 0
    for ifc_obj in ifc_sub_etapa.OperatesOn[0].RelatedObjects:
        if ifc_obj.is_a() == "IfcCovering":
            ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
            if nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento":
                per["area"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue

    per["area"] = round(per["area"], 0)

    if per["area"] == 0:
        return False
    else:
        return per


def portas(ifc_sub_etapa, nome_do_ambiente):
    portas = {}
    portas_de_madeira = {}
    portas_de_madeira["id"] = nome_do_ambiente + "-" + ifc_sub_etapa.Name + "-portas-de-madeira"
    portas_de_madeira["tipo"] = "Portas de madeira"
    portas_de_madeira["quantidade"] = 0
    for ifc_obj in ifc_sub_etapa.OperatesOn[0].RelatedObjects:
        if ifc_obj.is_a() == "IfcDoor":
            if ifc_obj.ObjectType == "Porta de madeira":
                portas_de_madeira["quantidade"] += 1

    if portas_de_madeira["quantidade"] > 0:
        portas["portasDeMadeira"] = portas_de_madeira

    return portas


def eletrica_conduites(ifc_sub_etapa, nome_do_ambiente):
    eletrica_conduites = {}
    eletrica_conduites["id"] = nome_do_ambiente + "-infra-eletrica-conduites"
    eletrica_conduites["tipo"] = "Conduítes"
    eletrica_conduites["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            eletrica_conduites["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    eletrica_conduites["comprimento"] = round(eletrica_conduites["comprimento"], 1)

    if eletrica_conduites["comprimento"] == 0:
        return False
    else:
        return eletrica_conduites


def gas_tubos(ifc_sub_etapa, nome_do_ambiente):
    gas_tubos = {}
    gas_tubos["id"] = nome_do_ambiente + "-infra-gas-tubos"
    gas_tubos["tipo"] = "Tubo de cobre"
    gas_tubos["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            gas_tubos["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    gas_tubos["comprimento"] = round(gas_tubos["comprimento"], 1)

    if gas_tubos["comprimento"] == 0:
        return False
    else:
        return gas_tubos


def exaustao_dutos(ifc_sub_etapa, nome_do_ambiente):
    exaustao_dutos = {}
    exaustao_dutos["id"] = nome_do_ambiente + "-infra-exaustao-dutos"
    exaustao_dutos["tipo"] = "Duto de exaustão"
    exaustao_dutos["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            exaustao_dutos["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    exaustao_dutos["comprimento"] = round(exaustao_dutos["comprimento"], 1)

    if exaustao_dutos["comprimento"] == 0:
        return False
    else:
        return exaustao_dutos


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    demolicoes_infra = {}
    demolicoes_infra["projeto"] = ifc_projeto[0].Name

    demolicoes_infra["apartamento"] = {}
    demolicoes_infra["apartamento"]["nome"] = ifc_projeto[0].Name
    demolicoes_infra["apartamento"]["itens"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        if nome_da_etapa == "Demolições e Infra":
            tem_demolicoes = False
            demolicoes = {}
            demolicoes["item"] = "Demolições"
            demolicoes["per"] = []
            demolicoes["portas"] = []

            tem_infra_eletrica = False
            infra_eletrica = {}
            infra_eletrica["item"] = "Infra Elétrica"
            infra_eletrica["conduites"] = []

            tem_infra_gas = False
            infra_gas = {}
            infra_gas["item"] = "Infra Gás"
            infra_gas["tubos"] = []

            tem_infra_exaustao = False
            infra_exaustao = {}
            infra_exaustao["item"] = "Infra Exaustão"
            infra_exaustao["dutos"] = []

            for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]
                nome_da_sub_etapa = ifc_sub_etapa.Name

                if nome_da_sub_etapa == "Demolições" and per(ifc_sub_etapa, "apartamento"):
                    tem_demolicoes = True
                    demolicoes["per"].append(per(ifc_sub_etapa, "apartamento"))
                    tipos_de_portas = portas(ifc_sub_etapa, "apartamento")
                    for tipo_de_porta in tipos_de_portas:
                        demolicoes["portas"].append(tipos_de_portas[tipo_de_porta])

                if nome_da_sub_etapa == "Infra Elétrica" and eletrica_conduites(ifc_sub_etapa, "apartamento"):
                    tem_infra_eletrica = True
                    infra_eletrica["conduites"].append(eletrica_conduites(ifc_sub_etapa, "apartamento"))

                if nome_da_sub_etapa == "Infra Gás" and gas_tubos(ifc_sub_etapa, "apartamento"):
                    tem_infra_gas = True
                    infra_gas["tubos"].append(gas_tubos(ifc_sub_etapa, "apartamento"))

                if nome_da_sub_etapa == "Infra Exaustão" and exaustao_dutos(ifc_sub_etapa, "apartamento"):
                    tem_infra_exaustao = True
                    infra_exaustao["dutos"].append(exaustao_dutos(ifc_sub_etapa, "apartamento"))

            if tem_demolicoes:
                demolicoes_infra["apartamento"]["itens"].append(demolicoes)
            if tem_infra_eletrica:
                demolicoes_infra["apartamento"]["itens"].append(infra_eletrica)
            if tem_infra_gas:
                demolicoes_infra["apartamento"]["itens"].append(infra_gas)
            if tem_infra_exaustao:
                demolicoes_infra["apartamento"]["itens"].append(infra_exaustao)

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            demolicoes_infra[nome_curto_do_ambiente] = {}
            demolicoes_infra[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            demolicoes_infra[nome_curto_do_ambiente]["itens"] = []

            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name

                if nome_da_etapa == "Demolições e Infra":
                    tem_demolicoes = False
                    demolicoes = {}
                    demolicoes["item"] = "Demolições"
                    demolicoes["per"] = []

                    tem_infra_eletrica = False
                    infra_eletrica = {}
                    infra_eletrica["item"] = "Infra Elétrica"
                    infra_eletrica["conduites"] = []

                    tem_infra_gas = False
                    infra_gas = {}
                    infra_gas["item"] = "Infra Gás"
                    infra_gas["tubos"] = []

                    tem_infra_exaustao = False
                    infra_exaustao = {}
                    infra_exaustao["item"] = "Infra Exaustão"
                    infra_exaustao["dutos"] = []

                    for sub_i in ifc_etapas_por_id[i + 1]["sub_etapas"]:
                        ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i]
                        nome_da_sub_etapa = ifc_sub_etapa.Name

                        if nome_da_sub_etapa == "Demolições" and per(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_demolicoes = True
                            demolicoes["per"].append(per(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Elétrica" and eletrica_conduites(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_eletrica = True
                            infra_eletrica["conduites"].append(eletrica_conduites(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Gás" and gas_tubos(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_gas = True
                            infra_gas["tubos"].append(gas_tubos(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Exaustão" and exaustao_dutos(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_exaustao = True
                            infra_exaustao["dutos"].append(exaustao_dutos(ifc_sub_etapa, nome_curto_do_ambiente))

                    if tem_demolicoes:
                        demolicoes_infra[nome_curto_do_ambiente]["itens"].append(demolicoes)
                    if tem_infra_eletrica:
                        demolicoes_infra[nome_curto_do_ambiente]["itens"].append(infra_eletrica)
                    if tem_infra_gas:
                        demolicoes_infra[nome_curto_do_ambiente]["itens"].append(infra_gas)
                    if tem_infra_exaustao:
                        demolicoes_infra[nome_curto_do_ambiente]["itens"].append(infra_exaustao)

    json_de_demolicoes = "../../web/src/componentes/painel/etapas/demolicoesInfra.json"
    with open(json_de_demolicoes, "w") as f:
        json.dump(demolicoes_infra, f, indent=2)
