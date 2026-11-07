import math
def minimax(depth, index, maxTurn, scores, target, count):
    if depth == target:
        count[0] += 1
        return scores[index]
    if maxTurn:
        left = minimax(depth + 1, index * 2, False,
                       scores, target, count)
        right = minimax(depth + 1, index * 2 + 1, False,
                        scores, target, count)
        return max(left, right)
    else:
        left = minimax(depth + 1, index * 2, True,
                       scores, target, count)
        right = minimax(depth + 1, index * 2 + 1, True,
                        scores, target, count)
        return min(left, right)

def alphabeta(depth, index, maxTurn, scores, target,
              alpha, beta, count):
    if depth == target:
        count[0] += 1
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            child = alphabeta(
                depth + 1, index * 2 + i, False,
                scores, target, alpha, beta, count
            )
            value = max(value, child)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            child = alphabeta(
                depth + 1, index * 2 + i, True,
                scores, target, alpha, beta, count
            )
            value = min(value, child)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = int(math.log2(len(scores)))
minimax_count1 = [0]
alpha_count1 = [0]
minimax_value1 = minimax(0, 0, True, scores, depth, minimax_count1)
alpha_value1 = alphabeta(0, 0, True, scores, depth,float('-inf'), float('inf'), alpha_count1)

print("ORIGINAL BRANCH ORDER")
print("Minimax Value:", minimax_value1)
print("Minimax Evaluated Leaves:", minimax_count1[0])
print("Alpha-Beta Value:", alpha_value1)
print("Alpha-Beta Evaluated Leaves:", alpha_count1[0])

reordered_scores = []
for i in range(len(scores) - 2, -1, -2):
    reordered_scores.append(scores[i])
    reordered_scores.append(scores[i + 1])
minimax_count2 = [0]
alpha_count2 = [0]
minimax_value2 = minimax(0, 0, True, reordered_scores, depth, minimax_count2)
alpha_value2 = alphabeta(0, 0, True, reordered_scores, depth,float('-inf'), float('inf'), alpha_count2)
print("\nREORDERED BRANCHES")
print("Minimax Value:", minimax_value2)
print("Minimax Evaluated Leaves:", minimax_count2[0])
print("Alpha-Beta Value:", alpha_value2)
print("Alpha-Beta Evaluated Leaves:", alpha_count2[0])
