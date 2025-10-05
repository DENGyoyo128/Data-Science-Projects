"""
Text Preprocessing (Tokenization, Stemming, Lemmatization)
文本预处理操作：
-去掉多余空格
-统一大小写
-分词 (Tokenization)：将文本分割成单词
-词干提取 (Stemming)
-词形还原 (Lemmatization)
"""


"""
Text Tokenization(分词)
用分隔符（如空格、标点）将文本切割成单词或句子。
"""

from nltk.tokenize import PunktSentenceTokenizer
import string
# Example text
sample_text = """"So you said today, as you often say, that you live in Singapore. Of what nation are you a 
citizen?", said the Senator.
"Singapore, sir. Senator.", said Shou Chew.
"Are you a citizen of any other nation?", said the Senator.
"No, Senator.", said Shou Chew.
"""
# Initialize the Punkt tokenizer
punkt_tokenizer = PunktSentenceTokenizer()


# Tokenize the sample text using the Punkt tokenizer
sentences = punkt_tokenizer.tokenize(sample_text)
print(sentences)

# Display the tokenized sentences
for i, sentence in enumerate(sentences):
    # print(i, sentence)
    clean_str = ''
    for ch in sentence:
        if ch not in string.punctuation:
            clean_str += ch
    print(i+1,clean_str.strip())


"""
词干提取 (Stemming)
英文单词常有后缀（-s, -ed, -ing 等），词干 (Stem) 是去掉后缀的基础形式。
"""


# nltk.download('punkt')
from nltk.stem import PorterStemmer
ps=PorterStemmer()
print(ps.stem('studies'))



"""
Lemmatization(词形还原)
与词干提取类似，但会得到有效的词根 (lemma)。
"""


# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
wnl=WordNetLemmatizer()
print(wnl.lemmatize('studies',"n"))