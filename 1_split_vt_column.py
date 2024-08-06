import pandas as pd
import re
df = pd.read_csv('data/checking.csv')

# Function to count number of numbers
def count_numbers(s):
    return len(re.findall(r'\d', s))

df['surname_jyutping'].apply(count_numbers).value_counts()
df['forename_jyutping'].apply(count_numbers).value_counts()
df['surname_pinyin'].apply(count_numbers).value_counts()
df['forename_pinyin'].apply(count_numbers).value_counts()

# Function to split the strings at the first number
def split_at_number(s):
    import re
    match = re.search(r'(\d+)', s)
    if match:
        return s[:match.start()], match.group(1), s[match.end():]
    else:
        return s, '', ''

df[['surname_jyutping_char1_v', 'surname_jyutping_char1_t', 'surname_jyutping_rest']] = df['surname_jyutping'].apply(split_at_number).apply(pd.Series)
df = df.drop(columns=['surname_jyutping_rest'])

df[['surname_pinyin_char1_v', 'surname_pinyin_char1_t', 'surname_pinyin_rest']] = df['surname_pinyin'].apply(split_at_number).apply(pd.Series)
df = df.drop(columns=['surname_pinyin_rest'])

# split number of times depends on how many characters in sur/forename
df[['forename_jyutping_char1_v', 'forename_jyutping_char1_t', 'forename_jyutping_rest']] = df['forename_jyutping'].apply(split_at_number).apply(pd.Series)
df[['forename_jyutping_char2_v', 'forename_jyutping_char2_t', 'forename_jyutping_rest']] = df['forename_jyutping_rest'].apply(split_at_number).apply(pd.Series)
df = df.drop(columns=['forename_jyutping_rest'])

df[['forename_pinyin_char1_v', 'forename_pinyin_char1_t', 'forename_pinyin_rest']] = df['forename_pinyin'].apply(split_at_number).apply(pd.Series)
df[['forename_pinyin_char2_v', 'forename_pinyin_char2_t', 'forename_pinyin_rest']] = df['forename_pinyin_rest'].apply(split_at_number).apply(pd.Series)
df = df.drop(columns=['forename_pinyin_rest'])

df.to_csv('data/20240724_cleandata.csv', encoding = 'utf_8_sig') 
