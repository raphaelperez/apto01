import { useEffect, useState } from "react";

import Toggle from "./Toogle";
import Levantamentos from "./etapas/Levantamentos.jsx";
import DemolicoesInfra from "./etapas/DemolicoesInfra.jsx";
import Cobrimentos from "./etapas/Cobrimentos.jsx";
import Marmoraria from "./etapas/Marmoraria.jsx";
import Marcenaria from "./etapas/Marcenaria.jsx";

import "./painel.css";
import "./etapas/cards/acordeon.css";
import "./etapas/cards/cards.css";

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
          {props.etapa == "demolicoeseinfra" && <DemolicoesInfra ambiente={props.ambiente} />}
          {props.etapa == "cobrimentos" && <Cobrimentos ambiente={props.ambiente} />}
          {props.etapa == "marmoraria" && <Marmoraria ambiente={props.ambiente} />}
          {props.etapa == "marcenaria" && <Marcenaria ambiente={props.ambiente} />}
        </div>
      </dir>
    </div>
  );
}
