import { Button, PageHeader, Select, Form, Input } from "antd";
import Modal from "antd/lib/modal/Modal";
import React from "react";
import { CodeContext } from "../../../model/CodeContext";

const { Option } = Select;

export default function Header() {
  const [show, setShow] = React.useState(false);
  const [form] = Form.useForm();
  const { setBackend, backend } = React.useContext(CodeContext);

  const onSettingsClick = () => {
    let port = localStorage.getItem("port");
    let host = localStorage.getItem("host");
    let username = localStorage.getItem("username");
    let password = localStorage.getItem("password");
    let database = localStorage.getItem("database");

    let value = {
      port: port,
      host: host,
      username: username,
      password: password,
      database: database,
    };

    form.setFieldsValue(value);
    setShow(true);
  };

  const onSubmit = async (v: any) => {
    localStorage.setItem("port", v.port);
    localStorage.setItem("host", v.host);
    localStorage.setItem("username", v.username);
    localStorage.setItem("password", v.password);
    localStorage.setItem("database", v.database);
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
          // <Button type="primary" onClick={onSettingsClick}>
          //   Settings
          // </Button>,
        ];

  return (
    <div>
      <PageHeader title="CodeGen" extra={extra} />

      <Modal
        visible={show}
        title="Database settings"
        onCancel={() => setShow(false)}
        onOk={() => {
          form.submit();
        }}
      >
        <Form name="db settings" form={form} onFinish={onSubmit}>
          <Form.Item label="Host" name="host">
            <Input />
          </Form.Item>
          <Form.Item label="Port" name="port">
            <Input type="number" />
          </Form.Item>
          <Form.Item label="Username" name="username">
            <Input />
          </Form.Item>
          <Form.Item label="Password" name="password">
            <Input.Password />
          </Form.Item>
          <Form.Item label="Database" name="database">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
