import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

import Ambientes from "./meshes/Ambientes.jsx";
import Apartamento from "./meshes/Apartamento";
import Tag from "./tags/Tag";

import "./three.css";

export default function TresD(props) {
  return (
    <div className="canvas">
      <Canvas flat camera={{ position: [-3, 5, 6], fov: 70, near: 0.1, far: 200 }}>
        <OrbitControls enableDamping={true} />
        <Tag tag={props.tag} />
        {props.ambiente != "apartamento" && (
          <Ambientes ambiente={props.ambiente} etapa={props.etapa} setTag={props.setTag} />
        )}
        {props.ambiente == "apartamento" && <Apartamento etapa={props.etapa} setTag={props.setTag} />}
      </Canvas>
    </div>
  );
}
