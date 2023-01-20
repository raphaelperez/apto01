import { Vector3 } from "three";
import { useEffect, useState } from "react";
import { useTexture, useGLTF } from "@react-three/drei";

import modelosJson from "./modelos.json";

export default function Ambientes(props) {
  const [ambiente, setAmbiente] = useState(props.ambiente);
  const [etapa, setEtapa] = useState(props.etapa);

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
    for (const mesh of modelosJson[ambiente][etapa]["objetos"]) {
      if (child.name == mesh) {
        meshes.push(child);
      }
    }
    for (const mesh of modelosJson[ambiente][etapa]["portas"]) {
      if (child.name == mesh) {
        meshesPortas.push(child);
      }
    }
  }

  const texture = useTexture(`./gltf/textures/${modelosJson[ambiente][etapa]["texturaObjetos"]}0000.jpg`);
  texture.flipY = false;

  const texturePorta = useTexture(`./gltf/textures/${modelosJson[ambiente][etapa]["texturaPortas"]}0000.jpg`);
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
              child.position.x + props.posicao[0],
              child.position.y + props.posicao[1],
              child.position.z + props.posicao[2],
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
