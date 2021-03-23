from flask import Flask, request, jsonify
from flask import render_template
import json
from codegen.codegen import Parser
from codegen.table.table import Table
from codegen.table.free_connex_table import FreeConnexTable
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify()


@app.route("/generate", methods=["POST"])
def generate_code():
    data = request.json
    tables = [FreeConnexTable.load_from_json(t) for t in json.loads(data['table'])]
    sql = data['sql']
    parser = Parser(sql=sql, tables=tables)
    output = parser.parse().to_output()
    graph = [t for t in parser.tables if len(t.children) > 0][0].get_root().to_json(
        output_attrs=parser.get_output_attributes())
    print(graph)
    return jsonify({"code": output, "joinGraph": graph})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
