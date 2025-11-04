#!/usr/bin/env python3
"""
Script de Verificação de Neutralidade

Valida que ProfilerManager é usado de forma idêntica em todos os algoritmos,
garantindo comparabilidade das métricas (Princípio VII da Constituição).

Usage:
    python scripts/check_neutrality.py
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set


class ProfilerUsageExtractor(ast.NodeVisitor):
    """Extrai todas as chamadas ao ProfilerManager de um arquivo."""
    
    def __init__(self):
        self.profiler_calls: List[str] = []
        self.profiler_imports: List[str] = []
        
    def visit_ImportFrom(self, node):
        """Captura imports de ProfilerManager."""
        if node.module and 'metrics' in node.module:
            for alias in node.names:
                if 'ProfilerManager' in alias.name or alias.name == '*':
                    self.profiler_imports.append(f"from {node.module} import {alias.name}")
        self.generic_visit(node)
        
    def visit_Import(self, node):
        """Captura imports diretos."""
        for alias in node.names:
            if 'metrics' in alias.name:
                self.profiler_imports.append(f"import {alias.name}")
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Captura chamadas de métodos do ProfilerManager."""
        if isinstance(node.func, ast.Attribute):
            # Captura padrão: manager.start(), manager.stop(), etc.
            if hasattr(node.func.value, 'id'):
                call_pattern = f"{node.func.value.id}.{node.func.attr}()"
                self.profiler_calls.append(call_pattern)
        self.generic_visit(node)


def analyze_file(file_path: Path) -> Dict[str, any]:
    """
    Analisa um arquivo Python e extrai uso do ProfilerManager.
    
    Returns:
        Dict com imports, calls, e linha counts
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=str(file_path))
        extractor = ProfilerUsageExtractor()
        extractor.visit(tree)
        
        return {
            "file": file_path.name,
            "imports": extractor.profiler_imports,
            "calls": extractor.profiler_calls,
            "import_count": len(extractor.profiler_imports),
            "call_count": len(extractor.profiler_calls),
        }
    except Exception as e:
        return {
            "file": file_path.name,
            "error": str(e),
        }


def compare_usage(algorithms: List[Dict[str, any]]) -> bool:
    """
    Compara uso do ProfilerManager entre algoritmos.
    
    Returns:
        True se todos são idênticos, False caso contrário
    """
    if not algorithms:
        print("⚠️  WARNING: No algorithms to compare")
        return False
    
    # Extrair padrões de uso
    reference = algorithms[0]
    reference_calls = set(reference.get("calls", []))
    
    all_neutral = True
    
    print("\n" + "="*60)
    print("NEUTRALITY CHECK: ProfilerManager Usage")
    print("="*60)
    
    print(f"\n📋 Reference: {reference['file']}")
    print(f"   Imports: {reference.get('import_count', 0)}")
    print(f"   Calls: {reference.get('call_count', 0)}")
    if reference_calls:
        print(f"   Patterns: {', '.join(sorted(reference_calls))}")
    
    for algo in algorithms[1:]:
        algo_calls = set(algo.get("calls", []))
        
        print(f"\n📋 Comparing: {algo['file']}")
        print(f"   Imports: {algo.get('import_count', 0)}")
        print(f"   Calls: {algo.get('call_count', 0)}")
        if algo_calls:
            print(f"   Patterns: {', '.join(sorted(algo_calls))}")
        
        # Comparar padrões
        if algo_calls != reference_calls:
            all_neutral = False
            print(f"   ✗ MISMATCH with {reference['file']}")
            
            missing = reference_calls - algo_calls
            if missing:
                print(f"      Missing calls: {', '.join(missing)}")
            
            extra = algo_calls - reference_calls
            if extra:
                print(f"      Extra calls: {', '.join(extra)}")
        else:
            print(f"   ✓ MATCH with {reference['file']}")
    
    print("\n" + "="*60)
    if all_neutral:
        print("✓ PASS: All algorithms use ProfilerManager identically")
        print("        Metrics are comparable (Principle VII satisfied)")
    else:
        print("✗ FAIL: ProfilerManager usage differs between algorithms")
        print("        This violates neutrality requirement")
        print("        Review instrumentation to ensure identical profiling")
    print("="*60)
    
    return all_neutral


def main():
    """Execute neutrality verification."""
    algorithms_dir = Path("src/algorithms")
    
    if not algorithms_dir.exists():
        print(f"✗ ERROR: {algorithms_dir} not found")
        print("  Run this script from repository root")
        return 1
    
    # Analyze all algorithm files
    algorithm_files = list(algorithms_dir.glob("*.py"))
    algorithm_files = [f for f in algorithm_files if f.name != "__init__.py"]
    
    if not algorithm_files:
        print(f"✗ ERROR: No algorithm files found in {algorithms_dir}")
        return 1
    
    print(f"Scanning {len(algorithm_files)} algorithm files...")
    
    analyses = []
    for file_path in sorted(algorithm_files):
        print(f"  - {file_path.name}")
        analysis = analyze_file(file_path)
        
        if "error" in analysis:
            print(f"    ⚠️  Parse error: {analysis['error']}")
        else:
            analyses.append(analysis)
    
    # Compare usage patterns
    if not analyses:
        print("\n✗ ERROR: No files could be analyzed")
        return 1
    
    is_neutral = compare_usage(analyses)
    
    return 0 if is_neutral else 1


if __name__ == "__main__":
    sys.exit(main())
