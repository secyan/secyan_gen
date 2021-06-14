interface Result {
  client_result: string[][];
  server_result: string[][];
  joinGraph: any;
  isFreeConnex: boolean;
  errorTables: string[];
}

export interface CodeRunResult {
  name: string;
  code: string;
  result?: Result;
  num_of_rows: number;
  annotation_name: string;
}
