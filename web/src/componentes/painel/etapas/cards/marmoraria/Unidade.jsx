export default function Unidade(props) {
  return (
    <div className="card" key={props.unidade["id"]}>
      <img className="card-img" src={props.unidade["imgSource"]} alt="" />
      <a className="card-link" href={props.unidade["url"]} target="_blank">
        <img src="./icones/link.svg" alt="" />
      </a>
      <div className="card-infos">
        <h3>{props.unidade["nome"]}</h3>
        <p>{props.unidade["fabricante"] + " - " + props.unidade["especificacao"]}</p>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>descrição</h4>
            <p>{props.unidade["descricao"]}</p>
          </div>
          <div className="card-infos-col">
            <h4>Ref</h4>
            <p>{props.unidade["codigo"]}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
