import * as monaco from "monaco-editor";
export interface TableInterface {
  table_name: string;
  columns: ColumnInterface[];
}

export interface ColumnInterface {
  column_type: string;
  name: string;
}

export const sqlKeywords = [
  {
    keyword: "select",
    desc: "",
  },
  {
    keyword: "from",
    desc: "",
  },
  {
    keyword: "where",
    desc: "",
  },
  {
    keyword: "sum",
    desc: "Aggregation function",
  },
  {
    keyword: "max",
    desc: "Aggregation function",
  },
  {
    keyword: "avg",
    desc: "Aggregation function",
  },
  {
    keyword: "count",
    desc: "Aggregation function",
  },

  {
    keyword: "group by",
    desc: "",
  },
  {
    keyword: "desc",
    desc: "",
  },
  {
    keyword: "limit",
    desc: "",
  },
  {
    keyword: "having",
    desc: "",
  },
  {
    keyword: "exists",
    desc: "",
  },
];

export class Utils {
  static getURL(p: string): string {
    return new URL(p, process.env.REACT_APP_URL).href;
  }

  static generateHover(range: any, model: any, text: string, table?: string) {
    if (table) {
      let tables: TableInterface[] = JSON.parse(table);
      for (let k of sqlKeywords) {
        if (text.toLowerCase().includes(k.keyword.toLowerCase())) {
          return {
            range,
            contents: [{ value: "SQL Built In" }, { value: k.desc }],
          };
        }
      }
      for (let table of tables) {
        if (text.toLowerCase().includes(table.table_name.toLowerCase())) {
          return {
            range,
            contents: [{ value: "Table Name" }],
          };
        }

        for (let column of table.columns) {
          if (text.toLocaleLowerCase().includes(column.name.toLowerCase())) {
            return {
              range,
              contents: [
                { value: table.table_name },
                { value: `**Type: ${column.column_type}**` },
              ],
            };
          }
        }
      }
    } else
      return {
        range,
        contents: [],
      };
  }

  static generateSuggestions(range: any, table?: string) {
    if (table) {
      let tables: TableInterface[] = JSON.parse(table);
      let suggestions = [];
      for (let table of tables) {
        suggestions.push({
          label: table.table_name,
          kind: monaco.languages.CompletionItemKind.Constant,
          documentation: "",
          insertText: table.table_name.toUpperCase(),
          insertTextRules:
            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range: range,
        });

        for (let column of table.columns) {
          suggestions.push({
            label: column.name,
            kind: monaco.languages.CompletionItemKind.Constant,
            documentation: `${column.column_type}`,
            insertText: column.name,
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: range,
          });
        }
      }

      for (let k of sqlKeywords) {
        suggestions.push({
          label: k.keyword,
          kind: monaco.languages.CompletionItemKind.Keyword,
          document: k.desc,
          insertText: k.keyword.toUpperCase(),
          insertTextRules:
            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range: range,
        });
      }

      return suggestions;
    } else {
      return [];
    }
  }
}
