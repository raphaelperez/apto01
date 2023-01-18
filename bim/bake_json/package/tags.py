import json
from unidecode import unidecode


def gera_dicionario_placa(placa, elemento, nome_do_ambiente, nome_da_etapa):
    material = placa.HasAssociations[0].RelatingMaterial
    nome_do_material = ""

    try:
        if material.HasProperties[0].Name == "Covering_material":
            nome_do_material = (
                material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                + " - "
                + material.HasProperties[0].Properties[1].NominalValue.wrappedValue
            )
        elif material.HasProperties[0].Name == "Marble_material":
            nome_do_material = (
                material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                + " - "
                + material.HasProperties[0].Properties[1].NominalValue.wrappedValue
            )
    except:
        nome_do_material = "none"

    dict_da_placa = {}
    dict_da_placa["material"] = material.Name
    dict_da_placa["nomeDoMaterial"] = nome_do_material
    dict_da_placa["montagem"] = elemento.Description
    dict_da_placa["ambiente"] = nome_do_ambiente
    dict_da_placa["etapa"] = nome_da_etapa

    return dict_da_placa


def gera_dicionario_term_san(obj, elemento, nome_do_ambiente, nome_da_etapa):
    nome_do_material = (
        obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue
        + " - "
        + obj.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue
    )

    dict_do_obj = {}
    dict_do_obj["material"] = obj.Name
    dict_do_obj["nomeDoMaterial"] = nome_do_material
    dict_do_obj["montagem"] = elemento.Description
    dict_do_obj["ambiente"] = nome_do_ambiente
    dict_do_obj["etapa"] = nome_da_etapa

    return dict_do_obj


def bake_json(ifc_ambientes):
    dados_das_tags = {}

    elementos_sem_material = ["IfcOutlet", "IfcSwitchingDevice", "IfcFlowTerminal", "IfcPipeSegment"]

    for ifc_ambiente in ifc_ambientes:
        nome_do_ambiente = ifc_ambiente.LongName
        for elemento in ifc_ambiente.ContainsElements[0].RelatedElements:
            if elemento.is_a() == "IfcElementAssembly":
                try:
                    nome_da_etapa = elemento.HasAssignments[0].RelatingProcess.Nests[0].RelatingObject.Name
                except:
                    nome_da_etapa = elemento.ReferencedBy[0].RelatedObjects[0].Nests[0].RelatingObject.Name

                for parte in elemento.IsDecomposedBy[0].RelatedObjects:
                    if parte.is_a() == "IfcPlate":
                        nome_da_parte = parte.is_a() + parte.Name
                        dados_das_tags[nome_da_parte] = gera_dicionario_placa(parte, elemento, nome_do_ambiente, nome_da_etapa)
                    elif parte.is_a() == "IfcSanitaryTerminal":
                        nome_da_parte = parte.is_a() + parte.Name
                        dados_das_tags[nome_da_parte] = gera_dicionario_term_san(parte, elemento, nome_do_ambiente, nome_da_etapa)

            else:
                nome_do_elemento = elemento.is_a() + elemento.Name

                try:
                    nome_da_etapa = elemento.HasAssignments[0].RelatingProcess.Nests[0].RelatingObject.Name
                except:
                    nome_da_etapa = elemento.ReferencedBy[0].RelatedObjects[0].Nests[0].RelatingObject.Name

                if elemento.is_a() in elementos_sem_material:
                    dados_das_tags[nome_do_elemento] = {}
                    dados_das_tags[nome_do_elemento]["material"] = "Elétrica"
                    dados_das_tags[nome_do_elemento]["nomeDoMaterial"] = "Tomada ou Interruptor"
                    dados_das_tags[nome_do_elemento]["ambiente"] = nome_do_ambiente
                    dados_das_tags[nome_do_elemento]["etapa"] = nome_da_etapa

                else:
                    material = elemento.HasAssociations[0].RelatingMaterial
                    nome_do_material = ""

                    try:
                        if material.HasProperties[0].Name == "Covering_material":
                            nome_do_material = (
                                material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                                + " - "
                                + material.HasProperties[0].Properties[1].NominalValue.wrappedValue
                            )
                        elif material.HasProperties[0].Name == "Marble_material":
                            nome_do_material = (
                                material.HasProperties[0].Properties[0].NominalValue.wrappedValue
                                + " - "
                                + material.HasProperties[0].Properties[1].NominalValue.wrappedValue
                            )
                    except:
                        nome_do_material = "none"

                    dados_das_tags[nome_do_elemento] = {}
                    dados_das_tags[nome_do_elemento]["material"] = material.Name
                    dados_das_tags[nome_do_elemento]["nomeDoMaterial"] = nome_do_material
                    dados_das_tags[nome_do_elemento]["ambiente"] = nome_do_ambiente
                    dados_das_tags[nome_do_elemento]["etapa"] = nome_da_etapa

    json_das_tags = "../../web/src/components/tresD/tags/tags.json"
    with open(json_das_tags, "w") as f:
        json.dump(dados_das_tags, f, indent=2)
