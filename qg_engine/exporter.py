"""
Question & Answer Exporter Module.
Exports generated questions and answers to JSON or CSV formats.
"""

import json
import csv
from quest import parse as parse_factual
from blanks import generate_blanks_questions


def export_questions(input_text, output_path, file_format="json"):
    """
    Parses input text, generates factual and fill-in-the-blank questions,
    and exports them to JSON or CSV format.
    """
    factual_qs = parse_factual(input_text)
    blank_qs = generate_blanks_questions(input_text)

    records = []
    for idx, q in enumerate(factual_qs, 1):
        records.append({
            "id": idx,
            "type": "factual",
            "question": q,
            "options": [],
            "answer": ""
        })

    for idx, (q_text, choices, answer) in enumerate(blank_qs, len(records) + 1):
        records.append({
            "id": idx,
            "type": "fill-in-the-blank",
            "question": q_text,
            "options": choices,
            "answer": answer
        })

    file_format = file_format.lower()
    if file_format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    elif file_format == "csv":
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Question", "Options", "Answer"])
            for r in records:
                options_str = "; ".join(r["options"]) if r["options"] else ""
                writer.writerow([r["id"], r["type"], r["question"], options_str, r["answer"]])
    else:
        raise ValueError(f"Unsupported export format '{file_format}'. Use 'json' or 'csv'.")

    return len(records)
