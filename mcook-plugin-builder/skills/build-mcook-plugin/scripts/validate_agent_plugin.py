# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema==4.26.0"]
# ///

"""Validate an Agent Plugins 1.0.0 package and local or pinned Git marketplace entries."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator

PLUGIN_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
SCHEMA_DIR = Path(__file__).resolve().parent.parent / "references" / "schemas" / "1.0.0"
HTTP_TOKEN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
SECRET_HEADERS = {
    "authorization",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "api-key",
}
SECRET_ENV = re.compile(
    r"(?:^|_)(?:TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|PRIVATE_KEY|CREDENTIALS?)(?:$|_)"
)


def load_json(path: Path, errors: list[str]) -> Any | None:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
    return None


def schema_errors(document: Any, schema_path: Path, label: str) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    failures = sorted(
        validator.iter_errors(document),
        key=lambda item: [str(part) for part in item.absolute_path],
    )
    result: list[str] = []
    for failure in failures:
        location = "$"
        for part in failure.absolute_path:
            location += f"[{part}]" if isinstance(part, int) else f".{part}"
        result.append(f"{label} {location}: {failure.message}")
    return result


def suffix_is_contained(value: str) -> bool:
    if "\\" in value:
        return False
    depth = 0
    for part in value.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            depth -= 1
            if depth < 0:
                return False
        else:
            depth += 1
    return True


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def validate_package_paths(root: Path, errors: list[str], warnings: list[str]) -> None:
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(
                f"Codex-compatible portable packages cannot contain symlinks: {path}"
            )

    skills = root / "skills"
    if not skills.exists():
        return
    if not skills.is_dir():
        errors.append("skills must be a directory when present")
        return
    if not is_within(skills, root):
        errors.append("skills resolves outside the plugin root")
        return

    discovered: set[Path] = set()
    for child in skills.iterdir():
        skill_file = child / "SKILL.md"
        if child.is_dir() and skill_file.exists():
            discovered.add(skill_file.resolve())
            if not skill_file.is_file():
                errors.append(f"discovered skill is not a regular file: {skill_file}")
            elif not is_within(skill_file, root):
                errors.append(
                    f"discovered skill resolves outside the plugin root: {skill_file}"
                )

    for skill_file in skills.rglob("SKILL.md"):
        if skill_file.resolve() not in discovered:
            warnings.append(
                f"nested SKILL.md is not discovered by Agent Plugins: {skill_file}"
            )


def validate_stdio(
    name: str,
    server: dict[str, Any],
    root: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    command = server.get("command")
    if not isinstance(command, str):
        return
    if command.startswith("./"):
        suffix = command[2:]
        if not suffix or not suffix_is_contained(suffix):
            errors.append(
                f"mcpServers.{name}.command is not a contained portable path: {command}"
            )
        else:
            target = root.joinpath(
                *[part for part in suffix.split("/") if part not in ("", ".")]
            )
            if not is_within(target, root):
                errors.append(
                    f"mcpServers.{name}.command resolves outside the plugin root: {command}"
                )
            elif not target.is_file():
                errors.append(
                    f"mcpServers.{name}.command does not name a bundled file: {command}"
                )
    elif (
        "/" in command
        or "\\" in command
        or command != command.strip()
        or any(char.isspace() for char in command)
    ):
        errors.append(
            f"mcpServers.{name}.command must be one bare executable token or start with './': {command!r}"
        )

    cwd = server.get("cwd")
    if isinstance(cwd, str):
        if cwd.startswith("./"):
            suffix = cwd[2:]
        elif cwd == "${PLUGIN_ROOT}":
            suffix = ""
        elif cwd.startswith("${PLUGIN_ROOT}/"):
            suffix = cwd[len("${PLUGIN_ROOT}/") :]
        elif cwd == "${PLUGIN_DATA}":
            suffix = ""
        elif cwd.startswith("${PLUGIN_DATA}/"):
            suffix = cwd[len("${PLUGIN_DATA}/") :]
        else:
            suffix = "../invalid"
        if not suffix_is_contained(suffix):
            errors.append(f"mcpServers.{name}.cwd is not contained: {cwd}")

    env = server.get("env")
    if not isinstance(env, dict):
        return
    for key, value in env.items():
        if isinstance(key, str) and key.casefold() in {"plugin_root", "plugin_data"}:
            errors.append(
                f"mcpServers.{name}.env cannot override reserved variable {key}"
            )
        if (
            isinstance(key, str)
            and isinstance(value, str)
            and SECRET_ENV.search(key.upper())
            and not key.upper().endswith(("_FILE", "_PATH"))
        ):
            warnings.append(
                f"mcpServers.{name}.env.{key} looks credential-bearing; package config must not contain secrets"
            )


def is_loopback(host: str | None) -> bool:
    if host == "localhost":
        return True
    if host is None:
        return False
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def validate_remote(name: str, server: dict[str, Any], errors: list[str]) -> None:
    value = server.get("url")
    if not isinstance(value, str):
        return
    try:
        parsed = urlsplit(value)
        _ = parsed.port
    except ValueError as exc:
        errors.append(f"mcpServers.{name}.url is invalid: {exc}")
        return
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        errors.append(f"mcpServers.{name}.url must be an absolute HTTP or HTTPS URL")
    if parsed.username is not None or parsed.password is not None:
        errors.append(f"mcpServers.{name}.url must not contain user information")
    if parsed.fragment:
        errors.append(f"mcpServers.{name}.url must not contain a fragment")
    if parsed.scheme == "http" and not is_loopback(parsed.hostname):
        errors.append(
            f"mcpServers.{name}.url must use HTTPS for non-loopback endpoints"
        )

    seen: set[str] = set()
    headers = server.get("headers")
    if not isinstance(headers, dict):
        return
    for key, header_value in headers.items():
        normalized = key.casefold() if isinstance(key, str) else ""
        if not isinstance(key, str) or not HTTP_TOKEN.fullmatch(key):
            errors.append(
                f"mcpServers.{name}.headers contains an invalid HTTP field name: {key!r}"
            )
        if normalized in seen:
            errors.append(
                f"mcpServers.{name}.headers repeats {key!r} with different casing"
            )
        seen.add(normalized)
        if normalized in SECRET_HEADERS:
            errors.append(
                f"mcpServers.{name}.headers.{key} is credential-bearing package data"
            )
        if isinstance(header_value, str) and (
            "\r" in header_value or "\n" in header_value
        ):
            errors.append(f"mcpServers.{name}.headers.{key} contains a line break")


def validate_mcp(
    document: Any, root: Path, errors: list[str], warnings: list[str]
) -> None:
    if not isinstance(document, dict):
        return
    servers = document.get("mcpServers")
    if not isinstance(servers, dict):
        return
    for name, server in servers.items():
        if not isinstance(server, dict):
            continue
        server_type = server.get("type")
        if server_type == "stdio":
            validate_stdio(str(name), server, root, errors, warnings)
        elif server_type in {"streamable-http", "sse"}:
            validate_remote(str(name), server, errors)
            if server_type == "sse":
                warnings.append(
                    f"mcpServers.{name} uses the deprecated HTTP+SSE transport"
                )


def validate_openai_overlay(
    root: Path, portable_manifest: Any, errors: list[str]
) -> None:
    path = root / ".codex-plugin" / "plugin.json"
    overlay = load_json(path, errors)
    if not isinstance(overlay, dict) or not isinstance(portable_manifest, dict):
        return
    for field in ("name", "version"):
        if overlay.get(field) != portable_manifest.get(field):
            errors.append(
                f"OpenAI overlay {field!r} must match root plugin.json: "
                f"{overlay.get(field)!r} != {portable_manifest.get(field)!r}"
            )


def safe_subdir(value: Any) -> bool:
    """Reject traversal and platform-dependent path syntax before resolution."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "%" in value:
        return False
    path = value[2:] if value.startswith("./") else value
    return bool(path) and all(
        part not in {"", ".", ".."} and not any(ord(c) < 32 for c in part)
        for part in path.split("/")
    )


def validate_marketplace(
    path: Path,
    marketplace_root: Path,
    plugin_root: Path | None,
    plugin_name: str | None,
    errors: list[str],
) -> None:
    document = load_json(path, errors)
    if not isinstance(document, dict) or not isinstance(document.get("plugins"), list):
        errors.append(f"marketplace must contain a plugins array: {path}")
        return
    matches = [
        entry
        for entry in document["plugins"]
        if isinstance(entry, dict) and entry.get("name") == plugin_name
    ]
    if len(matches) != 1:
        errors.append(
            f"marketplace must contain exactly one entry for {plugin_name!r}; found {len(matches)}"
        )
        return
    source = matches[0].get("source")
    label = f"marketplace entry for {plugin_name!r}"
    if not isinstance(source, dict):
        errors.append(f"{label} must contain a source object")
    elif source.get("source") == "local":
        value = source.get("path")
        if not safe_subdir(value) or not value.startswith("./"):
            errors.append(f"{label} must use a contained relative ./ local path")
        else:
            source_path = (marketplace_root / value).resolve()
            if not is_within(source_path, marketplace_root):
                errors.append(f"{label} local path escapes marketplace root")
            elif plugin_root is not None and source_path != plugin_root.resolve():
                errors.append(f"{label} local path does not match plugin root")
    elif source.get("source") in {"git-subdir", "url"}:
        # Metadata only: never fetch a repository or execute package contents.
        value = source.get("url")
        try:
            parsed = urlsplit(value) if isinstance(value, str) else None
            valid_url = bool(
                parsed and parsed.scheme == "https" and parsed.hostname == "github.com"
                and not parsed.username and not parsed.password
                and not parsed.query and not parsed.fragment and parsed.port is None
                and re.fullmatch(r"/[A-Za-z0-9_-][A-Za-z0-9_.-]*/[A-Za-z0-9_-][A-Za-z0-9_.-]*(?:\.git)?", parsed.path)
                and not any(c.isspace() or ord(c) < 32 for c in value)
            )
        except ValueError:
            valid_url = False
        if not valid_url:
            errors.append(f"{label} requires a credential-free HTTPS GitHub repository URL")
        selectors = [source[key] for key in ("ref", "sha") if key in source]
        if len(selectors) != 1 or not isinstance(selectors[0], str) or not re.fullmatch(r"[0-9a-fA-F]{40}", selectors[0]):
            errors.append(f"{label} requires exactly one full 40-character commit ref or sha")
        if source["source"] == "git-subdir" and not safe_subdir(source.get("path")):
            errors.append(f"{label} requires a safe relative Git subdirectory")
        if source["source"] == "url" and "path" in source:
            errors.append(f"{label} root Git source must not contain a path")
        if plugin_root is not None:
            errors.append(f"{label} is external; use --marketplace-entry for metadata validation and separately verify pinned installed bytes")
    else:
        errors.append(f"{label} source must be local, git-subdir, or url")
    policy = matches[0].get("policy")
    if not isinstance(policy, dict):
        errors.append(f"marketplace entry for {plugin_name!r} must contain policy")
    else:
        if policy.get("installation") not in {
            "NOT_AVAILABLE",
            "AVAILABLE",
            "INSTALLED_BY_DEFAULT",
        }:
            errors.append(
                f"marketplace entry for {plugin_name!r} has invalid policy.installation"
            )
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            errors.append(
                f"marketplace entry for {plugin_name!r} has invalid policy.authentication"
            )
    if not isinstance(matches[0].get("category"), str) or not matches[0]["category"]:
        errors.append(f"marketplace entry for {plugin_name!r} must contain category")


def directory_matches_manifest(root: Path, manifest: dict[str, Any]) -> bool:
    name = manifest.get("name")
    version = manifest.get("version")
    return root.name == name or (
        root.parent.name == name and root.name == version
    )


def validate(
    plugin_root: Path,
    *,
    marketplace: Path | None = None,
    marketplace_root: Path | None = None,
    require_openai_overlay: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    root = plugin_root.resolve()
    if not root.is_dir():
        return [f"plugin root is not a directory: {plugin_root}"], warnings

    manifest_path = root / "plugin.json"
    manifest = load_json(manifest_path, errors)
    if manifest is not None:
        errors.extend(
            schema_errors(manifest, SCHEMA_DIR / "plugin.schema.json", "plugin.json")
        )
        if isinstance(manifest, dict) and not directory_matches_manifest(root, manifest):
            errors.append(
                "plugin path must end in the plugin name or the installed-cache "
                f"layout <name>/<version>: {root}"
            )

    mcp_path = root / "mcp.json"
    if mcp_path.exists():
        mcp = load_json(mcp_path, errors)
        if mcp is not None:
            errors.extend(
                schema_errors(mcp, SCHEMA_DIR / "mcp.schema.json", "mcp.json")
            )
            validate_mcp(mcp, root, errors, warnings)

    validate_package_paths(root, errors, warnings)
    if require_openai_overlay:
        validate_openai_overlay(root, manifest, errors)
    if marketplace is not None:
        name = manifest.get("name") if isinstance(manifest, dict) else None
        validate_marketplace(
            marketplace.resolve(),
            (marketplace_root or Path.cwd()).resolve(),
            root,
            name if isinstance(name, str) else None,
            errors,
        )
    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_root", type=Path, nargs="?")
    parser.add_argument("--marketplace-entry", help="validate only named catalog entry metadata; does not fetch or validate an external package")
    parser.add_argument("--marketplace", type=Path)
    parser.add_argument(
        "--marketplace-root",
        type=Path,
        default=Path.cwd(),
        help="base directory used to resolve local marketplace source paths (default: current directory)",
    )
    parser.add_argument(
        "--require-openai-overlay",
        action="store_true",
        help="require .codex-plugin/plugin.json and matching name/version",
    )
    args = parser.parse_args()
    if args.marketplace_entry:
        if args.plugin_root or not args.marketplace or args.require_openai_overlay:
            parser.error("--marketplace-entry requires --marketplace and cannot be combined with plugin_root or --require-openai-overlay")
    elif args.plugin_root is None:
        parser.error("plugin_root or --marketplace-entry is required")
    return args


def main() -> int:
    args = parse_args()
    if args.marketplace_entry:
        errors, warnings = [], []
        validate_marketplace(args.marketplace, args.marketplace_root.resolve(), None, args.marketplace_entry, errors)
        result = f"marketplace entry {args.marketplace_entry} (metadata only)"
    else:
        errors, warnings = validate(
            args.plugin_root,
            marketplace=args.marketplace,
            marketplace_root=args.marketplace_root,
            require_openai_overlay=args.require_openai_overlay,
        )
        result = f"Agent Plugins 1.0.0 package {args.plugin_root}"
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(
            f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"OK: {result} ({len(warnings)} warning(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
