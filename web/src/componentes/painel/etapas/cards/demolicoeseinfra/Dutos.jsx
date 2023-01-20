export default function Dutos(props) {
  return (
    <div className="card" key={props.dutos["id"]}>
      <div className="card-infos">
        <h3>{props.dutos["tipo"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>comprimento</h4>
            <p>{props.dutos["comprimento"]} m</p>
          </div>
        </div>
      </div>
    </div>
  );
}
