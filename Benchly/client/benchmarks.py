"""Benchmark routines for Benchly client."""

import os
import random
import time
from typing import Dict

from .config import DEFAULT_DISK_TEST_FILE


def cpu_benchmark(iterations: int = 200_000) -> Dict[str, float]:
    """Simple CPU-bound benchmark: compute primes or Fibonacci-like workload."""
    start = time.perf_counter()
    acc = 0
    for i in range(1, iterations + 1):
        acc += (i * i) % (i + 1)
    duration = time.perf_counter() - start
    return {"cpu_ops": iterations, "duration_s": duration}


def ram_benchmark(size_mb: int = 256) -> Dict[str, float]:
    """Measure memory write speed by populating a bytearray."""
    size_bytes = size_mb * 1024 * 1024
    start = time.perf_counter()
    buffer = bytearray(size_bytes)
    for i in range(len(buffer)):
        buffer[i] = i & 0xFF
    duration = time.perf_counter() - start
    # Touch memory to avoid lazy allocation effects
    checksum = sum(buffer)
    return {"ram_size_mb": size_mb, "duration_s": duration, "checksum": checksum}


def disk_benchmark(file_path: str = str(DEFAULT_DISK_TEST_FILE), size_mb: int = 64) -> Dict[str, float]:
    """Measure disk write/read speed using a temporary file."""
    data = os.urandom(size_mb * 1024 * 1024)
    start = time.perf_counter()
    with open(file_path, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    write_duration = time.perf_counter() - start

    start = time.perf_counter()
    with open(file_path, "rb") as f:
        _ = f.read()
    read_duration = time.perf_counter() - start

    try:
        os.remove(file_path)
    except OSError:
        pass

    return {
        "disk_test_file": file_path,
        "size_mb": size_mb,
        "write_seconds": write_duration,
        "read_seconds": read_duration,
    }


def run_benchmarks() -> Dict[str, Dict[str, float]]:
    return {
        "cpu": cpu_benchmark(),
        "ram": ram_benchmark(),
        "disk": disk_benchmark(),
    }
