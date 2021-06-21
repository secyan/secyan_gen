import { Affix, Button, notification, Row, Typography } from "antd";
import Modal from "antd/lib/modal/Modal";
import React from "react";
import { useLocation } from "react-router-dom";
import { TableConfigContext } from "../../model/TableContext";
import InputRowTableConfigCard from "./InputRowTableConfigCard";
import TableConfigCard from "./TableConfigCard";
import qs from "query-string";

export default function TableConfigPage() {
  const { configs, setConfigs } = React.useContext(TableConfigContext);
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);
  const location = useLocation();

  let q = qs.parse(location.search);

  React.useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 50);
  }, []);

  React.useEffect(() => {
    const table = q.table;
    if (table) {
      let element = document.getElementById(table as string);
      element?.scrollIntoView();
    }
  }, [location.search, loading]);

  
  return (
    <div style={{ overflowY: "scroll", height: "100%" }}>
      <InputRowTableConfigCard />
      {!loading &&
        configs.map((c, i) => (
          <TableConfigCard key={`config-${i}`} config={c} index={i} />
        ))}
    </div>
  );
}
