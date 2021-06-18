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
        table_name: {
          type: "string",
        },
        owner: {
          type: "string",
        },
        columns: {
          type: "array",
          items: {
            $ref: "#/definitions/Column",
          },
        },
      },
      required: ["columns", "table_name"],
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
