import React from "react";

interface Code {
  sql: string;
  setSQL(sql: string): void;
}

//@ts-ignore
const CodeContext = React.createContext<Code>({});

export default function CodeProvider() {
  return <div></div>;
}
