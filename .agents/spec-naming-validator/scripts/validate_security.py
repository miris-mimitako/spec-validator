from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    src_dir = repo_root / "src"
    sys.path.insert(0, str(src_dir))

    from spec_validator.security_validator import main as validator_main

    if "--rules" not in sys.argv:
        sys.argv[1:1] = [
            "--rules",
            str(repo_root / "_docs" / "_GroundRules" / "40_security-rules-typescript.yaml"),
        ]
    return validator_main()


if __name__ == "__main__":
    raise SystemExit(main())
