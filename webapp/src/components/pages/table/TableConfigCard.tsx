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
}

export default function TableConfigCard(props: Props) {
  const { config, index } = props;
  const [name, setName] = React.useState(config.table_name);
  const [owner, setOwner] = React.useState(config.owner);
  const [open, setOpen] = React.useState(false);
  const { setConfigs, configs } = React.useContext(TableConfigContext);

  const formValues = React.useCallback(() => {
    let longest = Math.max(
      config?.data_paths?.length ?? 0,
      config?.data_sizes?.length ?? 0
    );
    let path_size = Array.from(Array(longest)).map((c) => {
      return { size: undefined, path: undefined };
    });

    for (let i = 0; i < longest; i++) {
      if (config?.data_sizes?.length ?? 0 < i) {
        //@ts-ignore
        path_size[i].size = config.data_sizes[i];
      }

      if (config?.data_paths?.length ?? 0 < i) {
        //@ts-ignore
        path_size[i].path = config.data_paths[i];
      }

      return {
        path_size,
        columns: config.columns,
      };
    }
  }, [config]);

  const updateTableConfig = React.useCallback(() => {
    configs[index].table_name = name;
    configs[index].owner = owner;
    setConfigs(configs);
    setOpen(false);
  }, [name, owner]);

  const updateConfig = React.useCallback(
    (value: FormValue) => {
      let path_size = value.path_size.filter((v) => v !== undefined);
      configs[index].data_sizes = path_size.map((v: any) => parseInt(v.size));
      configs[index].data_paths = path_size.map((v: any) => v.path);
      configs[index].columns = value.columns;
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
                    <Col md={12} xs={22}>
                      <Form.Item
                        {...restField}
                        name={[name, "annotation"]}
                        fieldKey={[fieldKey, "Annotation"]}
                        help="Will use this field to add annotation"
                        rules={[
                          {
                            required: false,
                            message: "",
                          },
                        ]}
                      >
                        <Input placeholder="Annotation SQL" />
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
