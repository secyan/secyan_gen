import React from "react";
import { TableConfigContext } from "../../model/TableContext";
import InputRowTableConfigCard from "./InputRowTableConfigCard";
import TableConfigCard from "./TableConfigCard";

export default function TableConfigPage() {
  const { configs } = React.useContext(TableConfigContext);

  return (
    <div style={{ overflowY: "scroll", height: "100%" }}>
      <InputRowTableConfigCard />
      {configs.map((c, i) => (
        <TableConfigCard key={`config-${i}`} config={c} index={i}/>
      ))}
    </div>
  );
}
