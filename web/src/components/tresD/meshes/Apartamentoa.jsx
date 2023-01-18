import { Vector3 } from "three";
import { useEffect, useState } from "react";
import { useTexture, useGLTF } from "@react-three/drei";

import meshesAmbientesJson from "./meshesAmbientes.json";
import meshesPortasJson from "./meshesPortas.json";
import posicoesJson from "./posicoes.json";
import ultimaEtapaJson from "./ultimaEtapa.json";

export default function Apartamento(props) {
  const [etapa, setEtapa] = useState(props.etapa);

  useEffect(() => {
    setEtapa(props.etapa);
  }, [props.etapa]);

  const gltf = useGLTF(`./gltf/project.glb`);

  const meshes = [];
  const meshesPortas = [];
  for (const child of gltf.scene.children) {
    for (const ambienteJson in meshesAmbientesJson) {
      for (const mesh of meshesAmbientesJson[ambienteJson][etapa]) {
        if (child.name == mesh) {
          const item = [];
          item.push(child);
          item.push(ambienteJson);
          meshes.push(item);
        }
      }
    }
    for (const mesh of meshesPortasJson["apartamento"][etapa]) {
      if (child.name == mesh) {
        meshesPortas.push(child);
      }
    }
  }

  const textures = {};
  const texturesPortas = {};
  for (const ambiente in ultimaEtapaJson) {
    const texturaDaEtapa = ultimaEtapaJson[ambiente][etapa];
    const texture = useTexture(`./gltf/textures/${ambiente}-${texturaDaEtapa}.jpg`);
    texture.flipY = false;
    textures[ambiente] = texture;
  }

  const texturePortas = useTexture(`./gltf/textures/${"portas"}-${etapa}.jpg`);
  texturePortas.flipY = false;

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
            <meshBasicMaterial map={texturePortas} />
          </mesh>
        );
      })}
      {meshes.map((mesh) => {
        return (
          <mesh
            key={mesh[0].name}
            geometry={mesh[0].geometry}
            position={[
              mesh[0].position.x + posicoesJson["apartamento"][0],
              mesh[0].position.y + posicoesJson["apartamento"][1],
              mesh[0].position.z + posicoesJson["apartamento"][2],
            ]}
            name={mesh[0].name}
            onDoubleClick={setTagHandler}
          >
            <meshBasicMaterial map={texturesPortas[mesh[1]]} />
          </mesh>
        );
      })}
    </group>
  );
}
