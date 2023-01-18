import dados from "./menuPrincipal.json";

import "../menu.css";
import classes from "./MenuPrincipal.module.css";

export default function MenuPrincipal(props) {
  const setEtapaHandler = (btn) => {
    props.setEtapa(btn.target.value);
    props.setTag({ name: "none", position: [0, 0, 0] });
    if (props.exibir != "2D" || props.exibir != "2D") {
      props.setExibir("3D");
    }
  };

  const setAmbienteHandler = (btn) => {
    props.setAmbiente(btn.target.value);
    props.setPosicaoDoMenu("posicao_dois");
    props.setTag({ name: "none", position: [0, 0, 0] });
    if (props.exibir != "2D" || props.exibir != "2D") {
      props.setExibir("3D");
    }
  };

  const setResumoHandler = (btn) => {
    props.setExibir("gantt");
  };

  return (
    <div className={`menus ${classes[props.posicaoDoMenu]}`}>
      <h2>Etapas</h2>
      <ul>
        {dados["etapas"].map((etapa) => {
          return (
            <li className="list-item" key={etapa["id"]}>
              <button
                className={`menu-btn ${
                  etapa["nomeCurto"] == props.etapa && (props.exibir == "2D" || props.exibir == "3D") ? "ativo" : ""
                }`}
                value={etapa["nomeCurto"]}
                onClick={setEtapaHandler}
              >
                {etapa["nome"]}
              </button>
            </li>
          );
        })}
      </ul>
      <h2>Ambientes</h2>
      <ul>
        {dados["ambientes"].map((ambiente) => {
          return (
            <li className="list-item" key={ambiente["id"]}>
              <button className={"menu-btn"} value={ambiente["nomeCurto"]} onClick={setAmbienteHandler}>
                {ambiente["nome"]}
              </button>
            </li>
          );
        })}
      </ul>
      <h2>Resumo</h2>
      <ul>
        <li className="list-item">
          <button
            className={`menu-btn ${props.exibir == "gantt" ? "ativo" : ""}`}
            value={"gantt"}
            onClick={setResumoHandler}
          >
            Cronograma (Gantt)
          </button>
        </li>
      </ul>
    </div>
  );
}
