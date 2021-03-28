import * as monaco from "monaco-editor";
export interface TableInterface {
  table_name: string;
  columns: ColumnInterface[];
}

export interface ColumnInterface {
  column_type: string;
  name: string;
}

export class Utils {
  static getURL(p: string): string {
    return new URL(p, process.env.REACT_APP_URL).href;
  }

  static generateHover(range: any, model: any, text: string, table?: string) {
    if (table) {
      let tables: TableInterface[] = JSON.parse(table);
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
            documentation: "",
            insertText: column.name,
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: range,
          });
        }
      }
      return suggestions;
    } else {
      return [];
    }
  }
}
