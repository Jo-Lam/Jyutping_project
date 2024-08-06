# this file does a simple counting of how unique each transformation is
# this is to capture how specific the romanised information captures
# add simplified chinese for comparison - doesn't make a difference here.


import pandas as pd
df = pd.read_csv("data/20240806_cleandata.csv")
unique_counts = df.nunique() # some chi characters not loaded properly. Inspect using CSV is more accurate.

# inspecting dup in representation
filtered_df = df[df.groupby('surname')['中文姓'].transform('nunique') > 1]
filtered_df.to_csv("shared_eng_diff_chi.csv", encoding = 'utf_8_sig')

filtered_df = df[df.groupby('中文姓')['surname'].transform('nunique') > 1]
filtered_df.to_csv("test.csv", encoding = 'utf_8_sig')

filtered_df = df[df.groupby('中文姓')['surname_jyutping'].transform('nunique') > 1] # none
filtered_df = df[df.groupby('surname_jyutping')['中文姓'].transform('nunique') > 1]

filtered_df = df[df.groupby('中文姓_SIMP')['surname_pinyin'].transform('nunique') > 1] # none
filtered_df = df[df.groupby('surname_pinyin')['中文姓_SIMP'].transform('nunique') > 1]

filtered_df = df[df.groupby('forename_jyutping')['中文名'].transform('nunique') > 1]

filtered_df = df[df.groupby('forename_pinyin')['中文名'].transform('nunique') > 1]


# common jyutping tonal combinations
df['jyut_tone'] = df['surname_jyutping_char1_t'].astype(str).str.cat(df[['forename_jyutping_char1_t', 'forename_jyutping_char2_t']].astype(str), sep='')
df['pin_tone'] = df['surname_pinyin_char1_t'].astype(str).str.cat(df[['forename_pinyin_char1_t', 'forename_pinyin_char2_t']].astype(str), sep='')

def remove_chars(s):
    if len(s) == 5:
        # Remove characters at index 3 (4th position) and index 4 (5th position)
        return s[:3]
    else:
        return s

df['jyut_tone'] = df['jyut_tone'].apply(remove_chars)
df['pin_tone'] = df['pin_tone'].apply(remove_chars)

jyut_counts = df['jyut_tone'].value_counts()
jyut_counts.to_csv('jyut_count.csv')

pin_counts = df['pin_tone'].value_counts()
pin_counts.to_csv('pin_count.csv')


# plot
import matplotlib.pyplot as plt

jyut_counts = df['jyut_tone'].value_counts().nlargest(10)
pin_counts = df['pin_tone'].value_counts().nlargest(10)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(jyut_counts.index, jyut_counts, label='Jyutping Tone Count', marker='o')
plt.plot(pin_counts.index, pin_counts, label='Pinyin Tone Count', marker='o')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Count')
plt.title('10 most common Jyutping and Pinyin Tone Count')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
