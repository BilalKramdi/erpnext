#!/usr/bin/env python3
"""Append entries from main.pot that are missing in fr.po."""

from __future__ import annotations

import argparse
from pathlib import Path

from list_missing_po import DEFAULT_PO, DEFAULT_POT, find_missing_entries


def append_missing_entries(pot_path: Path, po_path: Path) -> int:
	missing = find_missing_entries(pot_path, po_path)
	if not missing:
		return 0

	current = po_path.read_text(encoding="utf-8")
	separator = "" if current.endswith("\n\n") else "\n" if current.endswith("\n") else "\n\n"
	blocks = "\n\n".join("".join(entry.raw_lines).rstrip("\r\n") for entry in missing)
	po_path.write_text(current + separator + blocks + "\n", encoding="utf-8")
	return len(missing)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Ajoute à la fin de fr.po les chaînes absentes de main.pot."
	)
	parser.add_argument("--pot", type=Path, default=DEFAULT_POT, help="fichier POT source")
	parser.add_argument("--po", type=Path, default=DEFAULT_PO, help="fichier PO à compléter")
	args = parser.parse_args()

	count = append_missing_entries(args.pot, args.po)
	print(f"{count} entrée(s) ajoutée(s) à la fin de {args.po}.")


if __name__ == "__main__":
	main()
