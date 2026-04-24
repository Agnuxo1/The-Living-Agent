#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from living_agent_common import (
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_LIVING_AGENT_ROOT,
    ensure_module_runtime,
    normalize_whitespace,
    python_runtime,
    read_text,
    sha256_text,
    tokenize,
    write_json,
)


DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_WINDOW = 100
DEFAULT_EMBEDDING_DIM = 384

ensure_module_runtime("sentence_transformers")


def require_sentence_transformers():
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "sentence-transformers is not installed for the active interpreter.\n"
            f"Use {python_runtime()} -m pip install sentence-transformers"
        ) from exc
    return SentenceTransformer


@dataclass
class Archive:
    embeddings: np.ndarray
    entries: list[dict]


def encoder_embedding_dim(encoder: Encoder) -> int:
    return int(encoder.model.get_sentence_embedding_dimension())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Encoder:
    def __init__(self, model_name: str):
        SentenceTransformer = require_sentence_transformers()
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        arr = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.asarray(arr, dtype=np.float32)


def archive_paths(archive_dir: Path) -> tuple[Path, Path, Path]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    return (
        archive_dir / "paper_embeddings.npz",
        archive_dir / "paper_embeddings.json",
        archive_dir / "sns_model_info.json",
    )


def load_model_info(archive_dir: Path) -> dict | None:
    _, _, model_info_path = archive_paths(archive_dir)
    if not model_info_path.exists():
        return None
    return json.loads(model_info_path.read_text(encoding="utf-8"))


def load_archive(archive_dir: Path, *, embedding_dim: int | None = None) -> Archive:
    npz_path, json_path, _ = archive_paths(archive_dir)
    if not npz_path.exists() or not json_path.exists():
        dim = embedding_dim
        if dim is None:
            model_info = load_model_info(archive_dir)
            dim = int(model_info.get("embedding_dim", 0) or 0) if model_info else 0
        if dim <= 0:
            dim = DEFAULT_EMBEDDING_DIM
        return Archive(np.zeros((0, dim), dtype=np.float32), [])
    with np.load(npz_path) as payload:
        embeddings = np.asarray(payload["embeddings"], dtype=np.float32)
    entries = json.loads(json_path.read_text(encoding="utf-8"))
    return Archive(embeddings, entries)


def save_archive(
    archive_dir: Path,
    archive: Archive,
    *,
    model_name: str,
    embedding_dim: int,
) -> None:
    npz_path, json_path, model_info_path = archive_paths(archive_dir)
    np.savez_compressed(npz_path, embeddings=archive.embeddings)
    write_json(json_path, archive.entries)
    write_json(
        model_info_path,
        {
            "model_name": model_name,
            "embedding_dim": embedding_dim,
            "normalized": True,
            "archive_count": len(archive.entries),
            "updated_at": utc_now(),
        },
    )


def prepare_text(text: str) -> str:
    return normalize_whitespace(text)


def ensure_archive_compatibility(archive_dir: Path, encoder: Encoder) -> None:
    model_info = load_model_info(archive_dir)
    if not model_info:
        return
    archived_model = model_info.get("model_name")
    archived_dim = int(model_info.get("embedding_dim", 0) or 0)
    if archived_model and archived_model != encoder.model_name:
        raise SystemExit(
            "archive model mismatch: "
            f"{archive_dir} was built with {archived_model}, not {encoder.model_name}"
        )
    if archived_dim and archived_dim != int(encoder.model.get_sentence_embedding_dimension()):
        raise SystemExit(
            "archive embedding dimension mismatch: "
            f"{archive_dir} stores {archived_dim}, "
            f"but {encoder.model_name} returns "
            f"{encoder_embedding_dim(encoder)}"
        )


def score_text(
    text: str,
    *,
    archive_dir: Path,
    encoder: Encoder,
    window: int = DEFAULT_WINDOW,
    append: bool = False,
    metadata: dict | None = None,
    exclude_sha256: str | None = None,
) -> dict:
    cleaned = prepare_text(text)
    cleaned_sha = sha256_text(cleaned)
    ensure_archive_compatibility(archive_dir, encoder)
    archive = load_archive(archive_dir, embedding_dim=encoder_embedding_dim(encoder))
    embedding = encoder.encode([cleaned])[0]
    if len(archive.entries) == 0:
        novelty = 1.0
        max_similarity = 0.0
    else:
        candidate_indices = list(range(len(archive.entries)))
        if exclude_sha256:
            candidate_indices = [
                idx for idx, entry in enumerate(archive.entries) if entry.get("sha256") != exclude_sha256
            ]
        if candidate_indices:
            similarities = archive.embeddings[candidate_indices] @ embedding
            max_similarity = float(np.max(similarities))
            novelty = max(0.0, round(1.0 - max_similarity, 4))
        else:
            max_similarity = 0.0
            novelty = 1.0
    entry = {
        "sha256": cleaned_sha,
        "word_count": len(cleaned.split()),
        "token_count": len(tokenize(cleaned)),
        "preview": cleaned[:160],
    }
    if metadata:
        entry.update(metadata)
    if append:
        archive.entries.append(entry)
        archive.embeddings = (
            np.vstack([archive.embeddings, embedding[np.newaxis, :]])
            if archive.embeddings.size
            else embedding[np.newaxis, :]
        )
        archive.entries = archive.entries[-window:]
        archive.embeddings = archive.embeddings[-window:, :]
        save_archive(
            archive_dir,
            archive,
            model_name=encoder.model_name,
            embedding_dim=int(archive.embeddings.shape[1]),
        )
    return {
        "sns": novelty,
        "max_similarity": round(max_similarity, 4),
        "entry": entry,
    }


def calculate_sns(
    paper_text: str,
    archive_dir: str | Path,
    window: int = DEFAULT_WINDOW,
    *,
    model_name: str = DEFAULT_MODEL,
    encoder: Encoder | None = None,
) -> float:
    archive_root = Path(archive_dir)
    local_encoder = encoder or Encoder(model_name)
    payload = score_text(
        paper_text,
        archive_dir=archive_root,
        encoder=local_encoder,
        window=window,
        append=False,
    )
    return float(payload["sns"])


def bootstrap_archive(
    source_dir: Path,
    *,
    archive_dir: Path,
    encoder: Encoder,
    window: int,
) -> dict:
    files = sorted(source_dir.glob("paper_*.md"))
    accepted = []
    texts = []
    skipped = []
    for path in files:
        text = prepare_text(read_text(path))
        if len(text.split()) < 50 or text.startswith("ERROR: API offline"):
            skipped.append(path.name)
            continue
        accepted.append({"path": str(path), "sha256": sha256_text(text), "word_count": len(text.split())})
        texts.append(text)
    if texts:
        embeddings = encoder.encode(texts)
    else:
        embeddings = np.zeros((0, encoder_embedding_dim(encoder)), dtype=np.float32)
    archive = Archive(embeddings=embeddings[-window:], entries=accepted[-window:])
    dim = int(archive.embeddings.shape[1]) if archive.embeddings.size else encoder_embedding_dim(encoder)
    save_archive(archive_dir, archive, model_name=encoder.model_name, embedding_dim=dim)
    return {
        "source_count": len(files),
        "accepted_count": len(accepted),
        "skipped_count": len(skipped),
        "archive_count": len(archive.entries),
        "window": window,
        "model_name": encoder.model_name,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Living Agent embedding SNS utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    score = sub.add_parser("score")
    score.add_argument("--paper")
    score.add_argument("--paper-file")
    score.add_argument("--archive-dir", default=str(DEFAULT_ARTIFACT_ROOT))
    score.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    score.add_argument("--model", default=DEFAULT_MODEL)
    score.add_argument("--append", action="store_true")
    score.add_argument("--json", action="store_true")

    boot = sub.add_parser("bootstrap")
    boot.add_argument(
        "--source-dir",
        default=str(DEFAULT_LIVING_AGENT_ROOT / "memories" / "semantic"),
    )
    boot.add_argument("--archive-dir", default=str(DEFAULT_ARTIFACT_ROOT))
    boot.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    boot.add_argument("--model", default=DEFAULT_MODEL)
    boot.add_argument("--json", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    encoder = Encoder(args.model)
    if args.command == "score":
        if not args.paper and not args.paper_file:
            raise SystemExit("score requires --paper or --paper-file")
        text = args.paper or read_text(Path(args.paper_file))
        payload = score_text(
            text,
            archive_dir=Path(args.archive_dir),
            encoder=encoder,
            window=args.window,
            append=args.append,
            metadata={"paper_file": args.paper_file} if args.paper_file else None,
        )
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(payload["sns"])
        return 0
    if args.command == "bootstrap":
        payload = bootstrap_archive(
            Path(args.source_dir),
            archive_dir=Path(args.archive_dir),
            encoder=encoder,
            window=args.window,
        )
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(payload)
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
