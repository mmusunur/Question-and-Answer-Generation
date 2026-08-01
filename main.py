"""
Unified Command Line Interface for Question and Answer Generation Engine.
"""

import sys
import argparse
from quest import parse as parse_factual
from blanks import generate_blanks_questions
from mcqs import run_quiz
from exporter import export_questions


def build_parser():
    parser = argparse.ArgumentParser(
        description="Automatic Question and Answer Generation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: quest
    quest_parser = subparsers.add_parser("quest", help="Generate factual questions (What, Who, Where, When)")
    quest_parser.add_argument("filename", nargs="?", default="in.txt", help="Input text file path")
    quest_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    # Command: blanks
    blanks_parser = subparsers.add_parser("blanks", help="Generate fill-in-the-blanks multiple-choice questions")
    blanks_parser.add_argument("filename", nargs="?", default="in.txt", help="Input text file path")

    # Command: quiz
    subparsers.add_parser("quiz", help="Run interactive Multiple-Choice Question quiz")

    # Command: export
    export_parser = subparsers.add_parser("export", help="Generate and export questions to JSON or CSV format")
    export_parser.add_argument("filename", nargs="?", default="in.txt", help="Input text file path")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export file format")
    export_parser.add_argument("--output", default="questions_output.json", help="Output file path")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "quest":
        try:
            with open(args.filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error opening '{args.filename}': {e}")
            sys.exit(1)

        questions = parse_factual(text)
        print(f"\nGenerated {len(questions)} Factual Questions:\n")
        for q in questions:
            print("Question:", q)

    elif args.command == "blanks":
        try:
            with open(args.filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error opening '{args.filename}': {e}")
            sys.exit(1)

        questions = generate_blanks_questions(text)
        print(f"\nGenerated {len(questions)} Fill-in-the-Blank Questions:\n")
        for idx, (q_text, choices, answer) in enumerate(questions, 1):
            print(f"{idx}: {q_text}")
            print("Possible answers are:")
            for c_idx, choice in enumerate(choices, 1):
                print(f"  {c_idx}: {choice}")
            print(f"Correct Answer: {answer}")
            print("\n" + "=" * 40 + "\n")

    elif args.command == "quiz":
        run_quiz()

    elif args.command == "export":
        try:
            with open(args.filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error opening '{args.filename}': {e}")
            sys.exit(1)

        output_path = args.output
        if args.format == "csv" and output_path == "questions_output.json":
            output_path = "questions_output.csv"

        count = export_questions(text, output_path, file_format=args.format)
        print(f"[SUCCESS] Exported {count} questions to '{output_path}' in {args.format.upper()} format!")


if __name__ == "__main__":
    main()
