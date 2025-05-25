import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import tree
import matplotlib.pyplot as plt

# Membuat data contoh
data = {
    'Hari': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    'Outlook': ['Hujan', 'Hujan', 'Mendung', 'Cerah', 'Cerah', 'Cerah', 'Mendung', 'Hujan', 'Hujan', 'Cerah', 'Hujan', 'Mendung', 'Mendung', 'Cerah'],
    'Suhu': ['Panas', 'Panas', 'Panas', 'Sejuk', 'Dingin', 'Dingin', 'Dingin', 'Sejuk', 'Dingin', 'Sejuk', 'Sejuk', 'Sejuk', 'Panas', 'Sejuk'],
    'Kelembaban': ['Tinggi', 'Tinggi', 'Tinggi', 'Tinggi', 'Normal', 'Normal', 'Normal', 'Tinggi', 'Normal', 'Normal', 'Normal', 'Tinggi', 'Normal', 'Tinggi'],
    'Angin': ['Sepoi', 'Kencang', 'Sepoi', 'Sepoi', 'Sepoi', 'Kencang', 'Kencang', 'Sepoi', 'Sepoi', 'Sepoi', 'Kencang', 'Kencang', 'Sepoi', 'Kencang'],
    'Jalan-jalan': ['Tidak', 'Tidak', 'Ya', 'Ya', 'Ya', 'Tidak', 'Ya', 'Tidak', 'Ya', 'Ya', 'Ya', 'Ya', 'Ya', 'Tidak']
}
df = pd.DataFrame(data)

# Menampilkan data input dalam format tabel
print("Data Input:")
print(df)

# Fungsi untuk menghitung entropi
def entropy(target_col):
    values, counts = np.unique(target_col, return_counts=True)
    probabilities = counts / len(target_col)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

# Fungsi untuk menghitung information gain
def information_gain(data, feature, target):
    entropy_before = entropy(data[target])
    values, counts = np.unique(data[feature], return_counts=True)
    entropy_after = 0
    for value, count in zip(values, counts):
        subset = data[data[feature] == value]
        entropy_after += (len(subset) / len(data)) * entropy(subset[target])
    gain = entropy_before - entropy_after
    return gain

# Fungsi untuk membuat decision tree
def build_tree(data, features, target):
    if len(np.unique(data[target])) == 1:
        return np.unique(data[target])[0]
    if len(features) == 0:
        return np.unique(data[target])[0]
    best_feature = max(features, key=lambda feature: information_gain(data, feature, target))
    print(f"Root/Parent Node: {best_feature}")  # Display the root node
    tree = {best_feature: {}}
    features = [feature for feature in features if feature != best_feature]
    for value in np.unique(data[best_feature]):
        subset = data[data[best_feature] == value]
        print(f"Child Node of {best_feature}: {value}")  # Display child nodes
        tree[best_feature][value] = build_tree(subset, features, target)
    return tree

# Membuat decision tree
features = ['Outlook', 'Suhu', 'Kelembaban', 'Angin']
target = 'Jalan-jalan'
tree = build_tree(df, features, target)

# Menampilkan decision tree
print(tree)

# Mengubah decision tree ke format yang dapat divisualisasikan
clf = DecisionTreeClassifier()
X = pd.get_dummies(df[['Outlook', 'Suhu', 'Kelembaban', 'Angin']]) # Get the one-hot encoded features
clf.fit(X, df['Jalan-jalan'])

# Menampilkan figure decision tree
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=X.columns, # Use the columns of the one-hot encoded data as feature_names
          class_names=['Tidak', 'Ya'], filled=True, rounded=True)
plt.show()