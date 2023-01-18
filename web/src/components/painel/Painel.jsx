import { useEffect, useState } from "react";

import Toggle from "./Toogle";
import Levantamentos from "./contextos/Levantamentos.jsx";
import Demolicoes from "./contextos/Demolicoes.jsx";
import Cobrimentos from "./contextos/Cobrimentos.jsx";
import Marmoraria from "./contextos/Marmoraria.jsx";
import Marcenaria from "./contextos/Marcenaria.jsx";

import "./painel.css";
import "./contextos/cards/acordeon.css";
import "./contextos/cards/cards.css";

export default function Painel(props) {
  const [painelFechado, setPainelFechado] = useState(false);

  useEffect(() => {
    if (window.innerWidth < 768) {
      setPainelFechado(true);
    }
  }, []);

  const setPainelFechadoHandler = () => {
    setPainelFechado(!painelFechado);
  };

  return (
    <div className="painel">
      <dir className={`painel-ancora ${painelFechado ? "fechado" : ""}`}>
        <Toggle painelFechado={painelFechado} setPainelFechadoHandler={setPainelFechadoHandler} />
        <div className="painel-quadro">
          {props.etapa == "levantamentos" && <Levantamentos ambiente={props.ambiente} />}
          {props.etapa == "demolicoes" && <Demolicoes ambiente={props.ambiente} />}
          {props.etapa == "cobrimentos" && <Cobrimentos ambiente={props.ambiente} />}
          {props.etapa == "marmoraria" && <Marmoraria ambiente={props.ambiente} />}
          {props.etapa == "marcenaria" && <Marcenaria ambiente={props.ambiente} />}
        </div>
      </dir>
    </div>
  );
}
