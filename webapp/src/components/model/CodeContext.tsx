/** @format */

import React, { Component } from "react";
import { Utils } from "./utils";
import Axios from "axios";

interface Result {
  code: string;
  joinGraph: any;
  isFreeConnex: boolean;
  errorTables: string[];
}

interface CodeContextState {
  code?: string;
  tableStructure?: string;
  result?: Result;
  post(): Promise<void>;
  setCode(code: string): void;
  setTable(table: string): void;
}

interface CodeProps {}

export class CodeProvider extends Component<CodeProps, CodeContextState> {
  constructor(props: CodeProps) {
    super(props);
    this.state = {
      setCode: this.setCode,
      setTable: this.setTable,
      post: this.post,
    };
  }

  componentDidMount() {
    let code = window.localStorage.getItem("code");
    let tableStructure = window.localStorage.getItem("tableStructure");
    this.setState({
      code: code ?? "",
      tableStructure: tableStructure ?? "",
    });
  }

  post = async (): Promise<void> => {
    this.setState({ result: undefined });
    let url = Utils.getURL("generate");
    console.log("url", url);
    let resp = await Axios.post<Result>(url, {
      sql: this.state.code,
      table: this.state.tableStructure,
    });
    console.log(resp.data);
    this.setState({ result: resp.data });
  };

  setCode = (code: string) => {
    this.setState({ code });
    window.localStorage.setItem("code", code);
  };

  setTable = (tableStructure: string) => {
    this.setState({ tableStructure });
    window.localStorage.setItem("tableStructure", tableStructure);
  };

  render() {
    return (
      <CodeContext.Provider value={this.state}>
        {this.props.children}
      </CodeContext.Provider>
    );
  }
}

//@ts-ignore
const context: CodeContextState = {};

export const CodeContext = React.createContext(context);
