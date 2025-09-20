import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read CSV data
df = pd.read_csv("result.csv")  # assumes two columns: "Label", "Value"
df = df[df["feature"] == "BoC only"]
labels = df["classifier"]
values = df["recall"]
print(values)

# Determine color map: higher values get darker green
norm = plt.Normalize(0.8, 1.0)
colors = plt.cm.Greens(norm(values))

# Highlight the max value bar
max_index = values.idxmax()
colors[max_index] = (1.0, 0.4, 0.4, 1.0)  # red for highest value

# Plot settings
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(labels, values, color=colors)

# Add value labels on top
for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height:.2f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

# Legend
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor="red", edgecolor="red", label="Highest Value"),
    Patch(facecolor=plt.cm.Greens(0.9), label="High"),
    Patch(facecolor=plt.cm.Greens(0.7), label="Medium"),
    Patch(facecolor=plt.cm.Greens(0.5), label="Low"),
]
ax.legend(handles=legend_elements, loc="lower right")

ax.set_ylim(0.75, 1.01)
ax.set_ylabel("Value")
ax.set_title("Bar Graph with Color-Coded Values")
plt.xticks(rotation=45, fontsize=8)

plt.tight_layout()
plt.show()
