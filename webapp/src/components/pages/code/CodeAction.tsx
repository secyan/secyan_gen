import { Button, Form, Input, Row, Tooltip } from "antd";
import React from "react";
import { EditOutlined, CaretRightOutlined } from "@ant-design/icons";
import { CodeContext } from "../../model/CodeContext";
import { TableConfigContext } from "../../model/TableContext";
import Modal from "antd/lib/modal/Modal";

export default function CodeAction() {
  const {
    setCodeRunResults,
    codeRunResults,
    runCode,
    isLoading,
    index,
    setShowEdit,
    showEdit,
  } = React.useContext(CodeContext);
  const { configs } = React.useContext(TableConfigContext);
  const [form] = Form.useForm();

  // Rename, etc
  const reConfigure = React.useCallback(() => {
    let values = form.getFieldsValue();
    codeRunResults[index].annotation_name = values.annotation_name;
    codeRunResults[index].name = values.name;
    codeRunResults[index].num_of_rows = parseInt(values.num_of_rows);
    setCodeRunResults(codeRunResults);
    setShowEdit(false);
  }, [codeRunResults, index]);

  React.useEffect(() => {
    form.setFieldsValue(codeRunResults[index]);
  }, [showEdit]);

  return (
    <Row justify="end" style={{ marginRight: 20 }}>
      <Tooltip title="Run Code">
        <Button
          shape="round"
          size="large"
          style={{ marginRight: 10 }}
          loading={isLoading}
          onClick={async () => {
            await runCode(index, configs);
          }}
        >
          <CaretRightOutlined />
        </Button>
      </Tooltip>
      <Tooltip title="Rename">
        <Button
          shape="round"
          size="large"
          style={{ marginRight: 10 }}
          onClick={() => {
            setShowEdit(true);
          }}
        >
          <EditOutlined />
        </Button>
      </Tooltip>
      <Modal
        title="Configuration"
        visible={showEdit}
        onOk={reConfigure}
        onCancel={() => {
          form.resetFields();
          setShowEdit(false);
        }}
      >
        <Form initialValues={codeRunResults[index]} form={form}>
          <Form.Item name="name" label="Name">
            <Input placeholder="Name" />
          </Form.Item>
          <Form.Item name="num_of_rows" label="Number of rows">
            <Input placeholder="Num of rows" type="number" />
          </Form.Item>
          <Form.Item name="annotation_name" label="Annotation Name">
            <Input placeholder="Annotation Name" />
          </Form.Item>
        </Form>
      </Modal>
    </Row>
  );
}
