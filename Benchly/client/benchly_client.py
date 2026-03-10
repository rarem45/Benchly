"""Benchly client: collect hardware info and submit benchmark results."""

import argparse
import json
import logging
import time

import requests

from shared.utils import configure_basic_logging, get_machine_identity
from shared.constants import DEFAULT_SERVER_URL, API_SUBMIT
from .benchmarks import run_benchmarks
from .config import DEFAULT_RUN_INTERVAL_SECONDS, DEFAULT_RUN_ONCE


def submit_results(server_url: str, payload: dict, timeout_s: int = 10) -> dict:
    endpoint = server_url.rstrip("/") + API_SUBMIT
    resp = requests.post(endpoint, json=payload, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()


def build_payload() -> dict:
    machine = get_machine_identity()
    results = run_benchmarks()
    return {
        "machine_id": machine["hostname"],
        "machine": machine,
        "results": results,
        "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchly client: run benchmarks and submit to a Benchly server.")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, help="Benchly server URL")
    parser.add_argument("--interval", type=int, default=DEFAULT_RUN_INTERVAL_SECONDS, help="Seconds between automatic submissions")
    parser.add_argument("--once", action="store_true", help="Run once (default)")
    parser.add_argument("--loop", action="store_true", help="Run continuously on interval")
    args = parser.parse_args()

    # Default behavior: run once if no mode is specified
    if not args.once and not args.loop:
        args.once = True

    configure_basic_logging()
    logger = logging.getLogger("benchly.client")

    try:
        while True:
            logger.info("Running Benchly benchmarks...")
            payload = build_payload()
            logger.debug("Payload: %s", json.dumps(payload, indent=2))
            try:
                resp = submit_results(args.server, payload)
                logger.info("Submitted: %s", resp)
            except Exception as ex:
                logger.exception("Failed to submit results: %s", ex)

            if args.once:
                break

            logger.info("Sleeping for %s seconds", args.interval)
            time.sleep(args.interval)

    except KeyboardInterrupt:
        logger.info("Interrupted")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
