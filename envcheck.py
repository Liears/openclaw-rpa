#!/usr/bin/env python3
"""Environment checks for Python + Playwright (import + Chromium)."""

from __future__ import annotations

import subprocess
import sys
from typing import Callable, Tuple

MIN_PYTHON = (3, 8)

CheckFn = Callable[[], Tuple[bool, str]]


def check_python() -> Tuple[bool, str]:
    if sys.version_info < MIN_PYTHON:
        return (
            False,
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required (found {sys.version_info.major}.{sys.version_info.minor})",
        )
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_playwright_import() -> Tuple[bool, str]:
    try:
        import playwright  # noqa: F401

        try:
            from importlib.metadata import version as pkg_version

            ver = pkg_version("playwright")
        except Exception:
            ver = getattr(playwright, "__version__", "?")
        return True, f"playwright package ({ver})"
    except ImportError:
        return False, "playwright package not installed"


def check_chromium_launch() -> Tuple[bool, str]:
    try:
        r = subprocess.run(
            [
                sys.executable,
                "-c",
                "from playwright.sync_api import sync_playwright;"
                "p=sync_playwright().start(); b=p.chromium.launch(headless=True);"
                "b.close(); p.stop()",
            ],
            capture_output=True,
            timeout=45,
        )
        if r.returncode == 0:
            return True, "Chromium launch (headless) OK"
        err = (r.stderr or b"").decode("utf-8", errors="replace").strip()
        out = (r.stdout or b"").decode("utf-8", errors="replace").strip()
        return False, err or out or "Chromium launch failed"
    except subprocess.TimeoutExpired:
        return False, "Chromium launch timed out"
    except Exception as e:
        return False, str(e)


def install_chromium() -> None:
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
    )


def ensure_playwright_chromium(*, auto_install: bool = True) -> int:
    """
    Verify Python, playwright import, and Chromium. Optionally install Chromium.
    Returns 0 on success, 1 on failure.
    """
    ok, msg = check_python()
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        return 1

    ok, msg = check_playwright_import()
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        print("   Install: pip install -r requirements.txt", file=sys.stderr)
        return 1

    ok, msg = check_chromium_launch()
    if ok:
        return 0

    if not auto_install:
        print(f"❌ Chromium: {msg}", file=sys.stderr)
        print(
            "   Fix: python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return 1

    print("⚙️  Playwright Chromium missing or broken; installing (about 1–2 minutes)…")
    try:
        install_chromium()
    except subprocess.CalledProcessError as e:
        print(f"❌ playwright install failed: {e}", file=sys.stderr)
        return 1

    ok, msg = check_chromium_launch()
    if not ok:
        print(f"❌ Chromium still not usable: {msg}", file=sys.stderr)
        return 1
    return 0


def print_report() -> int:
    """Print human-readable lines; exit code 0 if all OK, else 1."""
    lines: list[str] = []
    fatal = False

    ok, msg = check_python()
    lines.append(f"{'✅' if ok else '❌'} {msg}")
    if not ok:
        fatal = True

    ok, msg = check_playwright_import()
    lines.append(f"{'✅' if ok else '❌'} {msg}")
    if not ok:
        fatal = True

    if not fatal:
        ok, msg = check_chromium_launch()
        lines.append(f"{'✅' if ok else '❌'} {msg}")
        if not ok:
            fatal = True

    print("\n".join(lines))
    if fatal:
        print(
            "\nInstall (recommended):\n"
            "  ./scripts/install.sh\n"
            "Or: pip install -r requirements.txt && python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    return print_report()


if __name__ == "__main__":
    raise SystemExit(main())
