import json
from unidecode import unidecode


def gera_modelos(ifc_ambientes, ifc_etapas_por_id):
    modelos = {}

    for ifc_space in ifc_ambientes:
        ambiente = ifc_space.LongName
        ambiente_min = unidecode(ambiente.lower().replace(" ", ""))
        modelos[ambiente_min] = {}

        portas_da_etapa_anterior = []
        objetos_da_etapa_anterior = []
        for i in range(len(ifc_etapas_por_id)):
            etapa = ifc_etapas_por_id[i + 1]["etapa"].Name
            etapa_min = unidecode(etapa.lower().replace(" ", ""))
            modelos[ambiente_min][etapa_min] = {}
            modelos[ambiente_min][etapa_min]["objetos"] = []
            modelos[ambiente_min][etapa_min]["texturaObjetos"] = ambiente_min + "-" + etapa_min
            modelos[ambiente_min][etapa_min]["portas"] = []
            modelos[ambiente_min][etapa_min]["texturaPortas"] = "portas-" + etapa_min

            portas_da_sub_etapa_anterior = []
            objetos_da_sub_etapa_anterior = []
            for sub_i in range(len(ifc_etapas_por_id[i + 1]["sub_etapas"])):
                ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i + 1]

                etapa_de_demolicao = False
                etapa_de_construcao = False
                etapa_de_alteracao = False
                try:
                    if ifc_sub_etapa.OperatesOn[0] and ifc_sub_etapa.HasAssignments:
                        etapa_de_alteracao = ifc_sub_etapa
                    elif ifc_sub_etapa.OperatesOn[0]:
                        etapa_de_demolicao = ifc_sub_etapa
                except:
                    if ifc_sub_etapa.HasAssignments:
                        etapa_de_construcao = ifc_sub_etapa
                finally:
                    if etapa_de_construcao:
                        for objeto_da_etapa_anterior in objetos_da_etapa_anterior:
                            if objeto_da_etapa_anterior not in objetos_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["objetos"].append(objeto_da_etapa_anterior)
                                objetos_da_sub_etapa_anterior.append(objeto_da_etapa_anterior)

                        for porta_da_etapa_anterior in portas_da_etapa_anterior:
                            if porta_da_etapa_anterior not in portas_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["portas"].append(porta_da_etapa_anterior)
                                portas_da_sub_etapa_anterior.append(porta_da_etapa_anterior)

                        for rel in etapa_de_construcao.HasAssignments:
                            if rel.is_a() == "IfcRelAssignsToProduct":
                                obj = rel.RelatingProduct
                                ambiente_do_objeto = obj.ContainedInStructure[0].RelatingStructure.LongName
                                objeto = obj.Name

                                if ambiente_do_objeto == ambiente and objeto:
                                    if obj.is_a() == "IfcElementAssembly":
                                        for parte_da_montagem in obj.IsDecomposedBy[0].RelatedObjects:
                                            objeto = parte_da_montagem.is_a() + parte_da_montagem.Name
                                            if objeto not in objetos_da_sub_etapa_anterior:
                                                modelos[ambiente_min][etapa_min]["objetos"].append(objeto)
                                                objetos_da_etapa_anterior.append(objeto)
                                                objetos_da_sub_etapa_anterior.append(objeto)

                                    else:
                                        objeto = obj.is_a() + obj.Name
                                        if objeto not in objetos_da_sub_etapa_anterior:
                                            modelos[ambiente_min][etapa_min]["objetos"].append(objeto)
                                            objetos_da_etapa_anterior.append(objeto)
                                            objetos_da_sub_etapa_anterior.append(objeto)

                                if obj.is_a() == "IfcDoor":
                                    porta = obj.is_a() + obj.Name
                                    porta_vem_de = obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue
                                    porta_vai_para = obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue
                                    if porta_vem_de == ambiente or porta_vai_para == ambiente:
                                        modelos[ambiente_min][etapa_min]["portas"].append(porta)
                                        portas_da_etapa_anterior.append(porta)
                                        portas_da_sub_etapa_anterior.append(porta)

                    elif etapa_de_demolicao:
                        for objeto_da_etapa_anterior in objetos_da_etapa_anterior:
                            if objeto_da_etapa_anterior not in objetos_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["objetos"].append(objeto_da_etapa_anterior)
                                objetos_da_sub_etapa_anterior.append(objeto_da_etapa_anterior)

                        for porta_da_etapa_anterior in portas_da_etapa_anterior:
                            if porta_da_etapa_anterior not in portas_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["portas"].append(porta_da_etapa_anterior)
                                portas_da_sub_etapa_anterior.append(porta_da_etapa_anterior)

                        for obj in etapa_de_demolicao.OperatesOn[0].RelatedObjects:
                            objeto_demolido = obj.is_a() + obj.Name
                            if objeto_demolido in objetos_da_etapa_anterior:
                                objetos_da_etapa_anterior.remove(objeto_demolido)
                            if objeto_demolido in portas_da_etapa_anterior:
                                portas_da_etapa_anterior.remove(objeto_demolido)

                    elif etapa_de_alteracao:
                        for objeto_da_etapa_anterior in objetos_da_etapa_anterior:
                            if objeto_da_etapa_anterior not in objetos_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["objetos"].append(objeto_da_etapa_anterior)
                                objetos_da_sub_etapa_anterior.append(objeto_da_etapa_anterior)

                        for porta_da_etapa_anterior in portas_da_etapa_anterior:
                            if porta_da_etapa_anterior not in portas_da_sub_etapa_anterior:
                                modelos[ambiente_min][etapa_min]["portas"].append(porta_da_etapa_anterior)
                                portas_da_sub_etapa_anterior.append(porta_da_etapa_anterior)

                        for obj in etapa_de_alteracao.OperatesOn[0].RelatedObjects:
                            objeto_demolido = obj.is_a() + obj.Name
                            if objeto_demolido in objetos_da_etapa_anterior:
                                objetos_da_etapa_anterior.remove(objeto_demolido)
                            if objeto_demolido in portas_da_etapa_anterior:
                                portas_da_etapa_anterior.remove(objeto_demolido)
                            if objeto_demolido in modelos[ambiente_min][etapa_min]["objetos"]:
                                modelos[ambiente_min][etapa_min]["objetos"].remove(objeto_demolido)
                            if objeto_demolido in modelos[ambiente_min][etapa_min]["portas"]:
                                modelos[ambiente_min][etapa_min]["portas"].remove(objeto_demolido)

                        for rel in etapa_de_alteracao.HasAssignments:
                            if rel.is_a() == "IfcRelAssignsToProduct":
                                obj = rel.RelatingProduct
                                ambiente_do_objeto = obj.ContainedInStructure[0].RelatingStructure.LongName
                                objeto = obj.Name
                                if ambiente_do_objeto == ambiente and objeto:
                                    if obj.is_a() == "IfcElementAssembly":
                                        for parte_da_montagem in obj.IsDecomposedBy[0].RelatedObjects:
                                            objeto = parte_da_montagem.is_a() + parte_da_montagem.Name
                                            if objeto not in objetos_da_sub_etapa_anterior:
                                                modelos[ambiente_min][etapa_min]["objetos"].append(objeto)
                                                objetos_da_etapa_anterior.append(objeto)
                                                objetos_da_sub_etapa_anterior.append(objeto)
                                    else:
                                        objeto = obj.is_a() + obj.Name
                                        if objeto not in objetos_da_sub_etapa_anterior:
                                            modelos[ambiente_min][etapa_min]["objetos"].append(objeto)
                                            objetos_da_etapa_anterior.append(objeto)
                                            objetos_da_sub_etapa_anterior.append(objeto)

                                    if obj.is_a() == "IfcDoor":
                                        porta = obj.is_a() + obj.Name
                                        porta_vem_de = obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue
                                        porta_vai_para = obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue
                                        if porta_vem_de == ambiente or porta_vai_para == ambiente:
                                            modelos[ambiente_min][etapa_min]["portas"].append(porta)
                                            portas_da_etapa_anterior.append(porta)
                                            portas_da_sub_etapa_anterior.append(porta)

    apartamento = {}
    for ambiente in modelos:
        for etapa in modelos[ambiente]:
            apartamento[etapa] = {}
            apartamento[etapa]["portas"] = []
            apartamento[etapa]["texturaPortas"] = modelos[ambiente][etapa]["texturaPortas"]

    for ambiente in modelos:
        for etapa in modelos[ambiente]:
            for porta in modelos[ambiente][etapa]["portas"]:
                apartamento[etapa]["portas"].append(porta)

    for etapa in apartamento:
        portas = []
        for porta in apartamento[etapa]["portas"]:
            if porta not in portas:
                portas.append(porta)
        apartamento[etapa]["portas"] = portas

    modelos["apartamento"] = apartamento

    return modelos


def bake_json(ifc_ambientes, ifc_etapas_por_id, etapas_por_ambiente, ifc_apartamento):

    modelos = gera_modelos(ifc_ambientes, ifc_etapas_por_id)

    json_modelos = "../../web/src/componentes/grafico3D/modelos/modelos.json"
    with open(json_modelos, "w") as f:
        json.dump(modelos, f, indent=2)
