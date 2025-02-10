import re
import pandas as pd
file_path = "C:/Users/VP/Downloads/productdata - Sheet1.csv"

df = pd.read_csv(file_path)

threshold = len(df) * 0.5
df = df.dropna(axis=1, thresh=threshold)

df.fillna(df.mode().iloc[0], inplace=True)

df.dropna(inplace = True)



df = df.drop_duplicates(subset=["PRODUCTID", "TITLE"])
print(f"Total duplicate rows after cleaning: {df.duplicated().sum()}")  # Should be 0


df.columns = (
    df.columns.str.strip()  # Remove leading/trailing spaces
    .str.lower()  # Convert to lowercase
    .str.replace(r"[^\w\s]", "", regex=True)  # Remove special characters
    .str.replace(" ", "_")  # Replace spaces with underscores
)
print(df.columns)


numeric_columns = ["producttypeid", "productlength"]  # Adjust based on dataset
for col in numeric_columns:
    df[col] = df[col].where(df[col] >= 0, 0)  # Replace negative values with 0
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert non-numeric to NaN
    df[col].fillna(0, inplace=True)  # Replace NaNs with 0
    


df["productlength"] = df["productlength"].clip(lower=0, upper=5)  # Ensure ratings are between 0-5

Q1 = df["producttypeid"].quantile(0.25)
Q3 = df["producttypeid"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["producttypeid"] < lower_bound) | (df["producttypeid"] > upper_bound)]
print("Outliers in Price:\n", outliers)

df["producttypeid"] = df["producttypeid"].clip(lower=lower_bound, upper=upper_bound)
print(df["producttypeid"])

print(df["productid"].unique())  # View unique categories

df = df.drop_duplicates(subset=["productid","bullet_points"])
duplicate_id = df[df.duplicated(subset=["bullet_points"], keep=False)]["bullet_points"].unique()  # Example categories
df = df[df["bullet_points"].isin(duplicate_id)]

print(df)
print(df.head())

def create_short_title(title):
    if pd.isna(title):
        return ""  # Handle missing titles
    
    # Convert to lowercase
    title = title.lower()
    
    # Remove special characters (except spaces)
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    
    # Define stop words and redundant phrases to remove
    redundant_words = ['includes', 'set of', 'features', 'with', 'for', 'and', 'or', 'canvas fabric']
    
    # Remove redundant words
    title = ' '.join([word for word in title.split() if word not in redundant_words])
    
    # Extract key components based on patterns (e.g., size, quantity)
    title = re.sub(r'(\d+)\s*(pcs?|y)', r'- \1 \2', title)  # Replace size/quantity format
    
    # Truncate the title to a maximum of 50 characters for SEO
    title = title[:50]
    
    return title
# Apply the function to create the 'short_title' column
df['short_title'] = df['title'].apply(create_short_title)


if not df.empty:
    # Save the updated DataFrame with the new 'short_title' column to a new CSV file
    df.to_csv('C:/Users/VP/Downloads/updated_products.csv', index=False)
    print(df[['title', 'short_title']].head())
    # Confirm the file has been saved
    print("File saved successfully!")
else:
    print("Warning: DataFrame is empty after processing. Check filtering steps.")

df_saved = pd.read_csv("C:/Users/VP/Downloads/updated_products.csv")
print(df_saved.head())  # Ensure short_title is present
