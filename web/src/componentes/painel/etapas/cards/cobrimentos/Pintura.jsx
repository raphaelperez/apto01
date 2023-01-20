export default function Pintura(props) {
  return (
    <div className="card" key={props.pintura["id"]}>
      <img className="card-img" src={props.pintura["imgSource"]} alt="" />
      <a className="card-link" href={props.pintura["url"]} target="_blank">
        <img src="./icones/link.svg" alt="" />
      </a>
      <div className="card-infos">
        <h3>{props.pintura["nome"]}</h3>
        <p>{props.pintura["fabricante"] + " - " + props.pintura["especificacao"]}</p>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>quantidade</h4>
            <p>{props.pintura["area"]} m²</p>
          </div>
          <div className="card-infos-col">
            <h4>preço unitário</h4>
            <p>{props.pintura["precoUnitario"]} R$/m²</p>
          </div>
        </div>
      </div>
    </div>
  );
}
