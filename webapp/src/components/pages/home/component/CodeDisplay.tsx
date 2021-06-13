import React from "react";
import Highlight, { defaultProps } from "prism-react-renderer";
import {
  Affix,
  Alert,
  Button,
  Card,
  Col,
  Popover,
  Row,
  Typography,
} from "antd";
import theme from "prism-react-renderer/themes/github";

// const { Title, Paragraph, Text, Link } = Typography;
// export default function CodeDisplay() {
//   const { result } = React.useContext(CodeContext);
//   const [copied, setCopied] = React.useState(false);
//   const [visible, setVisible] = React.useState(false);

//   React.useEffect(() => {
//     setCopied(false);
//   }, [result]);

//   return (
//     <Card style={{ width: "100%", height: "90vh", overflow: "scroll" }}>
//       <Affix style={{ position: "fixed", top: 110, right: 40 }}>
//         <Row gutter={[10, 10]}>
//           <Col>
//             <Button
//               onClick={() => {
//                 navigator.clipboard.writeText(result?.code ?? "");
//                 setCopied(true);
//               }}
//             >
//               {copied ? "Copied" : "Copy"}
//             </Button>
//           </Col>
//           <Col>
//             <Popover
//               content={<TreeDisplay />}
//               placement="leftBottom"
//               trigger="click"
//             >
//               <Button>Show Join Tree</Button>
//             </Popover>
//           </Col>
//         </Row>
//       </Affix>
//       <Typography>
//         <Title>Result</Title>
//       </Typography>
//       {result?.isFreeConnex === false && (
//         <Popover content={<ErrorTablesDisplay />}>
//           <Alert
//             type="error"
//             style={{ marginBottom: 10 }}
//             message={`Cannot auto generate a free connex join tree from query. Check the join tree and reorder your join statement.`}
//           />
//         </Popover>
//       )}
//       <Highlight
//         {...defaultProps}
//         code={result!.code}
//         language="cpp"
//         theme={theme}
//       >
//         {({ className, style, tokens, getLineProps, getTokenProps }) => (
//           <pre className={className} style={style}>
//             {tokens.map((line, i) => (
//               <div {...getLineProps({ line, key: i })}>
//                 {line.map((token, key) => (
//                   <span {...getTokenProps({ token, key })} />
//                 ))}
//               </div>
//             ))}
//           </pre>
//         )}
//       </Highlight>
//     </Card>
//   );
// }
