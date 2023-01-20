export default function Per(props) {
  return (
    <div className="card" key={props.per["id"]}>
      <div className="card-infos">
        <h3>{props.per["tipo"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>área</h4>
            <p>{props.per["area"]} m²</p>
          </div>
        </div>
      </div>
    </div>
  );
}
