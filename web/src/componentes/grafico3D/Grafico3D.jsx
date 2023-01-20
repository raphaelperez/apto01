import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

import Ambientes from "./modelos/Ambientes.jsx";
import Apartamento from "./modelos/Apartamento.jsx";
import Tag from "./tags/Tag";

import "./grafico3D.css";

export default function Grafico3D(props) {
  const posicao = [-6.5, -1, 1.35];
  return (
    <div className="canvas">
      <Canvas flat camera={{ position: [-3, 5, 6], fov: 70, near: 0.1, far: 200 }}>
        <OrbitControls enableDamping={true} />
        <Tag tag={props.tag} />
        {props.ambiente != "apartamento" && (
          <Ambientes ambiente={props.ambiente} etapa={props.etapa} setTag={props.setTag} posicao={posicao} />
        )}
        {props.ambiente == "apartamento" && <Apartamento etapa={props.etapa} setTag={props.setTag} posicao={posicao} />}
      </Canvas>
    </div>
  );
}
