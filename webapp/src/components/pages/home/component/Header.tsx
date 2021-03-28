import Editor from "@monaco-editor/react";
import { Button, PageHeader, Select, Form, Input } from "antd";
import Checkbox from "antd/lib/checkbox/Checkbox";
import Modal from "antd/lib/modal/Modal";
import React from "react";
import { CodeContext } from "../../../model/CodeContext";

const { Option } = Select;

export default function Header() {
  const [show, setShow] = React.useState(false);
  const [code, setCode] = React.useState("");
  const [createDB, setCreateDB] = React.useState(false);
  const [dbName, setDBName] = React.useState("");
  const [form] = Form.useForm();
  const { setBackend, backend, setDatabase } = React.useContext(CodeContext);

  const onSettingsClick = () => {
    setCode(localStorage.getItem("createScript") ?? "");
    setCreateDB(localStorage.getItem("createDB") === "true" ? true : false);
    setDBName(localStorage.getItem("dbName") ?? "");
    setShow(true);
  };

  const onSubmit = () => {
    localStorage.setItem("createScript", code);
    localStorage.setItem("createDB", createDB === true ? "true" : "false");
    localStorage.setItem("dbName", dbName);
    if (!createDB) {
      setDatabase(dbName);
    } else {
      setDatabase(undefined);
    }
    setShow(false);
  };

  const select = (
    <Select
      value={backend}
      style={{ width: 200 }}
      onChange={(v) => setBackend(v)}
    >
      <Option value={"python"}>Use Default Backend</Option>
      <Option value={"db"}>Use Query Plan</Option>
    </Select>
  );
  const extra =
    backend == "python"
      ? [select]
      : [
          select,
          <Button type="primary" onClick={onSettingsClick}>
            Settings
          </Button>,
        ];

  return (
    <div>
      <PageHeader title="CodeGen" extra={extra} />

      <Modal
        visible={show}
        title="Database settings"
        onCancel={() => setShow(false)}
        onOk={() => {
          onSubmit();
        }}
      >
        {createDB && (
          <div style={{ height: 500 }}>
            <Editor
              value={code}
              options={{ minimap: { enabled: false } }}
              onChange={(v) => setCode(v ?? "")}
              language="sql"
            />
          </div>
        )}
        <Checkbox
          value={createDB}
          onChange={(v) => {
            setCreateDB(v.target.checked);
          }}
        >
          Create database
        </Checkbox>
        {createDB}
        {!createDB && (
          <Input
            placeholder="Database Name"
            value={dbName}
            onChange={(e) => setDBName(e.target.value)}
          />
        )}
      </Modal>
    </div>
  );
}
