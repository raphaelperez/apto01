import Acordeon from "./cards/Acordeon";
import Mdf from "./cards/marcenaria/Mdf";
import Unidade from "./cards/marcenaria/Unidade";

import dados from "./marcenaria.json";

export default function Marmoraria(props) {
  return (
    <>
      {dados[props.ambiente]["itens"].map((dado) => {
        return (
          <Acordeon item={dado["item"]}>
            {dado["mdfs"].map((mdf) => {
              return <Mdf placa={mdf} />;
            })}
            {dado["acessorios"].map((acessorio) => {
              return <Unidade unidade={acessorio} />;
            })}
          </Acordeon>
        );
      })}
    </>
  );
}
