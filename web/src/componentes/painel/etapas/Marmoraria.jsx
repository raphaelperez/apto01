import Acordeon from "./cards/Acordeon";
import Placa from "./cards/marmoraria/Placa";
import Unidade from "./cards/marmoraria/Unidade";

import dados from "./marmoraria.json";

export default function Marmoraria(props) {
  return (
    <>
      {dados[props.ambiente]["itens"].map((dado) => {
        return (
          <Acordeon item={dado["item"]}>
            {dado["pedras"].map((pedra) => {
              return <Placa placa={pedra} />;
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
