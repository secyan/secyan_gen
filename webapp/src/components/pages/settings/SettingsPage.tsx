import { Card, Typography, Form, Select } from "antd";
import React from "react";
import { BackEnd, Role, SettingsContext } from "../../model/SettingsContext";

interface FormValue {
  role: Role;
  backend: BackEnd;
}

export default function SettingsPage() {
  const { role, setRole, backend, setBackend } =
    React.useContext(SettingsContext);

  const formValue: FormValue = {
    role: role,
    backend: backend,
  };

  return (
    <div style={{ padding: 10 }}>
      <Typography.Title level={3}>Settings</Typography.Title>
      <Card>
        <Typography.Title level={5}>General Settings</Typography.Title>
        <Form
          initialValues={formValue}
          onValuesChange={(changed) => {
            if (changed.role) {
              setRole(changed.role);
            }
            if (changed.backend) {
              setBackend(changed.backend);
            }
          }}
        >
          <Form.Item label="Role" name="role">
            <Select>
              {["Client", "Server"].map((v, i) => (
                <Select.Option value={v} key={`role-${i}`}>
                  {v}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            label="Backend"
            name="backend"
            extra="This will only affect the c++ code generator"
          >
            <Select>
              {["Default Backend", "Postgres Backend"].map((v, i) => (
                <Select.Option value={v} key={`role-${i}`}>
                  {v}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
