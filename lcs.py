def lcs(text1, text2):
    m, n = len(text1), len(text2)
    longest = 0
    end_indices = []
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest:
                    longest = dp[i][j]
                    end_indices = [i]
                elif dp[i][j] == longest:
                    end_indices.append(i)
            else:
                dp[i][j] = 0

    substrings = [text1[end - longest:end] for end in end_indices]
    return substrings
