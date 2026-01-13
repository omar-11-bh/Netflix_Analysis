import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

df = pd.read_csv("../data/netflix_titles.csv", encoding="utf-8")
df.head()

df.info()
df.isnull().sum()

# Fill missing values

for col in ["director", "cast", "country", "rating"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

#Convert date_added if present

if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year

#Ensure release_year is numeric

if "release_year" in df.columns:
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")


#MOVIES VS TV SHOWS

if "type" in df.columns:
    sns.countplot(data=df, x="type", palette="viridis")
    plt.title("Movies vs TV Shows")
    plt.show()
else:
    print("Column 'type' not found in the dataset.")


#TOP 10 GENRES

if "listed_in" in df.columns:
    genres = df["listed_in"].dropna().str.split(", ").explode()
    top_genres = genres.value_counts().head(10)

    sns.barplot(x=top_genres.values, y=top_genres.index, palette="magma")
    plt.title("Top 10 Genres on Netflix")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.show()
else:
    print("Column 'listed_in' not found in the dataset.")


#Releases per year

if "release_year" in df.columns:
    year_counts = df["release_year"].dropna().astype(int).value_counts().sort_index()

    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o")
    plt.title("Number of Releases per Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.show()
else:
    print("Column 'release_year' not found in the dataset.")


# Summary Insights

print("Total titles:", len(df))

if "type" in df.columns:
    print("Movies:", (df["type"] == "Movie").sum())
    print("TV Shows:", (df["type"] == "TV Show").sum())

if "listed_in" in df.columns:
    print("\nMost common genre:", genres.value_counts().idxmax())

if "release_year" in df.columns:
    print("Most active release year:", year_counts.idxmax())


