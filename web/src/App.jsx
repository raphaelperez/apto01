import { useState, useEffect } from "react";

import Contexto from "./componentes/contexto/Contexto.jsx";
import Controle from "./componentes/controle/Controle.jsx";
import Menu from "./componentes/menu/Menu.jsx";
import Painel from "./componentes/painel/Painel.jsx";
import Grafico3D from "./componentes/grafico3D/Grafico3D.jsx";
import Grafico2D from "./componentes/grafico2D/Grafico2D.jsx";
import Gantt from "./componentes/gantt/Gantt.jsx";

export default function App() {
  const [ambiente, setAmbiente] = useState("apartamento");
  const [etapa, setEtapa] = useState("marcenaria");
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
      {exibir == "3D" && <Grafico3D ambiente={ambiente} etapa={etapa} tag={tag} setTag={setTag} />}
      {exibir == "2D" && <Grafico2D ambiente={ambiente} etapa={etapa} />}
      {exibir == "gantt" && <Gantt />}
    </>
  );
}
