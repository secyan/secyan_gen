import { Button, Card, Input, Space, Form, Row, Col, Typography } from "antd";
import React from "react";
import { TableConfig } from "../../model/table-config";
import {
  EditOutlined,
  PlusOutlined,
  MinusCircleOutlined,
} from "@ant-design/icons";
import { TableConfigContext } from "../../model/TableContext";
import Modal from "antd/lib/modal/Modal";

interface Props {
  config: TableConfig;
  index: number;
}

interface FormValue {
  path_size: { size: number; path: string }[];
}

export default function TableConfigCard(props: Props) {
  const { config, index } = props;
  const [name, setName] = React.useState(config.table_name);
  const [open, setOpen] = React.useState(false);
  const { setConfigs, configs } = React.useContext(TableConfigContext);

  const formValues = {
    path_size: config.data_sizes.map((v, i) => {
      return { path: config.data_paths[i], size: v };
    }),
  };

  const updateTableName = React.useCallback(() => {
    configs[index].table_name = name;
    setConfigs(configs);
    setOpen(false);
  }, [name]);

  const updateConfig = React.useCallback(
    (value: FormValue) => {
      let path_size = value.path_size.filter((v) => v !== undefined);
      configs[index].data_sizes = path_size.map((v: any) => parseInt(v.size));
      configs[index].data_paths = path_size.map((v: any) => v.path);
      setConfigs(configs);
    },
    [config]
  );

  return (
    <Card
      title={config.table_name}
      style={{ margin: 10 }}
      extra={[
        <Button shape="circle" onClick={() => setOpen(true)}>
          <EditOutlined />
        </Button>,
      ]}
    >
      <Form
        name="data_paths"
        title="Data Sizes and"
        initialValues={formValues}
        onValuesChange={(_, v) => {
          updateConfig(v);
        }}
      >
        {/* data sizes and data paths */}

        <Typography.Title level={5}>Data Sizes and Paths</Typography.Title>
        <Form.List name="path_size">
          {(fields, { add, remove }) => (
            <Row gutter={[10, 10]}>
              {fields.map(({ key, name, fieldKey, ...restField }) => (
                <Col
                  key={key}
                  style={{ display: "flex", marginBottom: 8 }}
                  xs={24}
                  md={12}
                >
                  <Row style={{ width: "100%" }} gutter={[20, 10]}>
                    <Col md={10} xs={24}>
                      <Form.Item
                        {...restField}
                        name={[name, "size"]}
                        rules={[
                          { required: true, message: "Data Size is required" },
                        ]}
                      >
                        <Input placeholder="Data size" type="number" />
                      </Form.Item>
                    </Col>
                    <Col md={12} xs={22}>
                      <Form.Item
                        {...restField}
                        name={[name, "path"]}
                        rules={[
                          { required: true, message: "Data Path is required" },
                        ]}
                      >
                        <Input placeholder="Data path" />
                      </Form.Item>
                    </Col>
                    <Col span={2}>
                      <MinusCircleOutlined
                        className="dynamic-delete-button"
                        onClick={() => remove(name)}
                      />
                    </Col>
                  </Row>
                </Col>
              ))}
              <Col xs={24}>
                <Form.Item>
                  <Button
                    type="dashed"
                    onClick={() => add()}
                    block
                    icon={<PlusOutlined />}
                  >
                    Add field
                  </Button>
                </Form.Item>
              </Col>
            </Row>
          )}
        </Form.List>

        {/* end data sizes and data paths */}
        {/* columns */}
        <Typography.Title level={5}>Table Columns</Typography.Title>

        {/* end columns */}
      </Form>
      <Modal
        visible={open}
        title="Table name"
        onCancel={() => {
          setName(config.table_name);
          setOpen(false);
        }}
        onOk={updateTableName}
      >
        <Input
          placeholder="Table name"
          value={name}
          onChange={(e) => {
            setName(e.target.value);
          }}
        />
      </Modal>
    </Card>
  );
}
