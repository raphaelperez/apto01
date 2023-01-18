import { useState, useEffect } from "react";

import Contexto from "./components/contexto/Contexto.jsx";
import Controle from "./components/controle/Controle.jsx";
import Menu from "./components/menu/Menu.jsx";
import Painel from "./components/painel/Painel.jsx";
import TresD from "./components/tresD/TresD.jsx";
import DoisD from "./components/doisD/DoisD.jsx";
import Gantt from "./components/gantt/Gantt.jsx";

export default function App() {
  const [ambiente, setAmbiente] = useState("apartamento");
  const [etapa, setEtapa] = useState("cobrimentos");
  const [exibir, setExibir] = useState("3D");
  const [tag, setTag] = useState({ name: "none", position: [0, 0, 0] });

  useEffect(() => {
    document.documentElement.style.setProperty("--altura-da-janela", `${window.innerHeight}px`);
  });

  useEffect(() => {
    window.addEventListener("resize", () => {
      document.documentElement.style.setProperty("--altura-da-janela", `${window.innerHeight}px`);
    });
  });

  return (
    <>
      <Contexto ambiente={ambiente} etapa={etapa} exibir={exibir} />
      <Menu
        ambiente={ambiente}
        setAmbiente={setAmbiente}
        etapa={etapa}
        setEtapa={setEtapa}
        setTag={setTag}
        exibir={exibir}
        setExibir={setExibir}
      />
      {(exibir == "2D" || exibir == "3D") && <Painel ambiente={ambiente} etapa={etapa} />}
      {(exibir == "2D" || exibir == "3D") && (
        <Controle exibir={exibir} setExibir={setExibir} ambiente={ambiente} etapa={etapa} setEtapa={setEtapa} />
      )}
      {exibir == "3D" && <TresD ambiente={ambiente} etapa={etapa} tag={tag} setTag={setTag} />}
      {exibir == "2D" && <DoisD ambiente={ambiente} etapa={etapa} />}
      {exibir == "gantt" && <Gantt />}
    </>
  );
}
