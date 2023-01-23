import json
from unidecode import unidecode


def bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_project):
    dados_do_menu_principal = {}

    dados_do_menu_principal["projeto"] = ifc_project[0].LongName

    dados_do_menu_principal["etapas"] = []

    for i in range(len(ifc_etapas_por_id)):
        ifc_etapa = ifc_etapas_por_id[i + 1]["etapa"]
        nome_da_etapa = ifc_etapa.Name

        etapa_tem_objeto = False

        etapas_adicionadas = []
        for sub_i in range(len(ifc_etapas_por_id[i + 1]["sub_etapas"])):
            ifc_sub_etapa = ifc_etapas_por_id[i + 1]["sub_etapas"][sub_i + 1]

            etapa_tem_objeto = False
            try:
                if ifc_sub_etapa.OperatesOn[0]:
                    etapa_tem_objeto = True
            except:
                if ifc_sub_etapa.HasAssignments:
                    etapa_tem_objeto = True
            finally:
                if etapa_tem_objeto and nome_da_etapa not in etapas_adicionadas:
                    id = "MENU_PRINC-" + nome_da_etapa
                    nome_curto_da_etapa = unidecode(nome_da_etapa.lower().replace(" ", ""))
                    dados_do_menu_principal["etapas"].append({"id": id, "nomeCurto": nome_curto_da_etapa, "nome": nome_da_etapa})
                    etapas_adicionadas.append(nome_da_etapa)

    dados_do_menu_principal["ambientes"] = []

    for ifc_ambiente in ifc_ambientes:
        if ifc_ambiente.PredefinedType == "INTERNAL":
            id = "MENU_PRINC-" + ifc_ambiente.Name
            nome_da_etapa = ifc_ambiente.LongName
            nome_curto_da_etapa = unidecode(nome_da_etapa.lower().replace(" ", ""))
            dados_do_menu_principal["ambientes"].append({"id": id, "nomeCurto": nome_curto_da_etapa, "nome": nome_da_etapa})

    json_do_menu_principal = "../../web/src/componentes/menu/menus/menuPrincipal.json"
    with open(json_do_menu_principal, "w") as f:
        json.dump(dados_do_menu_principal, f, indent=2)
