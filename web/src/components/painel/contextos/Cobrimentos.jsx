import Acordeon from "./cards/Acordeon";
import Per from "./cards/cobrimentos/Per.jsx";
import Pintura from "./cards/cobrimentos/Pintura.jsx";
import Forro from "./cards/cobrimentos/Forro.jsx";

import dados from "./cobrimentos.json";

export default function Cobrimentos(props) {
  return (
    <>
      {dados[props.ambiente]["itens"].map((dado) => {
        return (
          <Acordeon item={dado["item"]}>
            {dado["item"] == "Forros" &&
              dado["forros"].map((forro) => {
                return <Forro forro={forro} />;
              })}
            {dado["item"] == "Pinturas" &&
              dado["pinturas"].map((pintura) => {
                return <Pintura pintura={pintura} />;
              })}
            {dado["item"] == "Pisos e Revestimentos" &&
              dado["pers"].map((per) => {
                return <Per per={per} />;
              })}
          </Acordeon>
        );
      })}
    </>
  );
}
