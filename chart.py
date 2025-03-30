import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load both CSV files
df_adidas = pd.read_csv("csv/pricing_ef66338733fc4ecea49009daf3b202c0_competitor_analysis_20250330_193404.csv")  # Adidas dataset
df_puma = pd.read_csv("csv/pricing_a6d28c4cd55f46edbd5825a2ad57b6f9_competitor_analysis_20250330_193404.csv")  # Puma dataset

# Convert 'price' to numeric (remove '$' sign if present)
df_adidas["price"] = df_adidas["price"].replace('[\$,]', '', regex=True).astype(float)
df_puma["price"] = df_puma["price"].replace('[\$,]', '', regex=True).astype(float)

# Add 'Brand' column to differentiate products
df_adidas["Brand"] = "Adidas"
df_puma["Brand"] = "Puma"

# Keep only relevant columns
df_adidas = df_adidas[["title", "price", "Brand"]]
df_puma = df_puma[["title", "price", "Brand"]]

# Combine both datasets
df_combined = pd.concat([df_adidas, df_puma])

# Plot the bar graph
plt.figure(figsize=(12, 6))
sns.barplot(x="title", y="price", hue="Brand", data=df_combined, palette=["blue", "red"])

# Labels and title
plt.xticks(rotation=45, ha="right")
plt.xlabel("Product Name")
plt.ylabel("Price ($)")
plt.title("Adidas vs. Puma Price Comparison")
plt.legend(title="Brand")

# Show the plot
plt.show()
