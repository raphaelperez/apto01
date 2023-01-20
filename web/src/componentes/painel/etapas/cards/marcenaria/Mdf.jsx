export default function Mdf(props) {
  return (
    <div className="card" key={props.placa["id"]}>
      <img className="card-img" src={props.placa["imgSource"]} alt="" />
      <a className="card-link" href={props.placa["url"]} target="_blank">
        <img src="./icones/link.svg" alt="" />
      </a>
      <div className="card-infos">
        <h3>{props.placa["nome"]}</h3>
        <p>{props.placa["fabricante"] + " - " + props.placa["especificacao"]}</p>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>espessura</h4>
            <p>{props.placa["espessura"]} mm</p>
          </div>
          <div className="card-infos-col">
            <h4>área</h4>
            <p>{props.placa["area"]} m²</p>
          </div>
        </div>
      </div>
    </div>
  );
}
