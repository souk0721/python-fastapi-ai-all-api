import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def tokenize_and_check(data, token_limit=3000):
    """
    데이터의 각 'text' 필드를 토큰화하고, 토큰 수가 지정된 한계를 초과하는지 확인합니다.

    :param data: 텍스트와 타임스탬프가 포함된 딕셔너리의 리스트
    :param token_limit: 토큰 수 제한 (기본값 3000)
    :return: 토큰 수가 한계를 초과하면 True, 그렇지 않으면 False
    """
    total_tokens = []

    for item in data:
        tokens = word_tokenize(item['text'])
        total_tokens.extend(tokens)
        

        if len(total_tokens) > token_limit:
            return True
    print(total_tokens)

    return False


