import { useState } from "react";

import "./acordeon.css";

export default function Acordeon(props) {
  const [acordeonFechado, setAcordeonFechado] = useState(true);

  const setAcordeonFechadoHandler = () => {
    setAcordeonFechado(!acordeonFechado);
  };

  return (
    <div className="acordeon">
      <button className={`expandir-btn ${!acordeonFechado ? "fechado" : ""}`} onClick={setAcordeonFechadoHandler}>
        <h3>{props.item}</h3>
        <img className={`expandir-btn-img ${acordeonFechado ? "fechado" : ""}`} src="./icones/expandir.svg" alt="" />
      </button>

      <div className={`acordeon-corpo ${acordeonFechado ? "fechado" : ""}`}>{props.children}</div>
    </div>
  );
}
