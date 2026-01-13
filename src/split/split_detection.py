from difflib import SequenceMatcher
from typing import Dict, List
# Hanan Code part for checking the Line split Detection 
#in this code i will use tte greedy algorithm

# L-> Line/S-> Similarity that will calculate how much two strings (a,b) are similar 
# here i will use the difflib.SequenceMatcher
def LS(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

#Here it will take what already mapping i have and will check if i took another like would make it more similar till a line that come and brek the similarity then it will stop 
#L1: the line on the left
#R1: the line on the right 
#start: it is the starting index (base)
#limit: how many lines i can match together, i choose it to be 10 lines is the max to be matched 
#min: which is the most important variable , the key to test the lines'score for similarity, i gave it a default value 2%, if the score was 2% or more it will accpet to extend to the next line
def SplitLogic(
    L1: str,
    R1: List[str],
    start: int,
    limit: int = 10,
    min: float = 0.02,
) -> List[int]:
    
    n = len(R1)
    
    #if statment to check if the base index is not valid it will retuen it 
    if start < 0 or start >= n:
        return [start]

    # startLine : Start with the single mapped line
    #lineText: text of the first right line
    #maxScore: the score for the similarity
    startline = [start]
    lineText = R1[start]
    maxScore = LS(L1, lineText)

    #try extending to next lines, up to limit score
    for offset in range(1, limit):
        #nextIndex: the one that will point to the next line
        nextIndx = start + offset
        # if statment for if i reached end of the file
        if nextIndx >= n:
            break  
        lineText = lineText + " " + R1[nextIndx]
        # the new update score 
        newScore = LS(L1, lineText)
        #accept the extension only when similarity improves, or the else part that will stop extending
        if newScore >= maxScore + min:
            maxScore = newScore
            startline.append(nextIndx)
        else:
            break
    return startline

#this will detect the result of the lines for the splited lines 
#L1: here it is the ones at the left BUt the new thing is that it will store All the lines on the left ,the old file, normalized 
#R1: here it is the ones at the right BUt the new thing is that it will store All the lines on the right ,the new file, normalized
# mapping : here it will do the single map that i will have from the other team member Parsia code for the mapping process
# and the benifit to this lines is to turn parsia's single-line mapping to allow the splits mapping where each left line can map to one or many right lines. 
def detect_splits(
    L1: List[str],
    R1: List[str],
    mapping: Dict[int, int],
) -> Dict[int, List[int]]:
    
    result: Dict[int, List[int]] = {}
    #a loop for going for each pair that i will get from Parsia mapping code
    for l_idx, r_idx in mapping.items():
        #if no split is detected for a line, it will still be a list of length 1
        if l_idx < 0 or l_idx >= len(L1):
            continue

        line_text = L1[l_idx]
        #these i explained before at line 11-16
        new_indices = SplitLogic(
            L1=line_text,
            R1=R1,
            start=r_idx,
            limit=10,
            min=0.02
        )
        result[l_idx] = sorted(new_indices)
    return result

if __name__ == "__main__":
#-----------------------------------------------------------------------------
# TO BE deleted, just to test my code till the project finish coding its parts
#-----------------------------------------------------------------------------
 
    # Test 1 
    left = ["x = a + b;"]
    right = ["x = a+"," b;", "hhhh"]
    mapping = {0: 0}
    print("Test 1:", SplitsDetector(left, right, mapping))
    # Expected: {0: [0, 1]}

    # Test 2
    left2 = ["return x;"]
    right2 = ["return x;", "unused;"]
    mapping2 = {0: 0}
    print("Test 2:", SplitsDetector(left2, right2, mapping2))
    # Expected: {0: [0]}

    # Test 3 
    left3 = ["total = a + b + c;"]
    right3 = ["total = a", "+ b", "+ c;","l"]
    mapping3 = {0: 0}
    print("Test 3:", SplitsDetector(left3, right3, mapping3))
    # Expected: {0: [0, 1, 2]}