import json
from unidecode import unidecode


def gera_meshes_ambientes(ifc_ambientes, ifc_etapas_por_id):
    meshes_ambientes = {}

    for ifc_space in ifc_ambientes:
        nome_do_ambiente = ifc_space.LongName
        nome_curto_do_ambiente = unidecode(nome_do_ambiente.lower().replace(" ", ""))
        meshes_ambientes[nome_curto_do_ambiente] = {}

        meshes_da_etapa_anterior = []
        for i in range(len(ifc_etapas_por_id)):
            nome_da_etapa = ifc_etapas_por_id[i + 1]["etapa"].Name
            nome_curto_da_etapa = unidecode(nome_da_etapa.lower().replace(" ", ""))
            meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa] = []

            meshes_adicionados_na_sub_etapa_anterior = []
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
                        for mesh_da_etapa_anterior in meshes_da_etapa_anterior:
                            if mesh_da_etapa_anterior not in meshes_adicionados_na_sub_etapa_anterior:
                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(mesh_da_etapa_anterior)
                                meshes_adicionados_na_sub_etapa_anterior.append(mesh_da_etapa_anterior)

                        for rel in etapa_de_construcao.HasAssignments:
                            if rel.is_a() == "IfcRelAssignsToProduct":
                                obj = rel.RelatingProduct
                                nome_do_ambiente_do_objeto = obj.ContainedInStructure[0].RelatingStructure.LongName
                                nome_do_objeto = obj.Name
                                if nome_do_ambiente_do_objeto == nome_do_ambiente and nome_do_objeto:
                                    if obj.is_a() == "IfcElementAssembly":

                                        for parte_da_montagem in obj.IsDecomposedBy[0].RelatedObjects:
                                            nome_do_mesh = parte_da_montagem.is_a() + parte_da_montagem.Name
                                            if nome_do_mesh not in meshes_adicionados_na_sub_etapa_anterior:
                                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(nome_do_mesh)
                                                meshes_da_etapa_anterior.append(nome_do_mesh)
                                                meshes_adicionados_na_sub_etapa_anterior.append(nome_do_mesh)

                                    else:
                                        nome_do_mesh = obj.is_a() + obj.Name
                                        if nome_do_mesh not in meshes_adicionados_na_sub_etapa_anterior:
                                            meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(nome_do_mesh)
                                            meshes_da_etapa_anterior.append(nome_do_mesh)
                                            meshes_adicionados_na_sub_etapa_anterior.append(nome_do_mesh)

                    elif etapa_de_demolicao:
                        for mesh_da_etapa_anterior in meshes_da_etapa_anterior:
                            if mesh_da_etapa_anterior not in meshes_adicionados_na_sub_etapa_anterior:
                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(mesh_da_etapa_anterior)
                                meshes_adicionados_na_sub_etapa_anterior.append(mesh_da_etapa_anterior)

                        for obj in etapa_de_demolicao.OperatesOn[0].RelatedObjects:
                            nome_do_mesh_demolido = obj.is_a() + obj.Name
                            if nome_do_mesh_demolido in meshes_da_etapa_anterior:
                                meshes_da_etapa_anterior.remove(nome_do_mesh_demolido)

                    elif etapa_de_alteracao:
                        for mesh_da_etapa_anterior in meshes_da_etapa_anterior:
                            if mesh_da_etapa_anterior not in meshes_adicionados_na_sub_etapa_anterior:
                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(mesh_da_etapa_anterior)
                                meshes_adicionados_na_sub_etapa_anterior.append(mesh_da_etapa_anterior)

                        for obj in etapa_de_alteracao.OperatesOn[0].RelatedObjects:
                            nome_do_mesh_demolido = obj.is_a() + obj.Name
                            if nome_do_mesh_demolido in meshes_da_etapa_anterior:
                                meshes_da_etapa_anterior.remove(nome_do_mesh_demolido)
                            if nome_do_mesh_demolido in meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa]:
                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].remove(nome_do_mesh_demolido)

                        for rel in etapa_de_alteracao.HasAssignments:
                            if rel.is_a() == "IfcRelAssignsToProduct":
                                obj = rel.RelatingProduct
                                nome_do_ambiente_do_objeto = obj.ContainedInStructure[0].RelatingStructure.LongName
                                nome_do_objeto = obj.Name
                                if nome_do_ambiente_do_objeto == nome_do_ambiente and nome_do_objeto:
                                    if obj.is_a() == "IfcElementAssembly":
                                        for parte_da_montagem in obj.IsDecomposedBy[0].RelatedObjects:
                                            nome_do_mesh = parte_da_montagem.is_a() + parte_da_montagem.Name
                                            if nome_do_mesh not in meshes_adicionados_na_sub_etapa_anterior:
                                                meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(nome_do_mesh)
                                                meshes_da_etapa_anterior.append(nome_do_mesh)
                                                meshes_adicionados_na_sub_etapa_anterior.append(nome_do_mesh)
                                    else:
                                        nome_do_mesh = obj.is_a() + obj.Name
                                        if nome_do_mesh not in meshes_adicionados_na_sub_etapa_anterior:
                                            meshes_ambientes[nome_curto_do_ambiente][nome_curto_da_etapa].append(nome_do_mesh)
                                            meshes_da_etapa_anterior.append(nome_do_mesh)
                                            meshes_adicionados_na_sub_etapa_anterior.append(nome_do_mesh)

    return meshes_ambientes


def gera_meshes_portas(ifc_apartamento, etapas_por_ambiente):
    meshes_portas = {}

    etapas = []
    ambientes = []

    for ambiente in etapas_por_ambiente:
        meshes_portas[etapas_por_ambiente[ambiente]["nome_curto"]] = {}
        for etapa in etapas_por_ambiente[ambiente]["etapas"]:
            meshes_portas[etapas_por_ambiente[ambiente]["nome_curto"]][etapa["nome_curto"]] = []
            if etapa["nome_curto"] not in etapas:
                etapas.append(etapa["nome_curto"])
            if ambiente not in ambientes:
                ambientes.append(ambiente)

    meshes_portas["apartamento"] = {}
    for etapa in etapas:
        meshes_portas["apartamento"][etapa] = []

    portas = []
    for elemento in ifc_apartamento[0].ContainsElements[0].RelatedElements:
        if elemento.is_a() == "IfcDoor":
            portas.append(elemento)

    for porta in portas:
        nome_da_porta = porta.is_a() + porta.Name
        porta_vem_de = unidecode(porta.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue.lower().replace(" ", ""))
        porta_vai_para = unidecode(
            porta.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue.lower().replace(" ", "")
        )

        if porta_vem_de in ambientes:
            for etapa in meshes_portas[porta_vem_de]:
                meshes_portas[porta_vem_de][etapa].append(nome_da_porta)

        if porta_vai_para in ambientes:
            for etapa in meshes_portas[porta_vai_para]:
                meshes_portas[porta_vai_para][etapa].append(nome_da_porta)

        for etapa in etapas:
            meshes_portas["apartamento"][etapa].append(nome_da_porta)

    return meshes_portas


def bake_json(ifc_ambientes, ifc_etapas_por_id, etapas_por_ambiente, ifc_apartamento):

    meshes_ambientes = gera_meshes_ambientes(ifc_ambientes, ifc_etapas_por_id)

    meshes_portas = gera_meshes_portas(ifc_apartamento, etapas_por_ambiente)

    json_meshes_ambientes = "../../web/src/components/tresD/meshes/meshesAmbientes.json"
    with open(json_meshes_ambientes, "w") as f:
        json.dump(meshes_ambientes, f, indent=2)

    json_meshes_portas = "../../web/src/components/tresD/meshes/meshesPortas.json"
    with open(json_meshes_portas, "w") as f:
        json.dump(meshes_portas, f, indent=2)
