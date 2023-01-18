from unidecode import unidecode


def gera_etapas_por_ambiente(ifc_ambientes, ifc_etapas_por_id):
    etapas_por_ambiente = {}

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            id_do_ambiente = ifc_ambiente.Name
            nome_do_ambiente = ifc_ambiente.LongName
            nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))

            etapas_por_ambiente[nome_curto_do_ambiente] = {}
            etapas_por_ambiente[nome_curto_do_ambiente]["nome"] = nome_do_ambiente
            etapas_por_ambiente[nome_curto_do_ambiente]["nome_curto"] = nome_curto_do_ambiente
            etapas_por_ambiente[nome_curto_do_ambiente]["etapas"] = []

            etapas_adicionada = []
            for i in range(len(ifc_etapas_por_id)):
                ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
                nome_da_etapa = ifc_etapa.Name
                nome_curto_da_etapa = unidecode(nome_da_etapa.lower().replace(" ", ""))

                for sub_i in range(len(ifc_etapas_por_id[i + 1]["sub_etapas"])):
                    ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i + 1]

                    etapa_de_demolicao = False
                    etapa_de_construcao = False
                    try:
                        if ifc_sub_etapa.OperatesOn[0]:
                            etapa_de_demolicao = ifc_sub_etapa
                    except:
                        if len(ifc_sub_etapa.HasAssignments) > 1:
                            etapa_de_construcao = ifc_sub_etapa
                    finally:
                        if etapa_de_demolicao:
                            for obj in etapa_de_demolicao.OperatesOn[0].RelatedObjects:
                                if (
                                    obj.ContainedInStructure[0].RelatingStructure.LongName == nome_do_ambiente
                                    and (nome_da_etapa) not in etapas_adicionada
                                ):
                                    etapa_do_ambiente = {
                                        "nome_curto": nome_curto_da_etapa,
                                        "nome": nome_da_etapa,
                                    }
                                    etapas_adicionada.append(nome_da_etapa)
                                    etapas_por_ambiente[nome_curto_do_ambiente]["etapas"].append(etapa_do_ambiente)
                        elif etapa_de_construcao:
                            for rel in etapa_de_construcao.HasAssignments:
                                if rel.is_a() == "IfcRelAssignsToProduct":
                                    obj = rel.RelatingProduct
                                    if (
                                        obj.ContainedInStructure[0].RelatingStructure.LongName == nome_do_ambiente
                                        and (nome_da_etapa) not in etapas_adicionada
                                    ):
                                        etapa_do_ambiente = {
                                            "nome_curto": nome_curto_da_etapa,
                                            "nome": nome_da_etapa,
                                        }
                                        etapas_adicionada.append(nome_da_etapa)
                                        etapas_por_ambiente[nome_curto_do_ambiente]["etapas"].append(etapa_do_ambiente)

    return etapas_por_ambiente


def gera_ifc_etapas_por_id(ifc_etapas):
    ifc_etapas_por_id = {}
    for ifc_etapa in ifc_etapas:
        if len(ifc_etapa.Identification) == 1:
            id = int(ifc_etapa.Identification)  # type: ignore
            ifc_etapas_por_id[id] = {}
            ifc_etapas_por_id[id]["etapa"] = ifc_etapa
            ifc_etapas_por_id[id]["sub_etapas"] = {}

    for ifc_etapa in ifc_etapas:
        if len(ifc_etapa.Identification) > 1:
            id = int(ifc_etapa.Identification[0])
            sub_id = int(ifc_etapa.Identification[2])  # type: ignore
            ifc_etapas_por_id[id]["sub_etapas"][sub_id] = ifc_etapa

    return ifc_etapas_por_id
