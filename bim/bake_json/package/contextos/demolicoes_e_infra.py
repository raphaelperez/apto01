import json
from unidecode import unidecode


def demol_per(ifc_sub_etapa, nome_do_ambiente):
    demol_per = {}
    demol_per["id"] = nome_do_ambiente + "-demolicoes-per"
    demol_per["tipo"] = "Pisos e Revestimentos"
    demol_per["area"] = 0
    for ifc_obj in ifc_sub_etapa.OperatesOn[0].RelatedObjects:
        if ifc_obj.is_a() == "IfcCovering":
            ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
            if nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento":
                demol_per["area"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].AreaValue

    demol_per["area"] = round(demol_per["area"], 0)

    if demol_per["area"] == 0:
        return False
    else:
        return demol_per


def infra_eletrica_conduites(ifc_sub_etapa, nome_do_ambiente):
    infra_eletrica_conduites = {}
    infra_eletrica_conduites["id"] = nome_do_ambiente + "-infra-eletrica-conduites"
    infra_eletrica_conduites["tipo"] = "Conduítes"
    infra_eletrica_conduites["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            infra_eletrica_conduites["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    infra_eletrica_conduites["comprimento"] = round(infra_eletrica_conduites["comprimento"], 1)

    if infra_eletrica_conduites["comprimento"] == 0:
        return False
    else:
        return infra_eletrica_conduites


def infra_gas_tubos(ifc_sub_etapa, nome_do_ambiente):
    infra_gas_tubos = {}
    infra_gas_tubos["id"] = nome_do_ambiente + "-infra-gas-tubos"
    infra_gas_tubos["tipo"] = "Tubo de cobre"
    infra_gas_tubos["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            infra_gas_tubos["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    infra_gas_tubos["comprimento"] = round(infra_gas_tubos["comprimento"], 1)

    if infra_gas_tubos["comprimento"] == 0:
        return False
    else:
        return infra_gas_tubos


def infra_exaustao_dutos(ifc_sub_etapa, nome_do_ambiente):
    infra_exaustao_dutos = {}
    infra_exaustao_dutos["id"] = nome_do_ambiente + "-infra-exaustao-dutos"
    infra_exaustao_dutos["tipo"] = "Duto de exaustão"
    infra_exaustao_dutos["comprimento"] = 0
    for rel in ifc_sub_etapa.HasAssignments:
        ifc_obj = rel.RelatingProduct
        ambiente_do_objeto = unidecode(ifc_obj.ContainedInStructure[0].RelatingStructure.LongName.lower().replace(" ", ""))
        if ifc_obj.is_a() == "IfcPipeSegment" and (nome_do_ambiente == ambiente_do_objeto or nome_do_ambiente == "apartamento"):
            infra_exaustao_dutos["comprimento"] += ifc_obj.IsDefinedBy[0].RelatingPropertyDefinition.Quantities[0].LengthValue

    infra_exaustao_dutos["comprimento"] = round(infra_exaustao_dutos["comprimento"], 1)

    if infra_exaustao_dutos["comprimento"] == 0:
        return False
    else:
        return infra_exaustao_dutos


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto):
    dados_de_demoleinfra = {}
    dados_de_demoleinfra["projeto"] = ifc_projeto[0].Name

    dados_de_demoleinfra["apartamento"] = {}
    dados_de_demoleinfra["apartamento"]["nome"] = ifc_projeto[0].Name
    dados_de_demoleinfra["apartamento"]["itens"] = []

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

                if nome_da_sub_etapa == "Demolições" and demol_per(ifc_sub_etapa, "apartamento"):
                    tem_demolicoes = True
                    demolicoes["per"].append(demol_per(ifc_sub_etapa, "apartamento"))

                if nome_da_sub_etapa == "Infra Elétrica" and infra_eletrica_conduites(ifc_sub_etapa, "apartamento"):
                    tem_infra_eletrica = True
                    infra_eletrica["conduites"].append(infra_eletrica_conduites(ifc_sub_etapa, "apartamento"))

                if nome_da_sub_etapa == "Infra Gás" and infra_gas_tubos(ifc_sub_etapa, "apartamento"):
                    tem_infra_gas = True
                    infra_gas["tubos"].append(infra_gas_tubos(ifc_sub_etapa, "apartamento"))

                if nome_da_sub_etapa == "Infra Exaustão" and infra_exaustao_dutos(ifc_sub_etapa, "apartamento"):
                    tem_infra_exaustao = True
                    infra_exaustao["dutos"].append(infra_exaustao_dutos(ifc_sub_etapa, "apartamento"))

            if tem_demolicoes:
                dados_de_demoleinfra["apartamento"]["itens"].append(demolicoes)
            if tem_infra_eletrica:
                dados_de_demoleinfra["apartamento"]["itens"].append(infra_eletrica)
            if tem_infra_gas:
                dados_de_demoleinfra["apartamento"]["itens"].append(infra_gas)
            if tem_infra_exaustao:
                dados_de_demoleinfra["apartamento"]["itens"].append(infra_exaustao)

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            dados_de_demoleinfra[nome_curto_do_ambiente] = {}
            dados_de_demoleinfra[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            dados_de_demoleinfra[nome_curto_do_ambiente]["itens"] = []

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

                        if nome_da_sub_etapa == "Demolições" and demol_per(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_demolicoes = True
                            demolicoes["per"].append(demol_per(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Elétrica" and infra_eletrica_conduites(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_eletrica = True
                            infra_eletrica["conduites"].append(infra_eletrica_conduites(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Gás" and infra_gas_tubos(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_gas = True
                            infra_gas["tubos"].append(infra_gas_tubos(ifc_sub_etapa, nome_curto_do_ambiente))

                        if nome_da_sub_etapa == "Infra Exaustão" and infra_exaustao_dutos(ifc_sub_etapa, nome_curto_do_ambiente):
                            tem_infra_exaustao = True
                            infra_exaustao["dutos"].append(infra_exaustao_dutos(ifc_sub_etapa, nome_curto_do_ambiente))

                    if tem_demolicoes:
                        dados_de_demoleinfra[nome_curto_do_ambiente]["itens"].append(demolicoes)
                    if tem_infra_eletrica:
                        dados_de_demoleinfra[nome_curto_do_ambiente]["itens"].append(infra_eletrica)
                    if tem_infra_gas:
                        dados_de_demoleinfra[nome_curto_do_ambiente]["itens"].append(infra_gas)
                    if tem_infra_exaustao:
                        dados_de_demoleinfra[nome_curto_do_ambiente]["itens"].append(infra_exaustao)

    json_de_demolicoes = "../../web/src/components/painel/contextos/demolicoesEInfra.json"
    with open(json_de_demolicoes, "w") as f:
        json.dump(dados_de_demoleinfra, f, indent=2)
