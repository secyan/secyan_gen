import {
  Button,
  Card,
  Col,
  Input,
  notification,
  PageHeader,
  Row,
  Select,
  Tabs,
  Typography,
} from "antd";
import Layout, { Content } from "antd/lib/layout/layout";
import Editor from "@monaco-editor/react";
import Sider from "antd/lib/layout/Sider";
import React from "react";
import { CodeContext } from "../../model/CodeContext";
import CodeDisplay from "./component/CodeDisplay";
import Header from "./component/Header";

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
    postDB,
    backend,
    functionName,
    setFunctionName,
  } = React.useContext(CodeContext);

  return (
    <Layout style={{ height: "100vh", overflow: "hidden", padding: 10 }}>
      <Header />
      <Content style={{ height: "100%" }}>
        <Row style={{ height: "80%" }} gutter={[16, 10]}>
          <Col span={8}>
            <Card>
              <Tabs defaultActiveKey="0" onChange={() => {}}>
                <TabPane tab="Function Info" key="0">
                  <Input
                    value={functionName}
                    placeholder="Function Name"
                    onChange={(e) => {
                      setFunctionName(e.target.value);
                    }}
                  />
                </TabPane>
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
                      if (backend == "python") {
                        await post();
                      } else {
                        await postDB();
                      }
                      notification.info({
                        message: "Code generated",
                      });
                    } catch (err) {
                      notification.error({
                        message: "Cannot generate code",
                        description: `${err?.response?.data}`,
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
