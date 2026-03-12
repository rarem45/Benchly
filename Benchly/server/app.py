"""Benchly server: REST API for collecting and querying benchmarks."""

from flask import Flask, jsonify, request
from flask_cors import CORS

from . import db
from .config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT, RUN_BENCHMARK_AUTH_TOKEN
from client.benchly_client import build_payload


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Benchly server is running"})

    @app.route("/submit", methods=["POST"])
    def submit():
        payload = request.get_json(force=True, silent=True)
        if not payload:
            return jsonify({"error": "Invalid JSON payload"}), 400

        machine_id = payload.get("machine_id")
        if not machine_id:
            return jsonify({"error": "Missing machine_id"}), 400

        # Persist to DB
        record_id = db.insert_benchmark(machine_id=machine_id, payload=payload)
        return jsonify({"status": "ok", "record_id": record_id}), 201

    @app.route("/leaderboard", methods=["GET"])
    def leaderboard():
        limit = request.args.get("limit", default=100, type=int)
        offset = request.args.get("offset", default=0, type=int)
        data = db.get_leaderboard(limit=limit, offset=offset)
        return jsonify({"results": data.get("results", []), "count": len(data.get("results", [])), "total": data.get("total", 0)})

    @app.route("/history", methods=["GET"])
    def history():
        machine_id = request.args.get("machine_id")
        if not machine_id:
            return jsonify({"error": "machine_id is required"}), 400

        limit = request.args.get("limit", default=100, type=int)
        data = db.get_history(machine_id=machine_id, limit=limit)
        return jsonify({"results": data, "count": len(data)})

    @app.route("/run-benchmark", methods=["POST"])
    def run_benchmark():
        # Optional token-based guard to avoid arbitrary public execution
        if RUN_BENCHMARK_AUTH_TOKEN:
            token = request.headers.get("Authorization") or request.args.get("token")
            if token != RUN_BENCHMARK_AUTH_TOKEN:
                return jsonify({"error": "Unauthorized"}), 401

        payload = build_payload()
        record_id = db.insert_benchmark(machine_id=payload.get("machine_id"), payload=payload)
        return jsonify({"status": "ok", "record_id": record_id, "machine_id": payload.get("machine_id")}), 201

    return app


if __name__ == "__main__":
    db.init_db()
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
