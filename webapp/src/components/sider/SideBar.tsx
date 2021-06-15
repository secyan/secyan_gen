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
import { TableConfigContext } from "../model/TableContext";
import SubMenu from "antd/lib/menu/SubMenu";

export default function SideBar(props: { expanded: boolean }) {
  const { configs } = React.useContext(TableConfigContext);
  const location = useLocation();
  const history = useHistory();
  const [selectedPath, setSelectedPath] = React.useState(routes[0].title);
  const { expanded } = props;

  React.useEffect(() => {
    if (location.pathname !== routes[0].path) {
      let route = routes.find(
        (r) => location.pathname.includes(r.path) && r.path !== routes[0].path
      );
      if (route) {
        setSelectedPath(route?.title);
      }
    } else {
      setSelectedPath(routes[0].path);
    }
  }, [location]);

  const renderSubMenu = React.useCallback(
    (path: string) => {
      if (path === routes[0].path) {
        return configs.map((c, i) => (
          <Menu.Item
            key={c.table_name}
            onClick={() => {
              history.push(`${routes[0].path}?table=${c.table_name}`);
            }}
          >
            {c.table_name}
          </Menu.Item>
        ));
      } else {
        return [];
      }
    },
    [configs]
  );

  const renderMenu = React.useCallback(() => {
    return routes.map((r) => {
      let subMenus = renderSubMenu(r.path);

      if (!r.hasSubMenu) {
        return (
          <Menu.Item
            key={r.title}
            icon={r.icon}
            onClick={() => history.push(r.path)}
          >
            {r.title}
          </Menu.Item>
        );
      } else {
        return (
          <SubMenu
            key={r.title}
            title={r.title}
            onTitleClick={() => history.push(r.path)}
            icon={r.icon}
          >
            {subMenus}
          </SubMenu>
        );
      }
    });
  }, [configs]);

  return (
    <Menu
      theme="light"
      mode="inline"
      selectedKeys={[selectedPath]}
      style={{ height: "100%" }}
    >
      {renderMenu()}
    </Menu>
  );
}
function useStyles() {
  throw new Error("Function not implemented.");
}
