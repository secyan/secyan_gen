import React from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { Button, Card, Layout, Menu, Row } from "antd";
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
} from "@ant-design/icons";
import "antd/dist/antd.css";
import "./index.css";
import SideBar from "./components/sider/SideBar";
import { routes } from "./settings/routes";
import TableConfigProvider from "./components/model/TableContext";

const { Header, Sider, Content } = Layout;

function App() {
  const [collapsed, setCollapsed] = React.useState(false);

  return (
    <div style={{ overflow: "hidden" }}>
      <TableConfigProvider>
        <Router>
          <Layout style={{ height: "100vh", overflow: "hidden" }}>
            <Card style={{ margin: 0, padding: 0 }} bodyStyle={{ padding: 0 }}>
              <Row align="middle">
                <div
                  className="trigger"
                  onClick={() => setCollapsed(!collapsed)}
                >
                  {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                </div>
                <h1 style={{ padding: 10 }}>CodeGen</h1>
              </Row>
            </Card>

            <Layout style={{ background: "white" }}>
              <Sider
                collapsible
                style={{ background: "#fff" }}
                trigger={null}
                collapsed={collapsed}
              >
                <SideBar />
              </Sider>
              <Content
                style={{
                  margin: "0px 0px",
                  padding: 0,
                  minHeight: 280,
                }}
              >
                <Switch>
                  {routes.map((r, i) => (
                    <Route key={`route-${i}`} path={r.path} exact>
                      {r.component}
                    </Route>
                  ))}
                </Switch>
              </Content>
            </Layout>
          </Layout>
        </Router>
      </TableConfigProvider>
    </div>
  );
}

export default App;
