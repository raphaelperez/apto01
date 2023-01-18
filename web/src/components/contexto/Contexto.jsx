import "./contexto.css";

import dados from "./contexto.json";

export default function Contexto(props) {
  return (
    <div className="contexto">
      <h1>{dados["projeto"]}</h1>
      <h2>
        {props.exibir == "2D" || props.exibir == "3D"
          ? props.ambiente == "apartamento"
            ? " / " + dados[props.etapa]
            : " / " + dados[props.ambiente] + " / " + dados[props.etapa]
          : props.ambiente == "apartamento"
          ? "/ Cronograma (Gannt)"
          : ""}
      </h2>
    </div>
  );
}
