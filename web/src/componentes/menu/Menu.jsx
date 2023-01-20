import { useEffect, useState } from "react";

import Toggle from "./Toggle";
import MenuPrincipal from "./menus/MenuPrincipal";
import MenuDoAmbiente from "./menus/menuDoAmbiente";

import "./menu.css";

export default function Menu(props) {
  const [menuFechado, setMenuFechado] = useState(false);
  const [posicaoDoMenu, setPosicaoDoMenu] = useState("posicao_um");

  useEffect(() => {
    if (window.innerWidth < 768) {
      setMenuFechado(true);
    }
  }, []);

  const setMenuFechadoHandler = () => {
    setMenuFechado(!menuFechado);
  };

  return (
    <div className="menu">
      <dir className={`menu-ancora ${menuFechado ? "fechado" : ""}`}>
        <Toggle menuFechado={menuFechado} setMenuFechadoHandler={setMenuFechadoHandler} />
        <div className="menu-quadro">
          <MenuPrincipal
            etapa={props.etapa}
            setEtapa={props.setEtapa}
            ambiente={props.ambiente}
            setAmbiente={props.setAmbiente}
            posicaoDoMenu={posicaoDoMenu}
            setPosicaoDoMenu={setPosicaoDoMenu}
            setTag={props.setTag}
            exibir={props.exibir}
            setExibir={props.setExibir}
          />
          <MenuDoAmbiente
            etapa={props.etapa}
            setEtapa={props.setEtapa}
            ambiente={props.ambiente}
            setAmbiente={props.setAmbiente}
            posicaoDoMenu={posicaoDoMenu}
            setPosicaoDoMenu={setPosicaoDoMenu}
            setTag={props.setTag}
          />
        </div>
      </dir>
    </div>
  );
}
