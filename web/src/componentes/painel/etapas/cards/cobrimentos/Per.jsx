export default function Per(props) {
  return (
    <div className="card" key={props.per["id"]}>
      <img className="card-img" src={props.per["imgSource"]} alt="" />
      <a className="card-link" href={props.per["url"]} target="_blank">
        <img src="./icones/link.svg" alt="" />
      </a>
      <div className="card-infos">
        <h3>{props.per["nome"]}</h3>
        <p>{props.per["fabricante"] + " - " + props.per["especificacao"]}</p>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>quantidade</h4>
            <p>{props.per["area"]} m²</p>
          </div>
          <div className="card-infos-col">
            <h4>preço unitário</h4>
            <p>{props.per["precoUnitario"]} R$/m²</p>
          </div>
        </div>
      </div>
    </div>
  );
}
