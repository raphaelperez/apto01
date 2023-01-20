export default function Portas(props) {
  return (
    <div className="card" key={props.porta["id"]}>
      <div className="card-infos">
        <h3>{props.porta["tipo"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>quantidade</h4>
            <p>{props.porta["quantidade"]} unid.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
