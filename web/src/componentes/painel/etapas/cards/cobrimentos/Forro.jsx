export default function Forro(props) {
  return (
    <div className="card" key={props.forro["id"]}>
      <div className="card-infos">
        <h3>{props.forro["tipo"]}</h3>
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
