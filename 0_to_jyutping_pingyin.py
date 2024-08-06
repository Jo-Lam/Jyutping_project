# preparing the data
# pip install pinyin_jyutping
# Data used scrapped online
# from - google searches 
# https://www.kcckc.edu.hk/main/banner/2223_F.1-F.3_Math%20EMI_update.pdf
# https://twghwyyms.edu.hk/uploads/file/202104/ce22d8e366dbcd7bf846113ddabb1581.pdf
# https://twghwyyms.edu.hk/uploads/file/202105/9d52f09a13661b77bae34cc322ddf7cb.pdf
# https://www.rcphkmc.edu.hk/sites/default/files/files/zhong_yi_fen_ban_ming_dan_updated.pdf
# https://www.hktta.org.hk/hstta/pdf/COURSE/Advance/HSC42_Namelist.pdf
# https://www.wingkwong.edu.hk/uploads/files/%E4%B8%AD%E4%B8%80%E6%96%B0%E7%94%9F%E5%88%86%E7%8F%AD%E5%90%8D%E5%96%AE.pdf
# https://www.semplekg.edu.hk/wp-content/uploads/2021/11/22-23%E5%B9%B4%E5%BA%A6%E5%B9%BC%E5%85%92%E7%8F%AD%E9%8C%84%E5%8F%96%E5%90%8D%E5%96%AE.pdf

import pandas as pd
import pinyin_jyutping ## using CC-Canto, open source cantonese dictionary with both jyutping and pinyin [https://cantonese.org/download.html, https://github.com/Vocab-Apps/pinyin-jyutping]

df = pd.read_excel("data/raw_namelist.xlsx")
j = pinyin_jyutping.PinyinJyutping()

# surname
column_a_string = ','.join(df['中文姓'].astype(str))
processed_string_jyut = j.jyutping(column_a_string, tone_numbers=True)
processed_list_jyut = processed_string_jyut.split(' , ')
processed_string_pinyin = j.pinyin(column_a_string, tone_numbers=True)
processed_list_pinyin = processed_string_pinyin.split(' , ')

df['surname_jyutping'] = processed_list_jyut
df['surname_pinyin'] = processed_list_pinyin

# check failed - 
pattern = r'\d'
df_filtered = df[~df['surname_jyutping'].str.contains(pattern)]
df_filtered['surname_jyutping'].value_counts()

df_filtered2 = df[~df['surname_pinyin'].str.contains(pattern)]
df_filtered2['surname_pinyin'].value_counts()

data = {
    '中文姓': [
        '李', "梁", '劉', '林', '葉',
        '盧', '鄺', '羅', '黎', '冷',
        '凌', '勞', '車', '呂', '陸'
    ],
    'surname_jyutping': [
        'lei5', 'loeng4', 'lau4', 'lam4', 'jip6',
        'lou4', 'kwong3', 'lo4', 'lai4', 'laang5',
        'ling4', 'lou4', 'ce1', 'leoi5', 'luk6'
    ],
    'surname_pinyin':[
        'li3', 'liang2', 'liu2', 'lin2', 'ye4',
        'lu3', 'kuang4', 'luo2', 'li2', 'leng3',
        'ling2', 'lao2', 'che1', 'lv3', 'lu4',
    ]
}

df2 = pd.DataFrame(data)
df['surname_jyutping'] = df['surname_jyutping'].combine_first(df2['surname_jyutping'])
df['surname_pinyin'] = df['surname_pinyin'].combine_first(df2['surname_pinyin'])

df_clean = pd.merge(df, df2, on='中文姓', how='left')

df_clean['surname_jyutping_y'] = df_clean['surname_jyutping_y'].fillna(df_clean['surname_jyutping_x'])
df_clean['surname_pinyin_y'] = df_clean['surname_pinyin_y'].fillna(df_clean['surname_pinyin_x'])

df_clean = df_clean.drop(columns = ['surname_jyutping_x','surname_pinyin_x'])

# final check
df_clean[~df_clean['surname_jyutping_y'].str.contains(pattern)]
df_clean[~df_clean['surname_pinyin_y'].str.contains(pattern)]

# forename
forename = ','.join(df['中文名'].astype(str))
processed_forename_jyut = j.jyutping(forename, tone_numbers=True)
processed_list_jyut = processed_forename_jyut.split(' , ')
processed_forename_pinyin = j.pinyin(forename, tone_numbers=True)
processed_list_pinyin = processed_forename_pinyin.split(' , ')

df_clean['forename_jyutping'] = processed_list_jyut
df_clean['forename_pinyin'] = processed_list_pinyin

df_filtered = df_clean[~df_clean['forename_jyutping'].str.contains(pattern)]
df_filtered['中文名'].value_counts()

df_filtered2 = df_clean[~df_clean['forename_pinyin'].str.contains(pattern)]
df_filtered2['中文名'].value_counts()

data = {
    '中文名': [
        '栢晞', "芓蓁", '朗', '昶', '甯匤',
        '諾', '禮行', '岶昍', '鉦澔', '釓橦'
    ],
    'forename_jyutping': [
        'paak3hei1', 'zi2zoen1', 'long5', 'cong2', 'ning6kuk1',
        'nok6', 'lai5hang6', 'paak3hyun1', 'zing1hou6', 'gaat3tung4',
    ],
    'forename_pinyin':[
        'bo2xi1', 'zi1zhen1', 'lang3', 'chang3', 'ning4qu1',
        'nuo4', 'li3xing2', 'po4xuan1', 'zheng1hao4', 'ga2tong2',
    ]
}

df2 = pd.DataFrame(data)
df_clean = pd.merge(df_clean, df2, on='中文名', how='left')

df_clean['forename_jyutping_y'] = df_clean['forename_jyutping_y'].fillna(df_clean['forename_jyutping_x'])
df_clean['forename_pinyin_y'] = df_clean['forename_pinyin_y'].fillna(df_clean['forename_pinyin_x'])

df_clean = df_clean.drop(columns = ['forename_jyutping_x','forename_pinyin_x'])
# df_clean.to_csv('data/checking.csv', encoding = 'utf_8_sig') 
# some further manual cleaning...
