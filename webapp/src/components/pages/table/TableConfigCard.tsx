import {
  Button,
  Card,
  Input,
  Space,
  Form,
  Row,
  Col,
  Typography,
  Divider,
  Select,
  Modal,
  notification,
  List,
  Descriptions,
} from "antd";
import React from "react";
import { TableConfig } from "../../model/table-config";
import {
  EditOutlined,
  PlusOutlined,
  MinusCircleOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import { TableConfigContext } from "../../model/TableContext";
import { column_types, table_owner } from "../../../settings/column_types";
import AwesomeDebouncePromise from "awesome-debounce-promise";
import { Role } from "../../model/SettingsContext";

interface Props {
  config: TableConfig;
  index: number;
}

interface FormValue {
  path_size: { size: number; path: string }[];
  columns: any[];
  annotations: any[];
}

export default function TableConfigCard(props: Props) {
  const { config, index } = props;
  const [name, setName] = React.useState(config.table_name);
  const [owner, setOwner] = React.useState(config.owner);
  const [open, setOpen] = React.useState(false);
  const { setConfigs, configs } = React.useContext(TableConfigContext);

  const formValues = React.useCallback(() => {
    return config;
  }, [config]);

  // Will be used to rename the table
  const updateTableConfig = React.useCallback(() => {
    configs[index].table_name = name;
    configs[index].owner = owner;
    setConfigs(configs);
    setOpen(false);
  }, [name, owner]);

  // Will be used on each field's update
  const updateConfig = React.useCallback(
    (value: FormValue) => {
      console.log(value.annotations);
      let annotations = value.annotations
        .filter((v) => v !== undefined && v.annotation !== undefined)
        .map((a) => a.annotation);

      configs[index].columns = value.columns;
      configs[index].annotations = annotations !== undefined ? annotations : [];
      setConfigs(configs, false);
    },
    [config]
  );

  const deleteTable = React.useCallback(() => {
    Modal.confirm({
      title: "confirm",
      content: "Delete this table",
      onOk: () => {
        configs.splice(index, 1);
        setConfigs(JSON.parse(JSON.stringify(configs)));
        notification.success({
          message: "Table deleted",
          placement: "bottomRight",
        });
      },
    });
  }, [config]);

  return (
    <Card
      id={config.table_name}
      title={`${config.table_name} - ${config.owner ?? "Client"}`}
      key={config.table_name}
      style={{ margin: 10 }}
      extra={[
        <Button
          shape="circle"
          onClick={deleteTable}
          style={{ marginRight: 10 }}
        >
          <DeleteOutlined />
        </Button>,
        <Button shape="circle" onClick={() => setOpen(true)}>
          <EditOutlined />
        </Button>,
      ]}
    >
      <Descriptions title="Data size and path" bordered={true}>
        <Descriptions.Item label="Data Path">
          {config.data_paths}
        </Descriptions.Item>
        <Descriptions.Item label="Data Size">
          {config.data_sizes}
        </Descriptions.Item>
      </Descriptions>
      <Form
        style={{ marginTop: 20 }}
        initialValues={formValues()}
        onValuesChange={(_, v) => {
          updateConfig(v);
        }}
      >
        {/* columns */}
        <Typography.Title level={5}>Table Columns</Typography.Title>
        <Form.List name="columns">
          {(fields, { add, remove }) => (
            <Row gutter={[10, 10]}>
              {fields.map(({ key, name, fieldKey, ...restField }) => (
                <Col
                  key={`column-${key}`}
                  style={{ display: "flex", marginBottom: 8 }}
                  xs={24}
                >
                  <Row style={{ width: "100%" }} gutter={[20, 10]}>
                    <Col md={5} xs={24}>
                      <Form.Item
                        {...restField}
                        name={[name, "column_type"]}
                        fieldKey={[fieldKey, "type"]}
                        rules={[
                          {
                            required: true,
                            message: "Column type is required",
                          },
                        ]}
                      >
                        <Select>
                          {column_types.map((c, i) => (
                            <Select.Option value={c}>{c}</Select.Option>
                          ))}
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col md={5} xs={22}>
                      <Form.Item
                        {...restField}
                        name={[name, "name"]}
                        fieldKey={[fieldKey, "name"]}
                        rules={[
                          {
                            required: true,
                            message: "Column name is required",
                          },
                        ]}
                      >
                        <Input placeholder="Column Name" />
                      </Form.Item>
                    </Col>
                    <Col span={2}>
                      <MinusCircleOutlined onClick={() => remove(name)} />
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
                    Add Column
                  </Button>
                </Form.Item>
              </Col>
            </Row>
          )}
        </Form.List>
        {/* end columns */}
        {/* Annotations */}
        <Typography.Title level={5}>Annotations</Typography.Title>
        <Form.List name="annotations">
          {(fields, { add, remove }) => (
            <div>
              {fields.map(({ key, name, fieldKey, ...restField }) => (
                <Row gutter={[10, 10]}>
                  <Col span={22}>
                    <Form.Item
                      name={[name, "annotation"]}
                      fieldKey={[fieldKey, "annotation"]}
                      label="Annotation"
                    >
                      <Input />
                    </Form.Item>
                  </Col>
                  <Col>
                    <MinusCircleOutlined onClick={() => remove(name)} />
                  </Col>
                </Row>
              ))}
              <Form.Item>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  block
                  icon={<PlusOutlined />}
                >
                  Add Annotation
                </Button>
              </Form.Item>
            </div>
          )}
        </Form.List>
        {/* end Annotations */}
      </Form>
      <Modal
        visible={open}
        title="Table name"
        onCancel={() => {
          setName(config.table_name);
          setOwner(config.owner);
          setOpen(false);
        }}
        onOk={updateTableConfig}
      >
        <Input
          placeholder="Table name"
          value={name}
          onChange={(e) => {
            setName(e.target.value);
          }}
        />
        <Select
          style={{ width: "100%", marginTop: 20 }}
          placeholder="Select Owner"
          value={owner}
          onChange={(e) => setOwner(e)}
        >
          {table_owner.map((v) => (
            <Select.Option value={v} key={v}>
              {v}
            </Select.Option>
          ))}
        </Select>
      </Modal>
    </Card>
  );
}
