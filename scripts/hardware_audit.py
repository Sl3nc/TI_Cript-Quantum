#!/usr/bin/env python3
"""
Hardware and Dependency Audit Script

Generates a comprehensive audit report including:
- Hardware specifications hash
- Python version
- Installed package versions
- Environment reproducibility data

Usage:
    python scripts/hardware_audit.py [--output <path>]
"""

import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path


def get_hardware_info():
    """Collect hardware and system information."""
    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
        cpu_data = {
            "brand": cpu_info.get("brand_raw", "Unknown"),
            "arch": cpu_info.get("arch", "Unknown"),
            "count": cpu_info.get("count", 0),
            "hz": cpu_info.get("hz_advertised_friendly", "Unknown"),
        }
    except ImportError:
        cpu_data = {"error": "py-cpuinfo not installed"}

    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_data = {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
        }
    except ImportError:
        memory_data = {"error": "psutil not installed"}

    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu": cpu_data,
        "memory": memory_data,
    }


def get_installed_packages():
    """Get list of installed packages with versions."""
    try:
        from importlib.metadata import distributions
        packages = {}
        for dist in distributions():
            packages[dist.name] = dist.version
        return packages
    except ImportError:
        return {"error": "importlib.metadata not available"}


def compute_environment_hash(hardware_info, packages):
    """Compute SHA256 hash of hardware and dependency configuration."""
    combined_data = {
        "hardware": hardware_info,
        "packages": packages,
    }
    json_str = json.dumps(combined_data, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()


def generate_audit_report(output_path=None):
    """Generate complete audit report."""
    print("Collecting hardware information...")
    hardware_info = get_hardware_info()
    
    print("Scanning installed packages...")
    packages = get_installed_packages()
    
    print("Computing environment hash...")
    env_hash = compute_environment_hash(hardware_info, packages)
    
    report = {
        "audit_timestamp": datetime.now().isoformat(),
        "environment_hash": env_hash,
        "hardware": hardware_info,
        "packages": packages,
    }
    
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Audit report saved to: {output_file}")
    else:
        print("\n" + "="*60)
        print("HARDWARE & DEPENDENCY AUDIT REPORT")
        print("="*60)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate hardware and dependency audit")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()
    
    generate_audit_report(args.output)
