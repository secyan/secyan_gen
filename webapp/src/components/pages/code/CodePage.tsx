import React from "react";

import { Affix, Button, Col, Row, Table, Tabs } from "antd";
import { CodeContext } from "../../model/CodeContext";
import { TableConfigContext } from "../../model/TableContext";
import { Utils } from "../../model/utils";
import CodePanel from "./CodePanel";
import { PlusOutlined } from "@ant-design/icons";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";

export default function CodePage() {
  const { codeRunResults, setCodeRunResults, setIndex } =
    React.useContext(CodeContext);
  const { configs } = React.useContext(TableConfigContext);

  const handleSQLEditorWillMount = React.useCallback(
    (monaco: Monaco) => {
      monaco.languages.registerCompletionItemProvider("sql", {
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
              suggestions: Utils.generateSuggestions(range, configs),
            };
          }
        },
      });

      monaco.languages.registerHoverProvider("sql", {
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
    [configs]
  );

  const renderPanel = React.useCallback(() => {
    return codeRunResults.map((c, i) => (
      <Tabs.TabPane tab={c.name} key={i} style={{ height: "100%" }}>
        <CodePanel
          codeRunResult={c}
          index={i}
          handleSQLEditorWillMount={handleSQLEditorWillMount}
        />
      </Tabs.TabPane>
    ));
  }, [codeRunResults]);

  return (
    <Tabs
      type="editable-card"
      style={{ height: "100%" }}
      addIcon={<PlusOutlined />}
      onChange={(index) => {
        setIndex(parseInt(index));
      }}
      onEdit={(targetKey, action) => {
        if (action === "add") {
          codeRunResults.push({
            name: "newResult",
            code: "",
            num_of_rows: 100,
            annotation_name: "q3_annot",
          });
          setCodeRunResults(codeRunResults);
        } else {
          codeRunResults.splice(parseInt(targetKey as string), 1);
          setCodeRunResults(codeRunResults);
        }
      }}
    >
      {renderPanel()}
    </Tabs>
  );
}
