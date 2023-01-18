export default function Forro(props) {
  return (
    <div className="card" key={props.forro["id"]}>
      <img className="card-img" src={props.forro["imgSource"]} alt="" />
      <a className="card-link" href={props.forro["url"]} target="_blank">
        <img src="./icones/link.svg" alt="" />
      </a>
      <div className="card-infos">
        <h3>{props.forro["nome"]}</h3>
        <p>{props.forro["tipo"]}</p>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>área</h4>
            <p>{props.forro["area"]} m²</p>
          </div>
          <div className="card-infos-col"></div>
        </div>
      </div>
    </div>
  );
}
