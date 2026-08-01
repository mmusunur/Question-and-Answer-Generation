"""
Multiple-Choice Question (MCQ) Interactive Quiz System.
"""

import random
import sys


class QA:
    def __init__(self, question, correct_answer, other_answers):
        self.question = question
        self.corr_answ = correct_answer
        self.other_answ = other_answers


def sample_quiz():
    return [
        QA("Where is Minsk?", "in Belarus", ["in Russia", "such a city doesn't exist"]),
        QA("What is the capital of Australia?", "Canberra", ["Sydney", "New York", "Australia doesn't exist"]),
        QA("Which of the following is not on Earth?", "Sea of Tranquility", ["Mediterranean Sea", "Baltic Sea", "North Sea"]),
        QA("Which of the following is not a continent?", "Arctica", ["Antarctica", "America"]),
        QA("Which of the following is not an African country?", "Malaysia", ["Madagascar", "Djibouti", "South Africa", "Zimbabwe"]),
    ]


def run_quiz(qa_list=None):
    if qa_list is None:
        qa_list = sample_quiz()

    corr_count = 0
    random.shuffle(qa_list)

    print("\n" + "=" * 50)
    print("      MULTIPLE-CHOICE QUESTION QUIZ")
    print("=" * 50 + "\n")

    for idx, qa_item in enumerate(qa_list, 1):
        print(f"Question {idx}/{len(qa_list)}: {qa_item.question}")
        possible = list(qa_item.other_answ) + [qa_item.corr_answ]
        random.shuffle(possible)

        print("Possible answers:")
        for c_idx, option in enumerate(possible, 1):
            print(f"  {c_idx}: {option}")

        while True:
            try:
                user_answ = input("Please enter the number of your answer (or 'q' to quit): ").strip()
                if user_answ.lower() == 'q':
                    print("Quiz terminated by user.")
                    return
                choice_idx = int(user_answ)
                if 1 <= choice_idx <= len(possible):
                    selected_option = possible[choice_idx - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(possible)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if selected_option == qa_item.corr_answ:
            print("✔ Your answer was CORRECT!\n")
            corr_count += 1
        else:
            print(f"✘ Your answer was WRONG. Correct answer was: {qa_item.corr_answ}\n")

    print("=" * 50)
    print(f"Quiz Completed! Score: {corr_count} of {len(qa_list)} correct ({(corr_count / len(qa_list)) * 100:.1f}%).")
    print("=" * 50)


if __name__ == "__main__":
    run_quiz()
