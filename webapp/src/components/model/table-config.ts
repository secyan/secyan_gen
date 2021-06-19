import { Role } from "./SettingsContext";

export interface TableConfig {
  table_name: string;
  data_sizes: number[];
  data_paths: string[];
  columns: Column[];
  owner: Role;
}

export interface Column {
  column_type: string;
  name: string;
  annotation: string;
}

interface Result {
  code: string;
  output: any[][];
  joinGraph: any;
  isFreeConnex: boolean;
  errorTables: string[];
}
