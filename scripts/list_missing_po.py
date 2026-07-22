#!/usr/bin/env python3
"""List POT entries that are completely absent from a PO catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from translate_po import POEntry, parse_po


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POT = REPOSITORY_ROOT / "erpnext/locale/main.pot"
DEFAULT_PO = REPOSITORY_ROOT / "erpnext/locale/fr.po"


def active_entries(path: Path) -> list[POEntry]:
	_, entries = parse_po(path.read_text(encoding="utf-8"))
	return [entry for entry in entries if entry.msgid and not entry.obsolete]


def find_missing_entries(pot_path: Path, po_path: Path) -> list[POEntry]:
	po_keys = {entry.key for entry in active_entries(po_path)}
	return [entry for entry in active_entries(pot_path) if entry.key not in po_keys]


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Liste les chaînes de main.pot qui sont absentes de fr.po."
	)
	parser.add_argument("--pot", type=Path, default=DEFAULT_POT, help="fichier POT source")
	parser.add_argument("--po", type=Path, default=DEFAULT_PO, help="fichier PO à vérifier")
	args = parser.parse_args()

	missing = find_missing_entries(args.pot, args.po)
	for entry in missing:
		context = f" [contexte : {entry.msgctxt}]" if entry.msgctxt else ""
		print(f"- {json.dumps(entry.msgid, ensure_ascii=False)}{context}")

	print(f"\n{len(missing)} chaîne(s) de {args.pot.name} absente(s) de {args.po.name}.")


if __name__ == "__main__":
	main()
