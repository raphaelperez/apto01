export default function Tabica(props) {
  return (
    <div className="card" key={props.tabica["id"]}>
      <div className="card-infos">
        <h3>{props.tabica["conjunto"]}</h3>
        <div className="card-infos-row">
          <div className="card-infos-col">
            <h4>área</h4>
            <p>{props.tabica["comprimento"]} m</p>
          </div>
          <div className="card-infos-col"></div>
        </div>
      </div>
    </div>
  );
}
