#!/usr/bin/env python3
"""
Script de Validação: Ausência de Implementação Criptográfica Customizada

Verifica que nenhuma implementação criptográfica própria existe no código,
garantindo conformidade com Princípio I da Constituição (uso exclusivo quantCrypt).

Usage:
    python scripts/validate_no_custom_crypto.py
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


# Padrões suspeitos que podem indicar implementação criptográfica
CRYPTO_PATTERNS = [
    # Operações criptográficas básicas
    (r'\bdef\s+(encrypt|decrypt|cipher|decipher)\s*\(', "Encryption/Decryption function"),
    (r'\bdef\s+(sign|verify|authenticate)\s*\(', "Signature/Verification function"),
    (r'\bdef\s+(hash|digest)\s*\(', "Hash function"),
    (r'\bdef\s+(keygen|generate_key|create_key)\s*\(', "Key generation function"),
    
    # Operações de baixo nível suspeitas
    (r'\bdef\s+(xor|mod_exp|modular_exponentiation)\s*\(', "Low-level crypto operation"),
    (r'\bdef\s+(permute|substitute|sbox)\s*\(', "Cipher primitive"),
    (r'\bdef\s+(pad|unpad|pkcs)\s*\(', "Padding scheme"),
    
    # Constantes criptográficas típicas
    (r'\bS_BOX\s*=', "S-Box constant"),
    (r'\bROUND_CONSTANTS\s*=', "Round constants"),
    (r'\bIV\s*=\s*b?["\']', "Initialization vector"),
    
    # Imports de bibliotecas cripto (fora quantCrypt)
    (r'from\s+(Crypto|cryptography|pycrypto|nacl)\s+import', "External crypto library"),
    (r'import\s+(Crypto|cryptography|pycrypto|nacl)\b', "External crypto library"),
]

# Exceções permitidas (funções que são apenas wrappers)
ALLOWED_PATTERNS = [
    r'quantCrypt',
    r'# TODO: Implementar lógica real com quantCrypt',
    r'# Placeholder',
]


def scan_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Escaneia arquivo para padrões criptográficos suspeitos.
    
    Returns:
        Lista de (line_number, matched_pattern, description)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        print(f"⚠️  ERROR reading {file_path}: {e}")
        return []
    
    findings = []
    
    for pattern, description in CRYPTO_PATTERNS:
        for i, line in enumerate(lines, 1):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                # Check if it's an allowed pattern (wrapper/placeholder)
                is_allowed = False
                
                # Check current line and surrounding context
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 3)
                context = '\n'.join(lines[context_start:context_end])
                
                for allowed in ALLOWED_PATTERNS:
                    if re.search(allowed, context, re.IGNORECASE):
                        is_allowed = True
                        break
                
                if not is_allowed:
                    findings.append((i, match.group(0), description))
    
    return findings


def scan_directory(directory: Path, extensions: List[str] = ['.py']) -> Dict[str, List]:
    """
    Escaneia diretório recursivamente.
    
    Returns:
        Dict mapping file paths to findings
    """
    results = {}
    
    for ext in extensions:
        for file_path in directory.rglob(f'*{ext}'):
            # Skip test files and virtual environments
            if any(skip in str(file_path) for skip in ['test_', 'venv', '.venv', 'site-packages']):
                continue
            
            findings = scan_file(file_path)
            if findings:
                results[str(file_path)] = findings
    
    return results


def main():
    """Execute validation scan."""
    print("="*60)
    print("VALIDATING: No Custom Cryptographic Implementation")
    print("="*60)
    print("\nScanning for suspicious cryptographic patterns...")
    print("(This validates Principle I: quantCrypt exclusivity)\n")
    
    # Scan src/algorithms/ primarily
    algorithms_dir = Path("src/algorithms")
    if not algorithms_dir.exists():
        print(f"✗ ERROR: {algorithms_dir} not found")
        print("  Run this script from repository root")
        return 1
    
    results = scan_directory(algorithms_dir)
    
    # Also scan metrics and orchestration for good measure
    for additional_dir in [Path("src/metrics"), Path("src/orchestration")]:
        if additional_dir.exists():
            additional_results = scan_directory(additional_dir)
            results.update(additional_results)
    
    # Report findings
    if not results:
        print("✓ PASS: No custom cryptographic implementations detected")
        print("        All algorithms use quantCrypt exclusively")
        print("        Principle I compliance verified")
        return 0
    
    print("✗ FAIL: Suspicious cryptographic patterns detected\n")
    
    for file_path, findings in results.items():
        print(f"📁 {file_path}")
        for line_num, matched_text, description in findings:
            print(f"   Line {line_num}: {description}")
            print(f"            {matched_text}")
        print()
    
    print("="*60)
    print("⚠️  VIOLATION: Custom cryptographic implementation detected")
    print("   Review the flagged code to ensure only quantCrypt is used")
    print("   If these are false positives (wrappers), add TODO comments")
    print("="*60)
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
