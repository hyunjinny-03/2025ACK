import pandas as pd
import re

# 1. CSV 파일 불러오기
df = pd.read_csv('benefits.csv', encoding='cp949')

# 2. 혜택 관련 컬럼 추출 (혜택1 ~ 혜택18 같은 컬럼들 자동 추출)
benefit_cols = [col for col in df.columns if '혜택' in col]

# 3. 혜택 텍스트 정제 함수 정의
def clean_benefits(row):
    # NaN 제외하고 모든 혜택 텍스트 합치기
    benefits = [str(row[col]) for col in benefit_cols if pd.notnull(row[col])]

    # 각 혜택 문자열에서 특수문자 제거, 공백 정리
    benefits = [re.sub(r'[^가-힣A-Za-z\s]', ' ', benefit) for benefit in benefits]  # 한글/영문/공백만 남김
    benefits = [re.sub(r'\s+', ' ', benefit).strip() for benefit in benefits]  # 공백 정리

    # 하나의 문자열로 합치기
    combined = ' '.join(benefits)

    # 중복 단어 제거 (단어 순서는 유지)
    words = combined.split()
    deduped = ' '.join(sorted(set(words), key=words.index))
    return deduped


# 4. 새로운 컬럼 생성: 통합 혜택
df['통합혜택'] = df.apply(clean_benefits, axis=1)

# 5. 결과 확인
print(df[['카드명_x', '통합혜택']].head())

# 6. 저장
df.to_csv('preprocessing_of_benefit.csv', index=False, encoding='utf-8-sig')
