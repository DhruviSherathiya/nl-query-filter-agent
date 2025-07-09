import json
import traceback
from difflib import SequenceMatcher
from app.agent import parse_query 


def load_dataset(path: str):
    with open(path, "r") as f:
        return json.load(f)

def fuzzy_score(pred: dict, expected: dict) -> float:
    return SequenceMatcher(
        None, json.dumps(pred, sort_keys=True), json.dumps(expected, sort_keys=True)
    ).ratio()


def evaluate(dataset, match_threshold=0.9):
    fuzzy, failed = 0, 0
    failed_cases = []

    for item in dataset:
        query = item["user_query"]
        expected = item["expected_filter"]

        try:
            predicted = parse_query(query)
        except Exception as e:
            print(f"[ERROR] Failed to parse: {query}\n{type(e).__name__}: {e}")
            traceback.print_exc()
            predicted = {}

        if fuzzy_score(predicted, expected) >= match_threshold:
            fuzzy += 1
        else:
            failed += 1
            print("--------------------------------")
            print(f"Failed: {query}")
            print(f"Expected: {expected}")
            print(f"Predicted: {predicted}")
            print("--------------------------------")
            failed_cases.append({
                "query": query,
                "expected": expected,
                "predicted": predicted
            })

    return {
        "total": len(dataset),
        "fuzzy": fuzzy,
        "failed": failed,
        "failures": failed_cases
    }


if __name__ == "__main__":
    path = "app/data/synthetic_eval_data.json"
    dataset = load_dataset(path)
    print(f"Loaded {len(dataset)} cases. Starting evaluation...")
    results = evaluate(dataset)

    print(f"\nEvaluation Results:")
    print(f"Total: {results['total']}")
    print(f"--------------------------------")
    print(f"Fuzzy Matches: {results['fuzzy']}")
    print(f"Failed: {results['failed']}")
    print(f"--------------------------------")

    if results["failures"]:
        print("\nSample Failure:")
        failure = results["failures"][0]
        print(f"Query: {failure['query']}")
        print(f"Expected: {json.dumps(failure['expected'], indent=2)}")
        print(f"Predicted: {json.dumps(failure['predicted'], indent=2)}")
