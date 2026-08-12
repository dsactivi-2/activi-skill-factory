#!/usr/bin/env python3
"""ActiVi Skill Factory — local + CI gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("pyyaml required: python3 -m pip install pyyaml jsonschema\n")
    raise

try:
    import jsonschema
except ImportError:  # pragma: no cover
    sys.stderr.write("jsonschema required: python3 -m pip install pyyaml jsonschema\n")
    raise

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SCHEMAS = ROOT / "schemas"
POLICIES = ROOT / "policies"
EVALS = ROOT / "evals" / "golden"
DIST = ROOT / "dist"

SECRET_PATTERNS = [
    re.compile("-----" + "BEGIN OPENSSH PRIVATE KEY" + "-----"),
    re.compile("-----" + "BEGIN RSA PRIVATE KEY" + "-----"),
    re.compile("-----" + "BEGIN PGP PRIVATE KEY BLOCK" + "-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]
PLACEHOLDERS = ("YOUR_TOKEN_HERE", "changeme", "pending", "x-access-token")

SKIP_SCAN = {
    ".git",
    "dist",
    ".artifacts",
    "__pycache__",
    ".venv",
    "node_modules",
}
SKIP_SCAN_FILES = {"ci/asf.py"}

REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "skillspec.yaml",
    "skill-manifest.yaml",
    "CHANGELOG.md",
)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schema(name: str) -> dict:
    with (SCHEMAS / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def iter_skills() -> list[Path]:
    if not SKILLS.exists():
        return []
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "skillspec.yaml").exists())


def read_freeze() -> dict:
    data = load_yaml(POLICIES / "freeze.yaml") or {}
    for key in (
        "build_freeze",
        "release_freeze",
        "deployment_freeze",
        "source_discovery_freeze",
    ):
        if key not in data:
            fail(f"policies/freeze.yaml missing {key}")
        if not isinstance(data[key], bool):
            fail(f"policies/freeze.yaml {key} must be boolean")
    return data


def cmd_validate(_: argparse.Namespace) -> None:
    freeze = read_freeze()
    if freeze["build_freeze"]:
        fail(f"build_freeze is true ({freeze.get('reason') or 'no reason'})")

    spec_schema = load_schema("skillspec.schema.json")
    man_schema = load_schema("release-manifest.schema.json")
    ev_schema = load_schema("evidence.schema.json")
    src_schema = load_schema("source-record.schema.json")

    skills = iter_skills()
    if not skills:
        fail("no skills found under skills/")

    for skill_dir in skills:
        for name in REQUIRED_SKILL_FILES:
            if not (skill_dir / name).is_file():
                fail(f"{skill_dir.name}: missing {name}")
        spec = load_yaml(skill_dir / "skillspec.yaml")
        man = load_yaml(skill_dir / "skill-manifest.yaml")
        jsonschema.validate(spec, spec_schema)
        jsonschema.validate(man, man_schema)
        if spec["skill_id"] != skill_dir.name:
            fail(f"{skill_dir.name}: skill_id {spec['skill_id']} != directory")
        if spec["skill_id"] != man["skill_id"]:
            fail(f"{skill_dir.name}: skillspec/manifest skill_id mismatch")
        if spec["version"] != man["version"]:
            fail(f"{skill_dir.name}: skillspec/manifest version mismatch")
        if man.get("artifact_sha256") not in (None, "pending") and not re.fullmatch(
            r"[a-f0-9]{64}", str(man.get("artifact_sha256"))
        ):
            fail(f"{skill_dir.name}: invalid artifact_sha256")
        skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        if spec["skill_id"] not in skill_md:
            fail(f"{skill_dir.name}: SKILL.md must mention skill_id")
        print(f"ok skill {skill_dir.name} {spec['version']} risk={man.get('risk')}")

    sources = load_yaml(ROOT / "sources" / "registry.yaml") or {}
    for rec in sources.get("sources") or []:
        jsonschema.validate(rec, src_schema)
    print(f"ok sources ({len(sources.get('sources') or [])})")

    ev_files = sorted((ROOT / "evidence").glob("ev_*.yaml"))
    for ev in ev_files:
        jsonschema.validate(load_yaml(ev), ev_schema)
    print(f"ok evidence ({len(ev_files)})")

    subs = load_yaml(ROOT / "registry" / "agent-subscriptions.yaml") or {}
    jsonschema.validate(subs, load_schema("agent-subscription.schema.json"))
    print("ok subscriptions")


def cmd_security(_: argparse.Namespace) -> None:
    read_freeze()
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_SCAN for part in path.parts):
            continue
        if str(path.relative_to(ROOT)).replace("\\", "/") in SKIP_SCAN_FILES:
            continue
        if path.suffix in {".png", ".jpg", ".jpeg", ".webp", ".zip", ".bundle", ".tgz"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            for match in pat.finditer(text):
                snippet = match.group(0)
                if any(p in snippet for p in PLACEHOLDERS):
                    continue
                # backup workflow uses a URL template, not a live token
                if "x-access-token:${" in text and pat.pattern.startswith("xox"):
                    continue
                rel = path.relative_to(ROOT)
                hits.append(f"{rel}: matched {pat.pattern}")
    if hits:
        fail("secret-like patterns:\n  " + "\n  ".join(hits))
    print("ok security scan")


def cmd_evals(_: argparse.Namespace) -> None:
    freeze = read_freeze()
    if freeze["build_freeze"]:
        fail("build_freeze blocks evals")

    cases = 0
    for skill_dir in iter_skills():
        golden = EVALS / skill_dir.name / "cases.yaml"
        if not golden.is_file():
            fail(f"{skill_dir.name}: missing {golden.relative_to(ROOT)}")
        data = load_yaml(golden) or {}
        items = data.get("cases") or []
        if not items:
            fail(f"{skill_dir.name}: golden cases empty")
        spec = load_yaml(skill_dir / "skillspec.yaml")
        skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for case in items:
            cid = case.get("id") or "<no-id>"
            contains = case.get("skill_md_contains") or []
            for needle in contains:
                if needle not in skill_md:
                    fail(f"{skill_dir.name} {cid}: SKILL.md missing {needle!r}")
            forbidden = case.get("skill_md_forbids") or []
            for needle in forbidden:
                if needle.lower() in skill_md.lower():
                    fail(f"{skill_dir.name} {cid}: SKILL.md contains forbidden {needle!r}")
            if case.get("expect_skill_id") and case["expect_skill_id"] != spec["skill_id"]:
                fail(f"{skill_dir.name} {cid}: skill_id mismatch")
            cases += 1
        print(f"ok evals {skill_dir.name} ({len(items)} cases)")
    print(f"ok evals total {cases}")


def _zip_skill(skill_dir: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(skill_dir))
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    (dest.with_suffix(dest.suffix + ".sha256")).write_text(digest + "\n", encoding="utf-8")
    return digest


def cmd_package(ns: argparse.Namespace) -> None:
    freeze = read_freeze()
    if freeze["build_freeze"]:
        fail("build_freeze blocks package")
    out_root = Path("/tmp/asf-dry-run") if ns.dry_run else DIST
    if ns.dry_run and out_root.exists():
        shutil.rmtree(out_root)
    for skill_dir in iter_skills():
        spec = load_yaml(skill_dir / "skillspec.yaml")
        dest = out_root / spec["skill_id"] / f"{spec['skill_id']}-{spec['version']}.zip"
        digest = _zip_skill(skill_dir, dest)
        print(f"ok pack {dest.relative_to(out_root) if ns.dry_run else dest} sha256={digest}")
    if ns.dry_run:
        print("ok package dry-run")


def cmd_build_release(_: argparse.Namespace) -> None:
    freeze = read_freeze()
    if freeze["release_freeze"]:
        fail(f"release_freeze is true ({freeze.get('reason') or 'no reason'})")
    cmd_package(argparse.Namespace(dry_run=False))
    print("ok build-release")


def _existing_tags() -> set[str]:
    try:
        out = subprocess.check_output(
            ["git", "tag"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def cmd_publish(ns: argparse.Namespace) -> None:
    freeze = read_freeze()
    if freeze["release_freeze"]:
        fail("release_freeze blocks publish")

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "dsactivi-2/activi-skill-factory")
    sha = os.environ.get("GITHUB_SHA", "unknown")
    tags = _existing_tags()
    published = 0

    for skill_dir in iter_skills():
        spec = load_yaml(skill_dir / "skillspec.yaml")
        man = load_yaml(skill_dir / "skill-manifest.yaml")
        tag = f"{spec['skill_id']}/v{spec['version']}"
        artifact = DIST / spec["skill_id"] / f"{spec['skill_id']}-{spec['version']}.zip"
        if not artifact.is_file():
            fail(f"missing artifact {artifact}")
        digest = artifact.with_suffix(".zip.sha256").read_text(encoding="utf-8").strip()
        if tag in tags:
            print(f"skip existing tag {tag}")
            continue
        if not token:
            print(f"skip publish {tag} (no GH_TOKEN)")
            continue
        notes = (
            f"skill={spec['skill_id']}\n"
            f"version={spec['version']}\n"
            f"risk={man.get('risk')}\n"
            f"channel={man.get('channel')}\n"
            f"sha256={digest}\n"
            f"commit={sha}\n"
        )
        subprocess.check_call(
            [
                "gh",
                "release",
                "create",
                tag,
                str(artifact),
                str(artifact) + ".sha256",
                "--title",
                tag,
                "--notes",
                notes,
                "--repo",
                repo,
            ]
        )
        published += 1
        print(f"ok release {tag}")

    print(f"ok publish ({published} new)")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("security")
    sub.add_parser("evals")
    p = sub.add_parser("package")
    p.add_argument("--dry-run", action="store_true")
    sub.add_parser("build-release")
    sub.add_parser("publish")
    ns = parser.parse_args()
    {
        "validate": cmd_validate,
        "security": cmd_security,
        "evals": cmd_evals,
        "package": cmd_package,
        "build-release": cmd_build_release,
        "publish": cmd_publish,
    }[ns.cmd](ns)


if __name__ == "__main__":
    main()
