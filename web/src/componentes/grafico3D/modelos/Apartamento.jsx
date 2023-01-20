import { Vector3 } from "three";
import { useEffect, useState } from "react";
import { useTexture, useGLTF } from "@react-three/drei";

import modelosJson from "./modelos.json";

export default function Apartamento(props) {
  const [etapa, setEtapa] = useState(props.etapa);

  useEffect(() => {
    setEtapa(props.etapa);
  }, [props.etapa]);

  const gltf = useGLTF(`./gltf/apto01.glb`);

  const meshes = [];
  const meshesPortas = [];
  for (const child of gltf.scene.children) {
    for (const ambienteObj in modelosJson) {
      if (ambienteObj != "apartamento") {
        for (const objeto of modelosJson[ambienteObj][etapa]["objetos"]) {
          if (child.name == objeto) {
            const item = [];
            item.push(child);
            item.push(ambienteObj);
            meshes.push(item);
          }
        }
      }
    }
    for (const porta of modelosJson["apartamento"][etapa]["portas"]) {
      if (child.name == porta) {
        meshesPortas.push(child);
      }
    }
  }

  const textures = {};
  for (const ambiente in modelosJson) {
    if (ambiente != "apartamento") {
      const texture = useTexture(`./gltf/textures/${modelosJson[ambiente][etapa]["texturaObjetos"]}0000.jpg`);
      texture.flipY = false;
      textures[ambiente] = texture;
    }
  }

  const texturePortas = useTexture(`./gltf/textures/${"portas"}-${etapa}0000.jpg`);
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
      {meshes.map((mesh) => {
        return (
          <mesh
            key={mesh[0].name}
            geometry={mesh[0].geometry}
            position={[
              mesh[0].position.x + props.posicao[0],
              mesh[0].position.y + props.posicao[1],
              mesh[0].position.z + props.posicao[2],
            ]}
            name={mesh[0].name}
            onDoubleClick={setTagHandler}
          >
            <meshBasicMaterial map={textures[mesh[1]]} />
          </mesh>
        );
      })}
      {meshesPortas.map((child) => {
        return (
          <mesh
            key={child.name}
            geometry={child.geometry}
            position={[
              child.position.x + props.posicao[0],
              child.position.y + props.posicao[1],
              child.position.z + props.posicao[2],
            ]}
            name={child.name}
            onDoubleClick={setTagHandler}
          >
            <meshBasicMaterial map={texturePortas} />
          </mesh>
        );
      })}
    </group>
  );
}
