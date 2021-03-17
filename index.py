from flask import Flask, request, jsonify
from flask import render_template
import json
from codegen.codegen import Parser
from codegen.table.table import Table
import subprocess

app = Flask(__name__)


@app.route("/")
def index():
    version = subprocess.check_output(["git", "describe"]).strip()
    return render_template("index.html", version=str(version).replace("b", ""))


@app.route("/generate", methods=["POST"])
def generate_code():
    data = request.json
    tables = [Table.load_from_json(t) for t in json.loads(data['table'])]
    sql = data['sql']
    parser = Parser(sql=sql, tables=tables)
    output = parser.parse().to_output()

    return jsonify({"code": output})


if __name__ == '__main__':
    app.run(debug=True)
