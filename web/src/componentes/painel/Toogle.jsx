import { useState, useEffect } from "react";
import "./painel.css";

export default function Toggle(props) {
  const [windowWidth, setWindowWidth] = useState(1080);

  useEffect(() => {
    setWindowWidth(window.innerWidth);
  });

  useEffect(() => {
    window.addEventListener("resize", () => {
      setWindowWidth(window.innerWidth);
    });
  });

  return (
    <div className="painel-toggle">
      <button
        className={`painel-toggle-btn ${props.painelFechado ? "fechado" : ""}`}
        onClick={props.setPainelFechadoHandler}
      >
        <img src={windowWidth > 768 ? "./icones/direita.svg" : "./icones/abaixo.svg"} alt="" />
      </button>
      <button
        className={`painel-toggle-btn ${!props.painelFechado ? "fechado" : ""}`}
        onClick={props.setPainelFechadoHandler}
      >
        <img src="./icones/cards.svg" alt="" />
      </button>
    </div>
  );
}
