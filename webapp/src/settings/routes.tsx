import React from "react";
import {
  TableOutlined,
  SettingOutlined,
  CodeOutlined,
} from "@ant-design/icons";
import TableConfigPage from "../components/pages/table/TableConfigPage";
import CodePage from "../components/pages/code/CodePage";
import CodeAction from "../components/pages/code/components/CodeAction";
import SettingsPage from "../components/pages/settings/SettingsPage";
import TableAction from "../components/pages/table/TableAction";

interface Route {
  path: string;
  component: JSX.Element;
  title: string;
  icon: JSX.Element;
  hasSubMenu: boolean;
  action?: JSX.Element;
}

export const routes: Route[] = [
  {
    path: "/",
    title: "Table Config",
    component: <TableConfigPage />,
    icon: <TableOutlined />,
    action: <TableAction />,
    hasSubMenu: true,
  },
  {
    path: "/settings",
    title: "Settings",
    component: <SettingsPage />,
    icon: <SettingOutlined />,
    hasSubMenu: false,
  },
  {
    path: "/editor",
    title: "Query Editor",
    component: <CodePage />,
    icon: <CodeOutlined />,
    hasSubMenu: false,
    action: <CodeAction />,
  },
];
