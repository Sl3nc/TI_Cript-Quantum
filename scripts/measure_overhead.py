#!/usr/bin/env python3
"""
Measure Profiling Overhead Script

Measures the overhead introduced by profiling instrumentation.
Validates that overhead stays within constitutional limits (<10%).

Usage:
    python scripts/measure_overhead.py [--iterations N]
"""

import time
import sys
from pathlib import Path
from statistics import mean

# Add root to path for imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.metrics import ProfilerManager
from src.algorithms.mlkem_kem import run_mlkem


def measure_baseline(iterations: int = 10, volume: int = 100) -> float:
    """
    Measure baseline execution time without profiling.
    
    Args:
        iterations: Number of iterations to average
        volume: Number of operations per iteration
        
    Returns:
        Average execution time in milliseconds
    """
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        run_mlkem(volume=volume, seed=42)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return mean(times)


def measure_with_profiling(iterations: int = 10, volume: int = 100) -> float:
    """
    Measure execution time with profiling enabled.
    
    Args:
        iterations: Number of iterations to average
        volume: Number of operations per iteration
        
    Returns:
        Average execution time in milliseconds
    """
    times = []
    profiler = ProfilerManager()
    
    for _ in range(iterations):
        start = time.perf_counter()
        profiler.profile_function(run_mlkem, volume=volume, seed=42)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return mean(times)


def calculate_overhead(baseline: float, profiled: float) -> float:
    """
    Calculate overhead percentage.
    
    Args:
        baseline: Baseline execution time (ms)
        profiled: Profiled execution time (ms)
        
    Returns:
        Overhead percentage
    """
    if baseline == 0:
        return 0.0
    return ((profiled - baseline) / baseline) * 100


def main():
    """Run overhead measurement and report results."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Measure profiling overhead")
    parser.add_argument("--iterations", "-i", type=int, default=10,
                       help="Number of iterations to average")
    parser.add_argument("--volume", "-v", type=int, default=100,
                       help="Number of operations per iteration")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("PROFILING OVERHEAD MEASUREMENT")
    print(f"{'='*60}")
    print(f"Algorithm: MLKEM_1024")
    print(f"Iterations: {args.iterations}")
    print(f"Volume: {args.volume}")
    print(f"{'='*60}\n")
    
    print("Measuring baseline (without profiling)...")
    baseline_avg = measure_baseline(args.iterations, args.volume)
    print(f"  Baseline average: {baseline_avg:.2f} ms")
    
    print("\nMeasuring with profiling...")
    profiled_avg = measure_with_profiling(args.iterations, args.volume)
    print(f"  Profiled average: {profiled_avg:.2f} ms")
    
    overhead_pct = calculate_overhead(baseline_avg, profiled_avg)
    
    print(f"\n{'='*60}")
    print(f"OVERHEAD: {overhead_pct:.2f}%")
    
    if overhead_pct < 10:
        print("✓ Within constitutional limits (<10%)")
        status = 0
    else:
        print("✗ EXCEEDS constitutional limits!")
        status = 1
    
    print(f"{'='*60}\n")
    
    return status


if __name__ == "__main__":
    sys.exit(main())
