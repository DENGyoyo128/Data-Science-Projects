
"""
任务简述：
构建并测试一个文本分类器，用来区分“胡说”和“非胡说”的句子
-使用 TF-IDF 将文本转为数值特征。
-用 随机森林分类器 训练一个模型，把句子分为 Nonsense / No Nonsense。
"""



# ## Given the following data and labels
import pandas as pd

# Read the CSV
df = pd.read_csv("nonsense_dictionary.csv")

# Make sure the columns match your desired format
# e.g., rename if needed
df = df.rename(columns={
    "text": "content",   # if your CSV uses "text"
    "category": "label"  # if your CSV uses "category"
})

# Convert label to numeric if it's categorical (optional)
# Example: if nonsense = 1, no nonsense = 0
df["label"] = df["label"].map({"Nonsense": 1, "No Nonsense": 0}).fillna(df["label"])

print(df.head())


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Extracting TF-IDF featuresß
word_vec = TfidfVectorizer()
x = word_vec.fit_transform(df['content'])
print(df['label'])
# Split the dataset into training and testing sets using x and label
x_train, x_test, y_train, y_test = train_test_split(x, df['label'] , test_size=0.3, random_state=0)
# Train a Random Forest Classifier and name it as classifier
classifier = RandomForestClassifier()
classifier.fit(x_train, y_train) # fit the data to classifier
# Make predictions on the test set
y_pred = classifier.predict(x_test)
# Evaluate the classifier
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

## Test with new data
sentences = ["We should eat meat daily.", 'The world is peaceful.']
sample = word_vec.transform(sentences)
new_predictions = classifier.predict(sample) # use the trained classifier to make prediction
for i, each in enumerate(sentences):
# print out the result if this is nonsense or fact.
    print(f"Content: {each}\nPredicted Label: {'Nonsense' if new_predictions[i] == 1 else 'No Nonsense'}\n")