import * as monaco from "monaco-editor";
import { TableConfig } from "../table-config";
import { sqlKeywords } from "./utils";
export class EditorUtils {
  static generateSuggestions(range: any, tables?: TableConfig[]) {
    if (tables) {
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
