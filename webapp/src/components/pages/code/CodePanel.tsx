import React from "react";
import { CodeRunResult } from "../../model/code-run-result";
import { CodeContext } from "../../model/CodeContext";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
import { Utils } from "../../model/utils";
import { TableConfigContext } from "../../model/TableContext";
import {
  Button,
  Card,
  Col,
  Form,
  Input,
  notification,
  Row,
  Spin,
  Table,
  Tooltip,
} from "antd";

import Modal from "antd/lib/modal/Modal";
import AutoSizer from "react-virtualized-auto-sizer";

interface Props {
  codeRunResult: CodeRunResult;
  index: number;
  handleSQLEditorWillMount(m: any): void;
}

const height = "calc(100vh - 64px - 56px - 20px)";
const tableHeight = "calc(100vh - 64px - 56px - 200px)";

export default function CodePanel(props: Props) {
  const { codeRunResult, index, handleSQLEditorWillMount } = props;
  const { setCodeRunResults, codeRunResults, showEdit, setShowEdit } =
    React.useContext(CodeContext);
  const { configs } = React.useContext(TableConfigContext);

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
    if (codeRunResult.result?.server_result?.length ?? 0 > 0) {
      let cs = codeRunResult.result?.server_result[0]!;
      codeRunResult.result?.server_result.slice(1).forEach((s, i) => {
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
            {codeRunResult.result && (
              <Table
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
