import ifcopenshell

from package import helpers

from package import contexto
from package import menu_principal
from package import menu_do_ambiente
from package import meshes
from package import tags
from package import controle

from package.contextos import demolicoes_e_infra
from package.contextos import cobrimentos
from package.contextos import marmoraria
from package.contextos import marcenaria


ifc = ifcopenshell.open("../apto01.ifc")
ifc_projeto = ifc.by_type("ifcProject")
ifc_apartamento = ifc.by_type("ifcBuildingStorey")
ifc_ambientes = ifc.by_type("ifcSpace")
ifc_etapas = ifc.by_type("ifcTask")

ifc_etapas_por_id = helpers.gera_ifc_etapas_por_id(ifc_etapas)
etapas_por_ambiente = helpers.gera_etapas_por_ambiente(ifc_ambientes, ifc_etapas_por_id)

contexto.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
menu_principal.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
menu_do_ambiente.bake_json(ifc_etapas_por_id, ifc_ambientes, etapas_por_ambiente)
# tags.bake_json(ifc_ambientes)
controle.bake_json(etapas_por_ambiente)

meshes.bake_json(ifc_ambientes, ifc_etapas_por_id, etapas_por_ambiente, ifc_apartamento)

demolicoes_e_infra.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
cobrimentos.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
marmoraria.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
marcenaria.bake_json(ifc_ambientes, ifc_etapas_por_id, ifc_projeto)
