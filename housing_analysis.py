"""
Housing Price Prediction - EDA and Model Training Script
This script performs comprehensive EDA and trains ML models for house price prediction.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('Housing.csv')

# ============================================================================
# EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================

print("\n" + "="*80)
print("EXPLORATORY DATA ANALYSIS (EDA)")
print("="*80)

# 1. Dataset Shape and Structure
print("\n1. DATASET SHAPE AND STRUCTURE")
print("-" * 80)
print(f"Dataset Shape: {df.shape}")
print(f"Number of Rows: {df.shape[0]}")
print(f"Number of Columns: {df.shape[1]}")
print(f"\nColumn Names: {list(df.columns)}")

# 2. Data Types
print("\n2. DATA TYPES")
print("-" * 80)
print(df.dtypes)

# 3. First Few Rows
print("\n3. FIRST FEW ROWS")
print("-" * 80)
print(df.head())

# 4. Summary Statistics
print("\n4. SUMMARY STATISTICS")
print("-" * 80)
print(df.describe())

# 5. Missing Value Analysis
print("\n5. MISSING VALUE ANALYSIS")
print("-" * 80)
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing_values,
    'Missing Percentage': missing_percent
})
print(missing_df[missing_df['Missing Count'] > 0])
if missing_df[missing_df['Missing Count'] > 0].empty:
    print("No missing values found in the dataset!")

# 6. Unique Value Counts
print("\n6. UNIQUE VALUE COUNTS")
print("-" * 80)
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique values")
    if unique_count <= 10:
        print(f"  Values: {df[col].unique()}")

# 7. Feature Distribution Analysis
print("\n7. FEATURE DISTRIBUTION ANALYSIS")
print("-" * 80)
numerical_cols = df.select_dtypes(include=[np.number]).columns
print(f"Numerical Features: {list(numerical_cols)}")
categorical_cols = df.select_dtypes(include=['object']).columns
print(f"Categorical Features: {list(categorical_cols)}")

# Calculate statistics for numerical features
print("\nNumerical Feature Statistics:")
for col in numerical_cols:
    print(f"\n{col}:")
    print(f"  Mean: {df[col].mean():.2f}")
    print(f"  Median: {df[col].median():.2f}")
    print(f"  Mode: {df[col].mode()[0] if not df[col].mode().empty else 'N/A'}")
    print(f"  Std Dev: {df[col].std():.2f}")
    print(f"  Min: {df[col].min()}")
    print(f"  Max: {df[col].max()}")

# 8. Skewness Analysis
print("\n8. SKEWNESS ANALYSIS")
print("-" * 80)
for col in numerical_cols:
    skewness = df[col].skew()
    print(f"{col}: {skewness:.4f} ({'Right skewed' if skewness > 0 else 'Left skewed' if skewness < 0 else 'Normal'})")

# 9. Correlation Matrix
print("\n9. CORRELATION MATRIX")
print("-" * 80)
correlation_matrix = df[numerical_cols].corr()
print(correlation_matrix)

# 10. Price Analysis
print("\n10. PRICE ANALYSIS")
print("-" * 80)
print(f"Price Statistics:")
print(f"  Mean Price: PKR {df['price'].mean():,.2f}")
print(f"  Median Price: PKR {df['price'].median():,.2f}")
print(f"  Min Price: PKR {df['price'].min():,.2f}")
print(f"  Max Price: PKR {df['price'].max():,.2f}")
print(f"  Price Range: PKR {df['price'].max() - df['price'].min():,.2f}")

# 11. Grouped Aggregations
print("\n11. GROUPED AGGREGATIONS")
print("-" * 80)
print("\nAverage Price by Furnishing Status:")
print(df.groupby('furnishingstatus')['price'].mean().sort_values(ascending=False))

print("\nAverage Price by Number of Bedrooms:")
print(df.groupby('bedrooms')['price'].mean().sort_values(ascending=False))

print("\nAverage Price by Main Road Access:")
print(df.groupby('mainroad')['price'].mean())

print("\nAverage Price by Preferred Area:")
print(df.groupby('prefarea')['price'].mean())

# 12. Outlier Detection (using IQR method)
print("\n12. OUTLIER DETECTION")
print("-" * 80)
for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")

# ============================================================================
# DATA VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS...")
print("="*80)

# Create a directory for saving plots
import os
os.makedirs('plots', exist_ok=True)

# 13. Histograms for Numerical Features
print("\n13. Generating Histograms...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.ravel()
for idx, col in enumerate(numerical_cols):
    axes[idx].hist(df[col], bins=30, edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel('Frequency')
plt.tight_layout()
plt.savefig('plots/histograms.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Histograms saved to plots/histograms.png")

# 14. Box Plots for Outlier Detection
print("\n14. Generating Box Plots...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.ravel()
for idx, col in enumerate(numerical_cols):
    axes[idx].boxplot(df[col])
    axes[idx].set_title(f'Box Plot of {col}', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel(col)
plt.tight_layout()
plt.savefig('plots/boxplots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Box plots saved to plots/boxplots.png")

# 15. Correlation Heatmap
print("\n15. Generating Correlation Heatmap...")
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, fmt='.2f')
plt.title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Correlation heatmap saved to plots/correlation_heatmap.png")

# 16. Scatter Plots for Feature Relationships
print("\n16. Generating Scatter Plots...")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
# Price vs Area
axes[0, 0].scatter(df['area'], df['price'], alpha=0.5)
axes[0, 0].set_xlabel('Area (sq ft)')
axes[0, 0].set_ylabel('Price (PKR)')
axes[0, 0].set_title('Price vs Area')

# Price vs Bedrooms
axes[0, 1].scatter(df['bedrooms'], df['price'], alpha=0.5)
axes[0, 1].set_xlabel('Number of Bedrooms')
axes[0, 1].set_ylabel('Price (PKR)')
axes[0, 1].set_title('Price vs Bedrooms')

# Price vs Bathrooms
axes[1, 0].scatter(df['bathrooms'], df['price'], alpha=0.5)
axes[1, 0].set_xlabel('Number of Bathrooms')
axes[1, 0].set_ylabel('Price (PKR)')
axes[1, 0].set_title('Price vs Bathrooms')

# Price vs Parking
axes[1, 1].scatter(df['parking'], df['price'], alpha=0.5)
axes[1, 1].set_xlabel('Number of Parking Spaces')
axes[1, 1].set_ylabel('Price (PKR)')
axes[1, 1].set_title('Price vs Parking')
plt.tight_layout()
plt.savefig('plots/scatter_plots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Scatter plots saved to plots/scatter_plots.png")

# 17. Pairwise Feature Relationships
print("\n17. Generating Pair Plot (sample)...")
# Sample data for pair plot (too many points can be slow)
sample_df = df.sample(min(100, len(df)), random_state=42)
sns.pairplot(sample_df[numerical_cols], diag_kind='kde')
plt.savefig('plots/pairplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Pair plot saved to plots/pairplot.png")

# 18. Price Distribution
print("\n18. Generating Price Distribution...")
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=50, edgecolor='black', alpha=0.7, color='skyblue')
plt.xlabel('Price (PKR)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of House Prices', fontsize=14, fontweight='bold')
plt.axvline(df['price'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: PKR {df["price"].mean():,.0f}')
plt.axvline(df['price'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: PKR {df["price"].median():,.0f}')
plt.legend()
plt.tight_layout()
plt.savefig('plots/price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Price distribution saved to plots/price_distribution.png")

# 19. Categorical Feature Analysis
print("\n19. Generating Categorical Feature Analysis...")
n_cats = len(categorical_cols)
n_cols = 3
n_rows = (n_cats + n_cols - 1) // n_cols  # Ceiling division
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6*n_rows))
axes = np.array(axes).flatten()  # Ensure axes is always a 1D array
for idx, col in enumerate(categorical_cols):
    value_counts = df[col].value_counts()
    axes[idx].bar(value_counts.index, value_counts.values, color='steelblue')
    axes[idx].set_title(f'{col} Distribution', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel('Count')
    axes[idx].tick_params(axis='x', rotation=45)
# Hide unused subplots
for idx in range(n_cats, len(axes)):
    axes[idx].axis('off')
plt.tight_layout()
plt.savefig('plots/categorical_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Categorical distributions saved to plots/categorical_distribution.png")

# 20. Price by Categorical Features
print("\n20. Generating Price by Categorical Features...")
n_cats = len(categorical_cols)
n_cols = 3
n_rows = (n_cats + n_cols - 1) // n_cols  # Ceiling division
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6*n_rows))
axes = np.array(axes).flatten()  # Ensure axes is always a 1D array
for idx, col in enumerate(categorical_cols):
    price_by_cat = df.groupby(col)['price'].mean().sort_values(ascending=False)
    axes[idx].bar(price_by_cat.index, price_by_cat.values, color='coral')
    axes[idx].set_title(f'Average Price by {col}', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel('Average Price (PKR)')
    axes[idx].tick_params(axis='x', rotation=45)
    # Add value labels on bars
    for i, v in enumerate(price_by_cat.values):
        axes[idx].text(i, v, f'PKR {v/1e6:.1f}M', ha='center', va='bottom', fontsize=9)
# Hide unused subplots
for idx in range(n_cats, len(axes)):
    axes[idx].axis('off')
plt.tight_layout()
plt.savefig('plots/price_by_categorical.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Price by categorical features saved to plots/price_by_categorical.png")

print("\n" + "="*80)
print("EDA COMPLETE! All visualizations saved to 'plots' directory.")
print("="*80)

# ============================================================================
# DATA PREPROCESSING
# ============================================================================

print("\n" + "="*80)
print("DATA PREPROCESSING")
print("="*80)

# Create a copy for preprocessing
df_processed = df.copy()

# Handle missing values (if any)
print("\n1. Handling Missing Values...")
if df_processed.isnull().sum().sum() > 0:
    # For numerical columns, fill with median
    for col in numerical_cols:
        if df_processed[col].isnull().sum() > 0:
            df_processed[col].fillna(df_processed[col].median(), inplace=True)
    # For categorical columns, fill with mode
    for col in categorical_cols:
        if df_processed[col].isnull().sum() > 0:
            df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    print("✓ Missing values handled")
else:
    print("✓ No missing values to handle")

# Encode categorical variables
print("\n2. Encoding Categorical Variables...")
label_encoders = {}

# Binary categorical variables (yes/no) - use Label Encoding
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col])
    label_encoders[col] = le

# Multi-category variable (furnishingstatus) - use One-Hot Encoding
df_processed = pd.get_dummies(df_processed, columns=['furnishingstatus'], prefix='furnishing', drop_first=True)
print("✓ Categorical variables encoded")

# Separate features and target
X = df_processed.drop('price', axis=1)
y = df_processed['price']

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Feature Scaling
print("\n3. Feature Scaling...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
print("✓ Features scaled using StandardScaler")

# Train-Test Split
print("\n4. Train-Test Split...")
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")
print("✓ Data split completed")

# ============================================================================
# MACHINE LEARNING MODEL TRAINING
# ============================================================================

print("\n" + "="*80)
print("MACHINE LEARNING MODEL TRAINING")
print("="*80)

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
    'Decision Tree Regressor': DecisionTreeRegressor(random_state=42, max_depth=10)
}

results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Metrics
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    results[name] = {
        'model': model,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mae': train_mae,
        'test_mae': test_mae
    }
    
    print(f"  Training RMSE: {train_rmse:,.2f}")
    print(f"  Testing RMSE: {test_rmse:,.2f}")
    print(f"  Training R²: {train_r2:.4f}")
    print(f"  Testing R²: {test_r2:.4f}")
    print(f"  Training MAE: {train_mae:,.2f}")
    print(f"  Testing MAE: {test_mae:,.2f}")

# Select best model (based on test R² score)
best_model_name = max(results.keys(), key=lambda x: results[x]['test_r2'])
best_model = results[best_model_name]['model']

print("\n" + "="*80)
print(f"BEST MODEL: {best_model_name}")
print(f"Test R² Score: {results[best_model_name]['test_r2']:.4f}")
print(f"Test RMSE: {results[best_model_name]['test_rmse']:,.2f}")
print("="*80)

# Save the best model and preprocessing objects
print("\nSaving model and preprocessing objects...")
with open('model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

# Save feature names
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)

print("✓ Model and preprocessing objects saved")

# Save results to CSV
results_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Train_RMSE': [results[m]['train_rmse'] for m in results.keys()],
    'Test_RMSE': [results[m]['test_rmse'] for m in results.keys()],
    'Train_R2': [results[m]['train_r2'] for m in results.keys()],
    'Test_R2': [results[m]['test_r2'] for m in results.keys()],
    'Train_MAE': [results[m]['train_mae'] for m in results.keys()],
    'Test_MAE': [results[m]['test_mae'] for m in results.keys()]
})
results_df.to_csv('model_results.csv', index=False)
print("✓ Model results saved to model_results.csv")

print("\n" + "="*80)
print("MODEL TRAINING COMPLETE!")
print("="*80)

