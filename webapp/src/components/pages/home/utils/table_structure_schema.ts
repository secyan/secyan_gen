export const tableStructureSchema = {
  $schema: "http://json-schema.org/draft-06/schema#",
  type: "array",
  items: {
    $ref: "#/definitions/TableConfigElement",
  },
  definitions: {
    TableConfigElement: {
      type: "object",
      additionalProperties: false,
      properties: {
        data_sizes: {
          type: "array",
          items: {
            type: "integer",
          },
        },
        data_paths: {
          type: "array",
          items: {
            type: "string",
          },
        },
        table_name: {
          type: "string",
        },
        columns: {
          type: "array",
          items: {
            $ref: "#/definitions/Column",
          },
        },
      },
      required: ["columns", "data_sizes", "table_name"],
      title: "TableConfigElement",
    },
    Column: {
      type: "object",
      additionalProperties: false,
      properties: {
        column_type: {
          type: "string",
        },
        name: {
          type: "string",
        },
      },
      required: ["column_type", "name"],
      title: "Column",
    },
  },
};
