import {
  Button,
  Card,
  Col,
  notification,
  PageHeader,
  Row,
  Tabs,
  Typography,
} from "antd";
import Layout, { Content } from "antd/lib/layout/layout";
import Editor from "@monaco-editor/react";
import Sider from "antd/lib/layout/Sider";
import React from "react";
import { CodeContext } from "../../model/CodeContext";
import CodeDisplay from "./CodeDisplay";

const { TabPane } = Tabs;
const { Link } = Typography;

export default function HomePage() {
  const [height, setHeight] = React.useState(window.innerHeight);
  const [isLoading, setIsLoading] = React.useState(false);

  React.useEffect(() => {
    window.addEventListener("resize", () => {
      setHeight(window.innerHeight);
    });
  }, []);

  const {
    setCode,
    setTable,
    code,
    tableStructure,
    result,
    post,
  } = React.useContext(CodeContext);

  return (
    <Layout style={{ maxHeight: "100vh", overflow: "hidden", padding: 10 }}>
      <PageHeader title="CodeGen" />
      <Content>
        <Row style={{ height: "80%" }} gutter={[16, 10]}>
          <Col span={8}>
            <Card>
              <Tabs defaultActiveKey="1" onChange={() => {}}>
                <TabPane tab="SQL Statement" key="1">
                  <Editor
                    height={height - 300}
                    language="sql"
                    value={code}
                    options={{ minimap: { enabled: false } }}
                    onChange={(e) => {
                      if (e) {
                        setCode(e);
                      }
                    }}
                  />
                </TabPane>
                <TabPane tab="Table structure" key="2">
                  <Typography>
                    <Link
                      target="_blank"
                      href="https://github.com/sirily11/SECYAN-GEN/blob/master/examples/table_config.json"
                    >
                      Example Table Structure
                    </Link>
                  </Typography>
                  <Editor
                    height={height - 300}
                    value={tableStructure}
                    language="json"
                    options={{ minimap: { enabled: false } }}
                    onChange={(e) => {
                      if (e) {
                        setTable(e);
                      }
                    }}
                  />
                </TabPane>
              </Tabs>
              <Row style={{ justifyContent: "flex-end", marginTop: 10 }}>
                <Button
                  type="primary"
                  loading={isLoading}
                  onClick={async () => {
                    setIsLoading(true);
                    if (code?.length === 0 || tableStructure?.length === 0) {
                      window.alert("Invaild Input");
                      setIsLoading(false);
                      return;
                    }
                    try {
                      await post();
                      notification.info({
                        message: "Code generated",
                      });
                    } catch (err) {
                      notification.open({
                        message: "Cannot generate code",
                        description: `${err}`,
                        duration: 5,
                      });
                    } finally {
                      setIsLoading(false);
                    }
                  }}
                >
                  Convert
                </Button>
              </Row>
            </Card>
          </Col>
          <Col span={16}>{result && <CodeDisplay />}</Col>
        </Row>
      </Content>
    </Layout>
  );
}
