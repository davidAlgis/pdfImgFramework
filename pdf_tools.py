import argparse
from pathlib import Path

from grayscale import convert_pdf_to_grayscale
from utils import str2bool


def main():
    parser = argparse.ArgumentParser(description="PDF tools")
    parser.add_argument("-i", "--input", required=True, help="Input PDF path")
    parser.add_argument("-o", "--output", help="Output PDF path")
    parser.add_argument(
        "-g",
        "--grayscale",
        type=str2bool,
        default=False,
        help="Convert to grayscale (true/false)",
    )

    args = parser.parse_args()

    in_path = Path(args.input)

    if args.grayscale:
        # If output not provided, append _grayscale before extension
        out_path = (
            Path(args.output)
            if args.output
            else in_path.with_name(f"{in_path.stem}_grayscale{in_path.suffix}")
        )
        result = convert_pdf_to_grayscale(str(in_path), str(out_path))
        print(f"Grayscale PDF written to: {result}")
    else:
        # Do nothing if grayscale is False
        print("No action taken (grayscale=False).")


if __name__ == "__main__":
    main()