import dados from "./controle.json";

import "./controle.css";

export default function Controle(props) {
  const setExibirDoisDHandler = () => {
    props.setExibir("2D");
  };

  const setExibirTresDHandler = () => {
    props.setExibir("3D");
  };

  const quantidadeDeEtapas = dados[props.ambiente].length;

  const indeceDaEtapa = dados[props.ambiente].indexOf(props.etapa);

  const avançarEtapa = () => {
    if (indeceDaEtapa + 1 < quantidadeDeEtapas) {
      props.setEtapa(dados[props.ambiente][indeceDaEtapa + 1]);
    }
  };

  const voltarEtapa = () => {
    if (indeceDaEtapa > 0) {
      props.setEtapa(dados[props.ambiente][indeceDaEtapa - 1]);
    }
  };

  return (
    <div className="controle-ancora">
      <div className="controle-grafico">
        <button
          className={`controle-btn esquerda ${props.exibir == "2D" ? "ativo" : ""}`}
          onClick={setExibirDoisDHandler}
        >
          2D
        </button>
        <button
          className={`controle-btn direita ${props.exibir == "3D" ? "ativo" : ""}`}
          onClick={setExibirTresDHandler}
        >
          3D
        </button>
      </div>
      <div className="controle-etapa">
        <button className="controle-btn esquerda" onClick={voltarEtapa}>
          <img src="./icones/para_tras.svg" alt="" />
        </button>
        <button className="controle-btn direita" onClick={avançarEtapa}>
          <img src="./icones/para_frente.svg" alt="" />
        </button>
      </div>
    </div>
  );
}
