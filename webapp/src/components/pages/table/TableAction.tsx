import { Button, Modal, notification, Tooltip, Typography } from "antd";
import React from "react";
import { TableConfigContext } from "../../model/TableContext";
import { PlusOutlined, ReloadOutlined } from "@ant-design/icons";

export default function TableAction() {
  const [open, setOpen] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const { configs, setConfigs, fetchConfigs } =
    React.useContext(TableConfigContext);

  const addTable = React.useCallback(() => {
    configs.push({
      table_name: "table",
      data_sizes: [],
      data_paths: [],
      columns: [],
      owner: "Server",
      annotations: [],
    });
    setConfigs(configs);
    setOpen(false);
    notification.success({
      message: "Added a new table",
      placement: "bottomRight",
    });
  }, [configs]);

  return (
    <div>
      <Tooltip title="Fetch Table Config from DB">
        <Button
          shape="round"
          loading={isLoading}
          style={{ marginRight: 20 }}
          onClick={async () => {
            setIsLoading(true);
            await fetchConfigs();
            setIsLoading(false);
          }}
        >
          <ReloadOutlined />
        </Button>
      </Tooltip>
      <Tooltip title="Create a new table">
        <Button
          shape="round"
          style={{ marginRight: 20 }}
          onClick={() => setOpen(true)}
        >
          <PlusOutlined />
        </Button>
      </Tooltip>
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
