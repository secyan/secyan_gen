import { TableConfig } from "../table-config";
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

  static generateHover(
    range: any,
    model: any,
    text: string,
    tables?: TableConfig[]
  ) {
    if (tables) {
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
}
