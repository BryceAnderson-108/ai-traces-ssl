# in parts AI written
# adjust paths in lines 34, 52, 80
from scipy.stats import chi2_contingency

def count_words(text):
    freq_dct = dict()
    total_words = 0
    for line in text:
        line = line.strip()
        words = line.split()
        for word in words:
            if word in freq_dct:
                freq_dct[word] += 1
            else:
                freq_dct[word] = 1
            total_words += 1
    return freq_dct, total_words

def chi_sq_test_for_significance(word, freq_dct2020_absolute, freq_dct2024_absolute, total_words2020, total_words2024, min_opm_2020):
    if word in freq_dct2020_absolute:
        data = [[freq_dct2020_absolute[word], total_words2020], [freq_dct2024_absolute[word], total_words2024]]
    else:
        data = [[min_opm_2020, total_words2020], [freq_dct2024_absolute[word], total_words2024]]

    # Performing the chi-square test
    chi2, p_value, dof, expected = chi2_contingency(data)

    chi2, p_value, expected
    # if the p-value is less than 0.05, return True
    return p_value < 0.05



text2020 = open('PATH/yearspos/2022_cleaned.txt', 'r', encoding='utf-8') # input_human_abstracts_sample_2020.txt
freq_dct2020, total_words2020 = count_words(text2020)
text2020.close()

freq_dct2020_absolute = freq_dct2020.copy()

# normalize the frequencies to occurances per 1000000 words
for word in freq_dct2020:
    freq_dct2020[word] = freq_dct2020[word] / total_words2020 * 1000000

"""# for any entry in the frequency dictionary, drop the entry if the frequency is less than 5
for word in list(freq_dct2020.keys()):
    if freq_dct2020[word] < 1:
        del freq_dct2020[word]
"""

min_opm_2020 = 1000000/total_words2020

text2024 = open('PATH/yearspos/2024_cleaned.txt', 'r', encoding='utf-8') # output_ai_abstracts-from-summary_gpt-3.5-turbo-instruct.txt
freq_dct2024, total_words2024 = count_words(text2024)
text2024.close()

freq_dct2024_absolute = freq_dct2024.copy()

# normalize the frequencies to occurances per 1000000 words
for word in freq_dct2024:
    freq_dct2024[word] = freq_dct2024[word] / total_words2024 * 1000000

# for any entry in the frequency dictionary, drop the entry if the frequency is less than 5
for word in list(freq_dct2024.keys()):
    if freq_dct2024[word] < 1:
        del freq_dct2024[word]

freq_diff = dict()
# calculate the increase in usage of each word in 2024 compared to 2020
for word in freq_dct2024:
    if word in freq_dct2020:
        freq_diff[word] = ((freq_dct2024[word] - freq_dct2020[word]) / freq_dct2020[word]) * 100
    else:
        freq_diff[word] = ((freq_dct2024[word] - min_opm_2020) / min_opm_2020) * 100

print(len(freq_diff))
# sort the dictionary by the increase in usage
sorted_freq_diff = dict(sorted(freq_diff.items(), key=lambda item: item[1], reverse=False))


output_file = open('PATH/change_reversed.tsv', 'w', encoding='utf-8') # brute_force_divergence_human_vs_ai-summary-based-abstracts
output_file.write("word\tchange (%)\topm 2020\topm 2024\tsignificant\n")


for word, increase in list(sorted_freq_diff.items()):
    result_is_significant = chi_sq_test_for_significance(word, freq_dct2020_absolute, freq_dct2024_absolute, total_words2020, total_words2024, min_opm_2020)
    if word in freq_dct2020_absolute:
        output_file.write(f"{word}\t{increase:.2f}\t{freq_dct2020[word]:.2f}\t{freq_dct2024[word]:.2f}\t{result_is_significant}\n")
    else:
        output_file.write(f"{word}\t{increase:.2f}\t{min_opm_2020:.2f}\t{freq_dct2024[word]:.2f}\t{result_is_significant}\n")

print(total_words2024)
