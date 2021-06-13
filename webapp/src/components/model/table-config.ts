export interface TableConfig {
  table_name: string;
  data_sizes: number[];
  data_paths: string[];
  columns: Column[];
}

export interface Column {
  column_type: string;
  name: string;
}

interface Result {
  code: string;
  output: any[][];
  joinGraph: any;
  isFreeConnex: boolean;
  errorTables: string[];
}
