import math
def minimax(depth, index, maxTurn, scores, target, count):
    if depth == target:
        count[0] += 1
        return scores[index]
    if maxTurn:
        return max(
            minimax(depth + 1, index * 2, False,scores, target, count),
            minimax(depth + 1, index * 2 + 1, False,scores, target, count)
        )
    else:
        return min(
            minimax(depth + 1, index * 2, True,scores, target, count),
            minimax(depth + 1, index * 2 + 1, True,scores, target, count)
        )
def alphabeta(depth, index, maxTurn, scores,target, alpha, beta, count):
    if depth == target:
        count[0] += 1
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(
                value,
                alphabeta(depth + 1, index * 2 + i,False, scores, target,alpha, beta, count)
            )
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(
                value,
                alphabeta(depth + 1, index * 2 + i,True, scores, target,alpha, beta, count)
            )
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = int(math.log2(len(scores)))
minimax_count = [0]
alpha_beta_count = [0]
minimax_value = minimax(0, 0, True, scores, depth, minimax_count)
alpha_beta_value = alphabeta(0, 0, True, scores, depth,float('-inf'), float('inf'), alpha_beta_count)
print("Minimax Value:", minimax_value)
print("Minimax Evaluated Leaves:", minimax_count[0])
print("Alpha-Beta Value:", alpha_beta_value)
print("Alpha-Beta Evaluated Leaves:", alpha_beta_count[0])