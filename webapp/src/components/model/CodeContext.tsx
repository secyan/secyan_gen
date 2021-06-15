import { notification } from "antd";
import axios from "axios";
import React from "react";
import { CodeRunResult } from "./code-run-result";
import { TableConfig } from "./table-config";
import { Utils } from "./utils";
import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";

interface Code {
  codeRunResults: CodeRunResult[];
  setCodeRunResults(c: CodeRunResult[]): void;
  runCode(index: number, tableConfigs: TableConfig[]): Promise<void>;
  isLoading: boolean;
  index: number;
  setIndex(num: number): void;
  showEdit: boolean;
  setShowEdit(b: boolean): void;
  // initSQLEditor(m: Monaco): void;
}

//@ts-ignore
export const CodeContext = React.createContext<Code>({});

export default function CodeProvider(props: any) {
  const { children } = props;
  const [codeRunResults, setCodeRunResultState] = React.useState<
    CodeRunResult[]
  >([]);

  const [isLoading, setIsLoading] = React.useState(false);
  const [index, setIndex] = React.useState(0);
  const [showEdit, setShowEdit] = React.useState(false);

  React.useEffect(() => {
    let code = localStorage.getItem("code");
    if (code) {
      try {
        setCodeRunResultState(JSON.parse(code));
      } catch (err) {
        console.log("No Code Saved");
      }
    }
  }, []);

  const setCodeRunResults = React.useCallback(
    (c: CodeRunResult[]) => {
      localStorage.setItem("code", JSON.stringify(c));
      setCodeRunResultState(JSON.parse(JSON.stringify(c)));
    },
    [codeRunResults]
  );

  const runCode = React.useCallback(
    async (index: number, tableConfigs: TableConfig[]) => {
      let url = Utils.getURL("/generate_python");
      let data = codeRunResults[index];

      try {
        setIsLoading(true);
        let resp = await axios.post(url, {
          sql: data.code,
          annotation_name: data.annotation_name,
          num_of_rows: data.num_of_rows,
          table: JSON.stringify(tableConfigs),
        });

        codeRunResults[index].result = resp.data;

        setCodeRunResults(codeRunResults);
        notification.info({
          message: "Code results returned",
          placement: "bottomRight",
        });
        setIsLoading(false);
      } catch (err) {
        setIsLoading(false);
        notification.error({
          message: "Cannot generate code",
          description: `${
            err?.response?.data ?? "Cannot connect to the backend"
          }`,
          duration: 5,
          placement: "bottomRight",
        });
      }
    },
    [codeRunResults]
  );

  const value: Code = {
    codeRunResults,
    setCodeRunResults,
    runCode,
    isLoading,
    index,
    setIndex,
    showEdit,
    setShowEdit,
  };

  return <CodeContext.Provider value={value}>{children}</CodeContext.Provider>;
}
