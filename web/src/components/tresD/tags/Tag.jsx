import { Html } from "@react-three/drei";

import dados from "./tags.json";

export default function Tag(props) {
  return (
    props.tag["name"] != "none" && (
      <Html wrapperClass="info-tag" occlude={true} zIndexRange={[1, 0]} position={props.tag["position"]}>
        <h3>
          {dados[props.tag["name"]]["montagem"]
            ? dados[props.tag["name"]]["etapa"] +
              " / " +
              dados[props.tag["name"]]["montagem"] +
              " / " +
              dados[props.tag["name"]]["material"]
            : dados[props.tag["name"]]["etapa"] + " / " + dados[props.tag["name"]]["material"]}
        </h3>
        <p>{dados[props.tag["name"]]["nomeDoMaterial"] != "none" && dados[props.tag["name"]]["nomeDoMaterial"]}</p>
      </Html>
    )
  );
}
