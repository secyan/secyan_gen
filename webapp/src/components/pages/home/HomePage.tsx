// import {
//   Button,
//   Card,
//   Col,
//   Input,
//   Menu,
//   notification,
//   PageHeader,
//   Row,
//   Select,
//   Tabs,
//   Typography,
// } from "antd";
// import Layout, { Content } from "antd/lib/layout/layout";
// import Editor, { Monaco } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
// import Sider from "antd/lib/layout/Sider";
// import React from "react";
// // import { CodeContext } from "../../model/CodeContext";
// import { Utils } from "../../model/utils";
// import Sidebar from "./component/Sidebar";
// import { tableStructureSchema } from "./utils/table_structure_schema";

// const { TabPane } = Tabs;

// const { Link } = Typography;

// export default function HomePage() {
//   const [height, setHeight] = React.useState(window.innerHeight);
//   const [isLoading, setIsLoading] = React.useState(false);

//   React.useEffect(() => {
//     window.addEventListener("resize", () => {
//       setHeight(window.innerHeight);
//     });
//   }, []);

//   // const {
//   //   setCode,
//   //   setTable,
//   //   code,
//   //   tableStructure,
//   //   result,
//   //   post,
//   //   postDB,
//   //   backend,
//   //   functionName,
//   //   setFunctionName,
//   // } = React.useContext(CodeContext);

  // const handleSQLEditorWillMount = React.useCallback(
  //   (monaco: Monaco) => {
  //     monaco.languages.registerCompletionItemProvider("sql", {
  //       provideCompletionItems: (
  //         model: monaco.editor.ITextModel,
  //         position: monaco.Position
  //       ) => {
  //         var word = model.getWordUntilPosition(position);
  //         var range = {
  //           startLineNumber: position.lineNumber,
  //           endLineNumber: position.lineNumber,
  //           startColumn: word.startColumn,
  //           endColumn: word.endColumn,
  //         };
  //         if (tableStructure)
  //           return {
  //             suggestions: Utils.generateSuggestions(range, tableStructure),
  //           };
  //       },
  //     });

  //     monaco.languages.registerHoverProvider("sql", {
  //       provideHover: (
  //         model: monaco.editor.ITextModel,
  //         position: monaco.Position
  //       ) => {
  //         var word = model.getWordAtPosition(position);
  //         var range = {
  //           startLineNumber: position.lineNumber,
  //           endLineNumber: position.lineNumber,
  //           startColumn: word?.startColumn,
  //           endColumn: word?.endColumn,
  //         };
  //         return Utils.generateHover(
  //           range,
  //           model,
  //           word?.word ?? "",
  //           tableStructure
  //         );
  //       },
  //     });
  //   },
  //   [tableStructure]
  // );

  // const handleJSONEditorWillMount = React.useCallback(
  //   (monaco: Monaco) => {
  //     monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
  //       validate: true,
  //       enableSchemaRequest: true,
  //       schemas: [
  //         {
  //           uri: "https://raw.githubusercontent.com/sirily11/SECYAN-GEN/master/examples/table_config.json",
  //           fileMatch: ["*"],
  //           schema: tableStructureSchema,
  //         },
  //       ],
  //     });
  //   },
  //   [tableStructure]
  // );

//   return (
//     <Layout style={{ height: "100vh", overflow: "hidden", padding: 10 }}>
//       {/* <Header /> */}

//       <Layout>
//         <Content style={{ height: "100%" }}>
//           <Row style={{ height: "80%" }} gutter={[16, 10]}>
//             <Col span={8}>
//               <Card>
//                 <Tabs defaultActiveKey="0" onChange={() => {}}>
//                   <TabPane tab="Function Info" key="0">
//                     <Input
//                       value={functionName}
//                       placeholder="Function Name"
//                       onChange={(e) => {
//                         setFunctionName(e.target.value);
//                       }}
//                     />
//                   </TabPane>
//                   <TabPane tab="SQL Statement" key="1">
//                     <Editor
//                       height={height - 300}
//                       beforeMount={(e) => {
//                         handleSQLEditorWillMount(e);
//                       }}
//                       language="sql"
//                       value={code}
//                       options={{ minimap: { enabled: false } }}
//                       onChange={(e) => {
//                         if (e) {
//                           setCode(e);
//                         }
//                       }}
//                     />
//                   </TabPane>
//                   <TabPane tab="Table structure" key="2">
//                     <Typography>
//                       <Link
//                         target="_blank"
//                         href="https://github.com/sirily11/SECYAN-GEN/blob/master/examples/table_config.json"
//                       >
//                         Example Table Structure
//                       </Link>
//                     </Typography>
//                     <Editor
//                       height={height - 300}
//                       value={tableStructure}
//                       beforeMount={(e) => handleJSONEditorWillMount(e)}
//                       language="json"
//                       options={{ minimap: { enabled: false } }}
//                       onChange={(e) => {
//                         if (e) {
//                           setTable(e);
//                         }
//                       }}
//                     />
//                   </TabPane>
//                 </Tabs>
//                 <Row style={{ justifyContent: "flex-end", marginTop: 10 }}>
//                   <Button
//                     type="primary"
//                     loading={isLoading}
//                     onClick={async () => {
//                       setIsLoading(true);
//                       if (code?.length === 0 || tableStructure?.length === 0) {
//                         window.alert("Invaild Input");
//                         setIsLoading(false);
//                         return;
//                       }
//                       try {
//                         if (backend == "python") {
//                           await post();
//                         } else {
//                           await postDB();
//                         }
//                         notification.success({
//                           message: "Code generated",
//                         });
//                       } catch (err) {
//                         notification.error({
//                           message: "Cannot generate code",
//                           description: `${
//                             err?.response?.data ??
//                             "Cannot connect to the backend"
//                           }`,
//                           duration: 5,
//                         });
//                       } finally {
//                         setIsLoading(false);
//                       }
//                     }}
//                   >
//                     Convert
//                   </Button>
//                 </Row>
//               </Card>
//             </Col>
//             <Col span={16}>{result && <CodeDisplay />}</Col>
//           </Row>
//         </Content>
//       </Layout>
//     </Layout>
//   );
// }
