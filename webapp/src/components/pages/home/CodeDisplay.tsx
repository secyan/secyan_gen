import React from "react";
import Highlight, { defaultProps } from "prism-react-renderer";
import { CodeContext } from "../../model/CodeContext";
import { Affix, Button, Card, Col, Popover, Row, Typography } from "antd";
import theme from "prism-react-renderer/themes/github";
import TreeDisplay from "./TreeDisplay";

const { Title, Paragraph, Text, Link } = Typography;
export default function CodeDisplay() {
  const { result } = React.useContext(CodeContext);
  const [copied, setCopied] = React.useState(false);
  React.useEffect(() => {
    setCopied(false);
  }, [result]);

  return (
    <Card style={{ width: "100%", height: "90vh", overflow: "scroll" }}>
      <Affix style={{ position: "fixed", top: 110, right: 40 }}>
        <Row gutter={[10, 10]}>
          <Col>
            <Button
              onClick={() => {
                navigator.clipboard.writeText(result?.code ?? "");
                setCopied(true);
              }}
            >
              {copied ? "Copied" : "Copy"}
            </Button>
          </Col>
          <Col>
            <Popover content={<TreeDisplay />} placement="leftBottom">
              <Button>Show Join Tree</Button>
            </Popover>
          </Col>
        </Row>
      </Affix>
      <Typography>
        <Title>Result</Title>
      </Typography>
      <Highlight
        {...defaultProps}
        code={result!.code}
        language="cpp"
        theme={theme}
      >
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <pre className={className} style={style}>
            {tokens.map((line, i) => (
              <div {...getLineProps({ line, key: i })}>
                {line.map((token, key) => (
                  <span {...getTokenProps({ token, key })} />
                ))}
              </div>
            ))}
          </pre>
        )}
      </Highlight>
    </Card>
  );
}
