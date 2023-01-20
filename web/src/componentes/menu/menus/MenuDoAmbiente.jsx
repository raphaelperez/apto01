import dados from "./menuDoAmbiente.json";

import "../menu.css";
import classes from "./MenuDoAmbiente.module.css";

export default function MenuDoAmbiente(props) {
  const voltar = () => {
    props.setPosicaoDoMenu("posicao_um");
    setTimeout(() => {
      props.setAmbiente("apartamento");
      props.setTag({ name: "none", position: [0, 0, 0] });
    }, "400");
  };

  const setEtapaHandler = (btn) => {
    props.setEtapa(btn.target.value);
    props.setTag({ name: "none", position: [0, 0, 0] });
  };

  let etapaCorrente = "";
  for (const etapa of dados[props.ambiente]["etapas"]) {
    etapaCorrente = etapa["nomeCurto"];
    if (etapa["nomeCurto"] == props.etapa) {
      etapaCorrente = props.etapa;
      break;
    }
  }

  return (
    <div className={`menus ${classes[props.posicaoDoMenu]}`}>
      <button className="voltar" onClick={voltar}>
        <img src="./icones/voltar.svg" alt="" />
      </button>
      <h2>{dados[props.ambiente]["nome"]}</h2>
      <h3>Etapas</h3>
      <ul>
        {dados[props.ambiente]["etapas"].map((etapa) => {
          return (
            <li className="list-item" key={etapa["id"]}>
              <button
                className={`menu-btn ${etapa["nomeCurto"] == etapaCorrente ? "ativo" : ""}`}
                value={etapa["nomeCurto"]}
                onClick={setEtapaHandler}
              >
                {etapa["nome"]}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
