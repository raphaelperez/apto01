import { Html } from "@react-three/drei";
import "./doisD.css";

export default function Desenho(props) {
  return (
    <Html center distanceFactor={1} zIndexRange={[1, 0]}>
      <img className="desenho" src={`./desenhos/${props.ambiente}-${props.etapa}.png`} alt="" />
      <img className="desenho" src={`./desenhos/${props.ambiente}-${props.etapa}.svg`} alt="" />
    </Html>
  );
}
