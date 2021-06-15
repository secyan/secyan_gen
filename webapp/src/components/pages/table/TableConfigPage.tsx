import { Affix, Button, notification, Row, Typography } from "antd";
import Modal from "antd/lib/modal/Modal";
import React from "react";
import { TableConfigContext } from "../../model/TableContext";
import InputRowTableConfigCard from "./InputRowTableConfigCard";
import TableConfigCard from "./TableConfigCard";

export default function TableConfigPage() {
  const { configs, setConfigs } = React.useContext(TableConfigContext);
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 50);
  }, []);

  const addTable = React.useCallback(() => {
    configs.push({
      table_name: "table",
      data_sizes: [],
      data_paths: [],
      columns: [],
      owner: "Server",
    });
    setConfigs(configs);
    setOpen(false);
    notification.success({
      message: "Added a new table",
      placement: "bottomRight",
    });
  }, [configs]);

  return (
    <div style={{ overflowY: "scroll", height: "100%" }}>
      <InputRowTableConfigCard />
      {!loading &&
        configs.map((c, i) => (
          <TableConfigCard key={`config-${i}`} config={c} index={i} />
        ))}

      <Affix offsetBottom={20} style={{ position: "fixed", right: 10 }}>
        <Row justify="end">
          <Button
            type="primary"
            style={{ marginRight: 20 }}
            onClick={() => setOpen(true)}
          >
            Add Table
          </Button>
        </Row>
      </Affix>
      <Modal
        visible={open}
        title="Add New Table"
        onOk={addTable}
        onCancel={() => {
          setOpen(false);
        }}
      >
        <Typography>Create a empty table?</Typography>
      </Modal>
    </div>
  );
}
