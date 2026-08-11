"""Command-line entry point."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from .client import create_deepseek_client
from .core import ReviewerConfig, review_pdf, write_outputs


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Review a paper with five independent DeepSeek V4 Flash reviewers "
            "and one Area Chair meta-review."
        )
    )
    parser.add_argument("pdf", type=Path, help="PDF manuscript to review")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: outputs/<paper>-<timestamp>)",
    )
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--base-url", default="https://api.deepseek.com")
    parser.add_argument("--ensemble-size", type=int, default=5)
    parser.add_argument("--parallelism", type=int, default=5)
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "minimal", "low", "medium", "high", "max"),
        default="max",
    )
    parser.add_argument("--max-output-tokens", type=int, default=16384)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument(
        "--aggregate-scores",
        choices=("meta", "mean"),
        default="meta",
        help=(
            "meta preserves all Area Chair scores (Nature-style); mean overwrites only "
            "numeric scores with rounded independent-review means (legacy repo behavior)"
        ),
    )
    parser.add_argument("--cache-hit-price", type=float, default=0.0028)
    parser.add_argument("--cache-miss-price", type=float, default=0.14)
    parser.add_argument("--output-price", type=float, default=0.28)
    return parser


def main(argv=None) -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    args = build_parser().parse_args(argv)
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print(
            "DEEPSEEK_API_KEY is not available. Copy .env.example to .env, add the key "
            "locally, and do not paste or commit it.",
            file=sys.stderr,
        )
        return 2

    pdf_path = args.pdf.expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = args.output_dir or PROJECT_ROOT / "outputs" / f"{pdf_path.stem}-{timestamp}"
    config = ReviewerConfig(
        model=args.model,
        base_url=args.base_url,
        ensemble_size=args.ensemble_size,
        parallelism=args.parallelism,
        reasoning_effort=args.reasoning_effort,
        max_output_tokens=args.max_output_tokens,
        max_attempts=args.max_attempts,
        aggregate_scores=args.aggregate_scores,
        cache_hit_usd_per_million=args.cache_hit_price,
        cache_miss_usd_per_million=args.cache_miss_price,
        output_usd_per_million=args.output_price,
    )
    client = create_deepseek_client(api_key=api_key, base_url=config.base_url)

    try:
        bundle = review_pdf(pdf_path, client=client, config=config)
        json_path, markdown_path = write_outputs(bundle, output_dir)
    except Exception as exc:
        print(f"AutoReviewer failed: {exc}", file=sys.stderr)
        return 1

    final = bundle["final_review"]
    print(f"Decision: {final['Decision']}")
    print(f"Overall: {final['Overall']}/10")
    print(f"Estimated API cost: ${bundle['estimated_cost_usd']['total_usd']:.8f}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
