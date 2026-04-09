from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    src_dir = repo_root / "src"
    sys.path.insert(0, str(src_dir))

    from spec_validator.architecture_validator import main as validator_main

    return validator_main()


if __name__ == "__main__":
    raise SystemExit(main())
