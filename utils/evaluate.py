import statistics

def evaluate(predicted_mapping: dict[int, list[int]],
             ground_truth: dict[int, list[int]]) -> dict[str, float]:
    """
    Compare predicted mapping vs ground truth and compute precision/recall/F1.
    """

    predicted_set = set(predicted_mapping.keys())
    ground_set = set(ground_truth.keys())

    mismatch_set = set()
    TP = 0
    FP = len(predicted_set - ground_set)
    FN = len(ground_set - predicted_set)

    intersect = predicted_set & ground_set

    for element in intersect:
        if predicted_mapping[element] == ground_truth[element]:
            TP += 1
        else:
            mismatch_set.add(element)

    for miss in mismatch_set:
        pred = predicted_mapping.get(miss, [])
        gt = ground_truth.get(miss, [])

        # If either side is empty, we cannot compute medians
        if not pred or not gt:
            FN += 1
            FP += 1
            continue

        diff = abs(len(pred) - len(gt))

        if diff < 2:
            diff_median = abs(
                statistics.median(pred) -
                statistics.median(gt)
            )
            if diff_median < 3:
                TP += 1
            else:
                FN += 1
                FP += 1
        else:
            FN += 1
            FP += 1


        if diff < 2:
            diff_median = abs(
                statistics.median(predicted_mapping[miss]) -
                statistics.median(ground_truth[miss])
            )
            if diff_median < 3:
                TP += 1
            else:
                FN += 1
                FP += 1
        else:
            FN += 1
            FP += 1

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }
