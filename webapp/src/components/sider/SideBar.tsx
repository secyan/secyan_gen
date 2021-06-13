import React from "react";
import { matchPath } from "react-router";
import { useLocation, useHistory } from "react-router-dom";
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
} from "@ant-design/icons";
import Sider from "antd/lib/layout/Sider";
import { Menu } from "antd";
import { routes } from "../../settings/routes";

export default function SideBar() {
  const location = useLocation();
  const history = useHistory();
  const [selectedPath, setSelectedPath] = React.useState(routes[0].title);

  React.useEffect(() => {
    if (location.pathname !== routes[0].path) {
      let route = routes.find((r) => location.pathname.includes(r.path));
      if (route) {
        setSelectedPath(route?.title);
      }
    }
  }, [location]);

  return (
    <Menu
      theme="light"
      mode="vertical-left"
      selectedKeys={[selectedPath]}
      style={{ height: "100%" }}
    >
      {routes.map((r) => (
        <Menu.Item
          key={r.title}
          icon={r.icon}
          onClick={() => history.push(r.path)}
        >
          {r.title}
        </Menu.Item>
      ))}
    </Menu>
  );
}
function useStyles() {
  throw new Error("Function not implemented.");
}
