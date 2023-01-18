import dados from "./demolicoes.json";

export default function Demolicoes(props) {
  return (
    <>
      {dados[props.ambiente]["itens"].map((dado) => {
        return (
          <div className="card">
            <div className="card-infos">
              <div className="card-infos-row">
                <div className="card-infos-col">
                  <h4>tipo</h4>
                  <p>{dado["tipo"]}</p>
                </div>
                <div className="card-infos-col">
                  <h4>área</h4>
                  <p>{dado["area"]} m²</p>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </>
  );
}
