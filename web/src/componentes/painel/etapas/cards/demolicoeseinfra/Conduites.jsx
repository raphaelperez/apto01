export default function Conduites(props) {
  return (
    <div className="card" key={props.conduites["id"]}>
      <div className="card-infos">
        <h3>{props.conduites["tipo"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>quantidade</h4>
            <p>{props.conduites["comprimento"]} m</p>
          </div>
        </div>
      </div>
    </div>
  );
}
