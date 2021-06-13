import React from "react";
import { TableOutlined } from "@ant-design/icons";
import TableConfigPage from "../components/pages/table/TableConfigPage";

interface Route {
  path: string;
  component: JSX.Element;
  title: string;
  icon: JSX.Element;
}

export const routes: Route[] = [
  {
    path: "/",
    title: "Table Config",
    component: <TableConfigPage />,
    icon: <TableOutlined />,
  },
];
