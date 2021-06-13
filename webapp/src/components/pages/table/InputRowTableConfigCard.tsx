import React from "react";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
import { Button, PageHeader, Row, Typography, Modal } from "antd";
import { TableConfigContext } from "../../model/TableContext";
import { tableStructureSchema } from "../home/utils/table_structure_schema";

export default function InputRowTableConfigCard() {
  const { setOpenRawConfigDialog, openRawConfigDialog, configs, setConfigs } =
    React.useContext(TableConfigContext);

  const [value, setValue] = React.useState("");

  const onOpen = React.useCallback(() => {
    setValue(JSON.stringify(configs, null, 4));
    setOpenRawConfigDialog(true);
  }, [configs]);

  const onClose = React.useCallback(() => {
    setConfigs(JSON.parse(value));
    setOpenRawConfigDialog(false);
  }, [value]);

  const handleJSONEditorWillMount = React.useCallback(
    (monaco: Monaco) => {
      monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
        validate: true,
        enableSchemaRequest: true,
        schemas: [
          {
            uri: "https://raw.githubusercontent.com/sirily11/SECYAN-GEN/master/examples/table_config.json",
            fileMatch: ["*"],
            schema: tableStructureSchema,
          },
        ],
      });
    },
    [value]
  );

  return (
    <PageHeader
      title="Table Configuration"
      subTitle="Config your table's info here"
      extra={[
        <Button type="primary" onClick={onOpen}>
          Set Raw Data
        </Button>,
      ]}
    >
      <Typography style={{ maxWidth: "800px" }}>
        You can either use the raw Data Config Editor to modify your database
        table's infomation, or use the GUI below to modify your table. You can
        check this{" "}
        <Typography.Link
          target="_blank"
          href="https://github.com/sirily11/SECYAN-GEN/blob/master/examples/table_config.json"
        >
          Link
        </Typography.Link>{" "}
        for example table configuration.
      </Typography>
      <Modal
        title="Raw Data Configuration"
        visible={openRawConfigDialog}
        onOk={onClose}
        onCancel={onClose}
        footer={[<Button onClick={onClose}>Close</Button>]}
        width={window.innerWidth * 0.8}
      >
        <Editor
          height={500}
          language="json"
          options={{ minimap: { enabled: false } }}
          beforeMount={(e) => handleJSONEditorWillMount(e)}
          value={value}
          onChange={(e) => {
            setValue(e ?? "");
          }}
        />
      </Modal>
    </PageHeader>
  );
}
