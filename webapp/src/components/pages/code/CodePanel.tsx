import React from "react";
import { CodeRunResult } from "../../model/code-run-result";
import { CodeContext } from "../../model/CodeContext";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
import { Utils } from "../../model/utils";
import { TableConfigContext } from "../../model/TableContext";
import { Card, Col, notification, Row, Spin } from "antd";
//@ts-ignore
import { InfinityTable } from "antd-table-infinity";
import { SettingsContext } from "../../model/SettingsContext";

interface Props {
  codeRunResult: CodeRunResult;
  index: number;
  handleSQLEditorWillMount(m: any): void;
}

const height = "calc(100vh - 64px - 56px - 20px)";
const tableHeight = "calc(100vh - 64px - 56px - 150px)";

export default function CodePanel(props: Props) {
  const { codeRunResult, index, handleSQLEditorWillMount } = props;
  const { setCodeRunResults, codeRunResults, showEdit, setShowEdit } =
    React.useContext(CodeContext);

  const [isLoading, setIsLoading] = React.useState(true);

  const { role } = React.useContext(SettingsContext);

  React.useEffect(() => {
    notification.info({
      message: "Loading Data",
      placement: "bottomRight",
    });
  }, []);

  // Update editor code
  const updateCode = React.useCallback(
    (code: string) => {
      codeRunResults[index].code = code;
      setCodeRunResults(codeRunResults);
    },
    [codeRunResult]
  );

  // Table columns
  const columns = () => {
    if (codeRunResult.result?.server_result?.length ?? 0 > 0) {
      return codeRunResult.result?.server_result[0].map((v) => {
        return {
          title: v.toLocaleUpperCase(),
          dataIndex: v.toLowerCase(),
          key: v.toLowerCase(),
        };
      });
    }
    return [];
  };

  const rows = () => {
    let res: any[] = [];
    let results: string[][] | undefined =
      role === "Server"
        ? codeRunResult.result?.server_result
        : codeRunResult.result?.client_result;
    if (results) {
      let cs = results[0]!;
      results.slice(1).forEach((s, i) => {
        let data: { [key: string]: any } = {
          key: i,
        };
        s.forEach((c, j) => {
          data[cs[j]] = c;
        });
        res.push(data);
      });
    }

    return res;
  };

  rows();

  return (
    <div style={{ padding: 10 }}>
      <Row gutter={[10, 10]}>
        <Col xs={8}>
          <Editor
            value={codeRunResult.code}
            onMount={() => {
              setIsLoading(false);
              notification.close("Data Loaded");
            }}
            language="sql"
            beforeMount={(e) => handleSQLEditorWillMount(e)}
            options={{ minimap: { enabled: false } }}
            height={height}
            onChange={(e) => {
              updateCode(e as string);
            }}
          />
        </Col>
        <Col
          xs={16}
          style={{ overflowY: "scroll", overflowX: "scroll", height: "100%" }}
        >
          <Card style={{ height: height, overflowY: "hidden" }}>
            {codeRunResult.result && !isLoading && (
              <InfinityTable
                style={{
                  width: "100%",
                }}
                columns={columns()}
                dataSource={rows()}
                scroll={{ y: tableHeight, x: "4000px" }}
              />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
}
