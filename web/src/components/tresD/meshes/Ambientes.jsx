import { Vector3 } from "three";
import { useEffect, useState } from "react";
import { useTexture, useGLTF } from "@react-three/drei";

import meshesAmbientesJson from "./meshesAmbientes.json";
import meshesPortasJson from "./meshesPortas.json";
import posicoesJson from "./posicoes.json";
import ultimaEtapaJson from "./ultimaEtapa.json";

export default function Ambientes(props) {
  const [ambiente, setAmbiente] = useState(props.ambiente);
  const [etapa, setEtapa] = useState(props.etapa);

  console.log(ultimaEtapaJson[ambiente][etapa]);

  useEffect(() => {
    setAmbiente(props.ambiente);
  }, [props.ambiente]);

  useEffect(() => {
    setEtapa(props.etapa);
  }, [props.etapa]);

  const gltf = useGLTF(`./gltf/apto01.glb`);

  const meshes = [];
  const meshesPortas = [];

  for (const child of gltf.scene.children) {
    for (const mesh of meshesAmbientesJson[ambiente][etapa]) {
      if (child.name == mesh) {
        meshes.push(child);
      }
    }
    for (const mesh of meshesPortasJson[ambiente][ultimaEtapaJson[ambiente][etapa]]) {
      if (child.name == mesh) {
        meshesPortas.push(child);
      }
    }
  }

  const texturaDaEtapa = ultimaEtapaJson[ambiente][etapa];
  const texture = useTexture(`./gltf/textures/${ambiente}-${texturaDaEtapa}0000.jpg`);
  texture.flipY = false;

  const texturePorta = useTexture(`./gltf/textures/${"portas"}-${texturaDaEtapa}0000.jpg`);
  texturePorta.flipY = false;

  let move = new Vector3(0.01, 0.01, 0.01);
  let pointPosition = new Vector3(0, 0, 0);

  const setTagHandler = (event) => {
    event.stopPropagation();
    move = move.multiply(event.face.normal);
    pointPosition = event.point.add(move);
    props.setTag({ name: event.object.name, position: pointPosition });
  };

  return (
    <group>
      {meshes.map((child) => {
        return (
          <mesh
            key={child.name}
            geometry={child.geometry}
            position={[
              child.position.x + posicoesJson["apartamento"][0],
              child.position.y + posicoesJson["apartamento"][1],
              child.position.z + posicoesJson["apartamento"][2],
            ]}
            name={child.name}
            onDoubleClick={setTagHandler}
          >
            <meshBasicMaterial map={texture} />
          </mesh>
        );
      })}
      {meshesPortas.map((child) => {
        return (
          <mesh
            key={child.name}
            geometry={child.geometry}
            position={[
              child.position.x + posicoesJson["apartamento"][0],
              child.position.y + posicoesJson["apartamento"][1],
              child.position.z + posicoesJson["apartamento"][2],
            ]}
            name={child.name}
            onDoubleClick={setTagHandler}
          >
            <meshBasicMaterial map={texturePorta} />
          </mesh>
        );
      })}
    </group>
  );
}
