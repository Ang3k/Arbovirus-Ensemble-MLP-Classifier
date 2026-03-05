"""
Extract CBO occupation codes from the Anexo-A-do-instrutivo.pdf
and generate src/data_processing/cbo_map.py.

Usage:
    python scripts/extract_cbo_from_pdf.py <path_to_pdf>

If no path is given, defaults to ~/Downloads/Anexo-A-do-instrutivo.pdf
"""
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is required. Install with: pip install pdfplumber")
    sys.exit(1)


def extract_cbo_entries(pdf_path):
    """Extract (code, description) pairs from CBO PDF."""
    entries = {}
    # Pattern: 6-digit code followed by description text
    pattern = re.compile(r'(\d{6})\s+(.+)')

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split('\n'):
                line = line.strip()
                match = pattern.match(line)
                if match:
                    code = int(match.group(1))
                    desc = match.group(2).strip().upper()
                    # Skip header lines that look like codes but aren't
                    if desc and not desc.startswith('CODIGO') and not desc.startswith('CBO'):
                        entries[desc] = code

    return entries


def write_cbo_map(entries, output_path):
    """Write CBO_MAP dict to a Python file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('CBO (Classificação Brasileira de Ocupações) codes.\n')
        f.write('Auto-generated from Anexo-A-do-instrutivo.pdf\n')
        f.write('"""\n\n')
        f.write('CBO_MAP = {\n')
        for desc, code in sorted(entries.items(), key=lambda x: x[1]):
            # Escape single quotes in descriptions
            desc_escaped = desc.replace("'", "\\'")
            f.write(f"    '{desc_escaped}': {code},\n")
        f.write('}\n')


def main():
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
    else:
        pdf_path = Path.home() / 'Downloads' / 'Anexo-A-do-instrutivo.pdf'

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        sys.exit(1)

    output_path = Path(__file__).resolve().parents[1] / 'src' / 'data_processing' / 'cbo_map.py'

    print(f"Extracting CBO codes from: {pdf_path}")
    entries = extract_cbo_entries(pdf_path)
    print(f"Found {len(entries)} unique CBO entries")

    write_cbo_map(entries, output_path)
    print(f"Written to: {output_path}")


if __name__ == '__main__':
    main()
