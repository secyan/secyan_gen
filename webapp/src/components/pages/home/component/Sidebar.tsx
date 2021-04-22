import { Menu } from "antd";
import Sider from "antd/lib/layout/Sider";
import React from "react";

export default function Sidebar() {
  return (
    <Sider theme="light" width="80">
      <Menu>
        <Menu.Item> A </Menu.Item>
      </Menu>
    </Sider>
  );
}
