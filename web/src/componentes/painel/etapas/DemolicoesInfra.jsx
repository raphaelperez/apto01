import Acordeon from "./cards/Acordeon";
import Per from "./cards/demolicoeseinfra/Per";
import Portas from "./cards/demolicoeseinfra/Portas";
import Conduites from "./cards/demolicoeseinfra/Conduites";
import Tubos from "./cards/demolicoeseinfra/Tubos";
import Dutos from "./cards/demolicoeseinfra/Dutos";

import dados from "./demolicoesInfra.json";

export default function DemolicoesInfra(props) {
  return (
    <>
      {dados[props.ambiente]["itens"].map((dado) => {
        return (
          <Acordeon item={dado["item"]}>
            {dado["item"] == "Demolições" &&
              dado["per"]["area"] != "0" &&
              dado["per"].map((per) => {
                return <Per per={per} />;
              })}
            {dado["item"] == "Demolições" &&
              dado["portas"].map((porta) => {
                return <Portas porta={porta} />;
              })}
            {dado["item"] == "Infra Elétrica" &&
              dado["conduites"].map((conduites) => {
                return <Conduites conduites={conduites} />;
              })}
            {dado["item"] == "Infra Gás" &&
              dado["tubos"].map((tubos) => {
                return <Tubos tubos={tubos} />;
              })}
            {dado["item"] == "Infra Exaustão" &&
              dado["dutos"].map((dutos) => {
                return <Dutos dutos={dutos} />;
              })}
          </Acordeon>
        );
      })}
    </>
  );
}
