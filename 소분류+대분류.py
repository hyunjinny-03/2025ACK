import pandas as pd
import glob

# 1. 정제된 CSV 파일 모두 읽기
files = glob.glob('suwon_*.csv')
df_list = [pd.read_csv(file) for file in files]
df_all = pd.concat(df_list, ignore_index=True)

# 10대(1), 100대(10), 110대(11) 제외
df_all = df_all[~df_all['age'].isin([1, 10, 11])]

# 2. 연령, 성별, 구별(cty_rgn_no), 업종(card_tpbuz_nm_2)별 소비금액 합산
group_cols = ['cty_rgn_no', 'age', 'sex']
grouped = df_all.groupby(group_cols + ['card_tpbuz_nm_2'], as_index=False).agg(
    amt=('amt', 'sum'),
    card_tpbuz_nm_1=('card_tpbuz_nm_1', 'first')
)

# 3. 각 (구, 연령, 성별) 그룹 내 소비금액 상위 5개 업종 추출
grouped['rank'] = grouped.groupby(group_cols)['amt'].rank(method='first', ascending=False)
top5 = grouped[grouped['rank'] <= 5].copy()

# 4. 정렬 및 연령대 라벨링
top5 = top5.sort_values(group_cols + ['amt'], ascending=[True, True, True, False]).reset_index(drop=True)
top5['age'] = (top5['age'].astype(int) * 10).astype(str) + '대'

# 5. 저장
top5.to_csv('소분류+대분류.csv', index=False, encoding='utf-8-sig')