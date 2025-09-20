import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.pipeline import Pipeline
from sql_tokenizer import tokenize

pipeline = Pipeline(
    [
        (
            "count_vec",
            CountVectorizer(
                tokenizer=tokenize,
                preprocessor=lambda x: x,
                lowercase=False,
                ngram_range=(1, 3),
            ),
        ),
        ("tfidf", TfidfTransformer()),
    ]
)

X_vec = pipeline.fit_transform(data["Query"])
df = pd.DataFrame(X_vec.toarray(), columns=pipeline.get_feature_names_out())
num_clusters = 10  # tune based on pattern diversity
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X_vec)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_
data["cluster"] = kmeans.fit_predict(X_vec)
print(data["cluster"])
data["stratify_col"] = data["Label"].astype(str) + "_" + data["cluster"].astype(str)
data.to_csv("stratified-data.csv")
X_vis = PCA(n_components=3).fit_transform(X_vec)
centroids_vis = PCA(n_components=3).fit_transform(centroids)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(X_vis[:, 0], X_vis[:, 1], X_vis[:, 2], c=labels, cmap="viridis", alpha=0.6)
ax.scatter(
    centroids_vis[:, 0],
    centroids_vis[:, 1],
    centroids_vis[:, 2],
    c="red",
    marker="x",
    s=100,
)
plt.title("3D K-Means Clustering")
plt.show()

tsne = TSNE(n_components=2, perplexity=30, random_state=42, n_iter=1000)
X_2d = tsne.fit_transform(X_vec.toarray())  # TSNE requires dense input

data["x"] = X_2d[:, 0]
data["y"] = X_2d[:, 1]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="x", y="y", hue="label", palette=["green", "red"], alpha=0.6)
sns.scatterplot(data=df, x="x", y="y", hue="cluster", palette="tab10", alpha=0.7)
plt.title("Clustering of SQLi Payloads")
plt.show()
