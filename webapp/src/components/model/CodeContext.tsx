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
  backend: string;
  databaseName?: string;
  functionName?: string;
  setFunctionName(name: string): void;
  setBackend(backend: string): void;
  post(): Promise<void>;
  postDB(): Promise<void>;
  setCode(code: string): void;
  setDatabase(name?: string): void;
  setTable(table: string): void;
}

interface CodeProps {}

export class CodeProvider extends Component<CodeProps, CodeContextState> {
  constructor(props: CodeProps) {
    super(props);
    let backend = localStorage.getItem("backend") ?? "python";
    let createDB = localStorage.getItem("createDB") === "true" ? true : false;
    let dbName = !createDB
      ? localStorage.getItem("dbName") ?? undefined
      : undefined;

    this.state = {
      setCode: this.setCode,
      setBackend: this.setBackend,
      backend: backend,
      setTable: this.setTable,
      post: this.post,
      setDatabase: this.setDatabase,
      postDB: this.postDB,
      setFunctionName: this.setFunctionName,
      databaseName: dbName,
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

  setFunctionName = (name: string) => {
    this.setState({ functionName: name });
  };

  /**
   * Set used database name
   * @param name Database name
   */
  setDatabase = (name?: string) => {
    this.setState({ databaseName: name });
  };

  setBackend = (end: string) => {
    this.setState({ backend: end });
    localStorage.setItem("backend", end);
  };

  /**
   * Post request and update generated code
   */
  post = async (): Promise<void> => {
    this.setState({ result: undefined });
    let url = Utils.getURL("generate");
    let resp = await Axios.post<Result>(url, {
      sql: this.state.code,
      table: this.state.tableStructure,
      functionName: this.state.functionName,
    });
    this.setState({ result: resp.data });
  };

  /**
   * Post request using db execution plan
   */
  postDB = async (): Promise<void> => {
    this.setState({ result: undefined });
    let url = Utils.getURL("generate_db");
    if (localStorage.getItem("createDB") === "true") {
      await this.createDB();
    }
    let resp = await Axios.post<Result>(url, {
      sql: this.state.code,
      table: this.state.tableStructure,
      database: this.state.databaseName,
      functionName: this.state.functionName,
    });
    this.setState({ result: resp.data });
  };

  createDB = async (): Promise<void> => {
    let code = localStorage.getItem("createScript");
    let url = Utils.getURL("create_db");
    await Axios.post(url, { data: code });
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
