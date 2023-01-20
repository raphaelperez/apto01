export default function Tubos(props) {
  return (
    <div className="card" key={props.tubos["id"]}>
      <div className="card-infos">
        <h3>{props.tubos["tipo"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>quantidade</h4>
            <p>{props.tubos["comprimento"]} m</p>
          </div>
        </div>
      </div>
    </div>
  );
}
