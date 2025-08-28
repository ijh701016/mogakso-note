import sys
input = sys.stdin.readline

# 단어를 알파벳 빈도 딕셔너리로 변환하여 저장
def add_word(word):
    temp = dict()
    for x in word:
        if x in temp:
            temp[x] += 1
        else:
            temp[x] = 1
    words_dict[word] = temp
    return

# 퍼즐로 단어를 만들 수 있는지 확인
def can_make_word(puzzle, word):
    for x in word:
        if word[x] > puzzle.get(x, 0):
            return False
    return True

# 결과 출력 함수
def print_answer(puzzle_count):
    ans = list(puzzle_count.items())
    ans.sort(key = lambda x: (x[1],x[0]))
    min_, max_ = ans[0][1], ans[-1][1]
    min_alpha, max_alpha = "",""
    for x, cnt in ans:
        if cnt == min_:
            min_alpha += x
        if cnt == max_:
            max_alpha += x
    print(min_alpha, min_, max_alpha, max_)

# 단어 입력
words_dict = dict()
while True:
    word = input().strip()
    if word == "-":
        break
    if word in words_dict:
        continue
    add_word(word)

# 퍼즐 입력
while True:
    puzzle = input().strip()
    if puzzle == "#":
        break
        
    # 퍼즐의 알파벳 빈도 딕셔너리 생성
    puzzle_dict = dict()
    for x in puzzle:
        if x in puzzle_dict:
            puzzle_dict[x] += 1
        else:
            puzzle_dict[x] = 1

    # 퍼즐에 포함된 단어의 알파벳 개수 계산
    puzzle_count = {t:0 for t in puzzle_dict.keys()}
    for word_dict in words_dict.values():
        if can_make_word(puzzle_dict, word_dict):
            for x in word_dict:
                puzzle_count[x] += 1

    # 결과 출력
    print_answer(puzzle_count)