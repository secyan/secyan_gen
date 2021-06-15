import React from "react";
import Tree from "react-d3-tree";
import { CodeContext } from "../../../model/CodeContext";

export default function TreeDisplay() {
  const { codeRunResults, index } = React.useContext(CodeContext);

  const result = codeRunResults[index]?.result;

  return (
    <div style={{ height: 500, width: 1000 }}>
      {/* {JSON.stringify(result?.joinGraph)} */}
      {result && (
        <Tree
          data={result.joinGraph}
          orientation="vertical"
          pathFunc="step"
          translate={{ y: 100, x: 400 }}
          nodeSize={{ x: 257, y: 175 }}
        />
      )}
    </div>
  );
}
