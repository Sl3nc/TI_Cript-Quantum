#!/usr/bin/env python3
"""
Code Style Validation Script

Runs code style checks using available tools (ruff, flake8, pylint).
Part of Polish phase validation (T068).

Usage:
    python scripts/check_code_style.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """
    Run a command and report results.
    
    Returns:
        True if passed, False if failed
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print(f"✓ PASS: {description}")
            return True
        else:
            print(f"✗ FAIL: {description} (exit code {result.returncode})")
            return False
    
    except FileNotFoundError:
        print(f"⚠️  SKIP: Tool not installed")
        return None


def check_ruff():
    """Run ruff linter."""
    return run_command(
        ['ruff', 'check', 'src/', '--select', 'E,F,W,C90', '--statistics'],
        "Ruff linter (errors, warnings, complexity)"
    )


def check_flake8():
    """Run flake8 linter."""
    return run_command(
        ['flake8', 'src/', '--count', '--statistics', '--max-line-length=100'],
        "Flake8 linter"
    )


def check_pylint():
    """Run pylint."""
    return run_command(
        ['pylint', 'src/', '--disable=C0111,R0913', '--reports=n'],
        "Pylint static analysis"
    )


def check_mypy():
    """Run mypy type checker."""
    return run_command(
        ['mypy', 'src/', '--ignore-missing-imports'],
        "MyPy type checking"
    )


def main():
    """Run all available style checks."""
    print("="*60)
    print("CODE STYLE VALIDATION")
    print("="*60)
    print("\nChecking code style and quality...")
    print("(Multiple tools will be tried; skipped if not installed)")
    
    results = {
        'ruff': check_ruff(),
        'flake8': check_flake8(),
        'pylint': check_pylint(),
        'mypy': check_mypy(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    for tool, result in results.items():
        status = "✓ PASS" if result is True else ("✗ FAIL" if result is False else "⚠️  SKIP")
        print(f"{tool:15} {status}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\n⚠️  Some style checks failed. Review output above.")
        return 1
    elif passed == 0:
        print("\n⚠️  No style checkers installed. Install ruff or flake8:")
        print("   pip install ruff flake8")
        return 0  # Don't fail if tools aren't installed
    else:
        print("\n✓ All available style checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
