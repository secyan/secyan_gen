import React from "react";
import { CodeRunResult } from "../../../model/code-run-result";
import { CodeContext } from "../../../model/CodeContext";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
import { Utils } from "../../../model/utils/utils";
import { TableConfigContext } from "../../../model/TableContext";
import { Card, Col, notification, Row, Spin, Table } from "antd";
//@ts-ignore
import { SettingsContext } from "../../../model/SettingsContext";
import {
  DataGrid,
  GridColDef,
  GridValueGetterParams,
} from "@material-ui/data-grid";
import { EditorUtils } from "../../../model/utils/editorUtils";
interface Props {
  codeRunResult: CodeRunResult;
  index: number;
}

const height = "calc(100vh - 64px - 56px - 20px)";
const tableHeight = "calc(100vh - 64px - 56px - 30px)";
let hover: monaco.IDisposable | undefined = undefined;
let completion: monaco.IDisposable | undefined = undefined;

export default function CodePanel(props: Props) {
  const { codeRunResult, index } = props;
  const { setCodeRunResults, codeRunResults, showEdit, setShowEdit } =
    React.useContext(CodeContext);

  const [isLoading, setIsLoading] = React.useState(true);
  const { configs } = React.useContext(TableConfigContext);
  const { role } = React.useContext(SettingsContext);
  const [editor, setEditor] =
    React.useState<monaco.editor.IStandaloneCodeEditor>();

  const handleSQLEditorWillMount = React.useCallback(
    (monaco: Monaco) => {
      hover?.dispose();
      completion?.dispose();
      completion = monaco.languages.registerCompletionItemProvider("sql", {
        provideCompletionItems: (
          model: monaco.editor.ITextModel,
          position: monaco.Position
        ) => {
          var word = model.getWordUntilPosition(position);
          var range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word.startColumn,
            endColumn: word.endColumn,
          };
          if (configs) {
            return {
              suggestions: EditorUtils.generateSuggestions(range, configs),
            };
          }
        },
      });

      hover = monaco.languages.registerHoverProvider("sql", {
        provideHover: (
          model: monaco.editor.ITextModel,
          position: monaco.Position
        ) => {
          var word = model.getWordAtPosition(position);
          var range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word?.startColumn,
            endColumn: word?.endColumn,
          };
          return Utils.generateHover(range, model, word?.word ?? "", configs);
        },
      });
    },
    [configs, editor]
  );

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
    let results: string[][] | undefined =
      role === "Server"
        ? codeRunResult.result?.server_result
        : codeRunResult.result?.client_result;
    if (results?.length ?? 0 > 0) {
      return results![0].map((v) => {
        return {
          title: v.toLocaleUpperCase(),
          field: v.toLowerCase(),
          width: v.length * 20,
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
          id: i,
        };
        s.forEach((c, j) => {
          data[cs[j]] = c;
        });
        res.push(data);
      });
    }

    return res;
  };

  return (
    <div style={{ padding: 10 }}>
      <Row gutter={[10, 10]}>
        <Col xs={8}>
          <Editor
            value={codeRunResult.code}
            onMount={(e) => {
              setEditor(e);
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
          <div style={{ height: tableHeight, overflowY: "hidden" }}>
            {codeRunResult.result && !isLoading && (
              <DataGrid columns={columns()} rows={rows()} rowHeight={60} />
            )}
          </div>
        </Col>
      </Row>
    </div>
  );
}
