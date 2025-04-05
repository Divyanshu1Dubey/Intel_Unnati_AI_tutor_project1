import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

# ---------------- Page Config ----------------
st.set_page_config(page_title="📊 Enhanced EDA Dashboard", layout="wide")

# --------------- Custom Styling ---------------
st.markdown("""
<style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1581092160617-df59c0bf855f?auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        color: white;
    }
    .glass {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-top: 30px;
        color: white;
    }
    h1, h2, h3, h4 {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.title("📌 Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Visualizations", "Feature Importance", "PCA"])

st.markdown("<div class='glass'>", unsafe_allow_html=True)

# ---------------- Upload Data ----------------
st.title("📓 Enhanced Exploratory Data Analysis")

uploaded_file = st.file_uploader("📁 Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    if section == "Overview":
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        st.subheader("📐 Dataset Info")
        st.write("Shape:", df.shape)
        st.write("Columns:", df.columns.tolist())
        st.dataframe(df.describe(include='all'))

        st.subheader("📉 Missing Values (%)")
        st.dataframe(((df.isnull().sum() / df.shape[0]) * 100).reset_index().rename(columns={0: 'Missing %', 'index': 'Feature'}))

        st.subheader("🧹 Duplicate Records")
        st.write(f"Duplicate Rows: {df.duplicated().sum()}")

    elif section == "Visualizations":
        st.subheader("📊 Visual Analysis")

        tab1, tab2 = st.tabs(["Numerical Columns", "Categorical Columns"])

        with tab1:
            col = st.selectbox("📈 Select numeric column", numeric_cols)
            fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
            st.plotly_chart(fig)

            st.subheader("📏 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
            st.pyplot(fig)

        with tab2:
            st.subheader("📊 Categorical Columns")
            col = st.selectbox("Select a categorical column", categorical_cols)

            # Value counts for the selected categorical column
            value_counts_df = df[col].value_counts().reset_index()
            value_counts_df.columns = [col, 'count']  # Rename columns

            # Bar chart using Plotly
            fig = px.bar(value_counts_df, x=col, y='count', title=f"{col} Distribution")
            st.plotly_chart(fig)

            # Grouped bar chart if 'promoted' column exists
            if 'promoted' in df.columns:
                st.subheader(f"{col} vs Promoted")
                fig = px.histogram(df, x=col, color='promoted', barmode='group',
                                   title=f"{col} Distribution by Promotion Status")
                st.plotly_chart(fig)

        st.subheader("📦 Outlier Detection")
        selected_col = st.selectbox("Choose column for outlier check", numeric_cols)
        fig, ax = plt.subplots()
        sns.boxplot(df[selected_col], color='tomato')
        ax.set_title(f'Outliers in {selected_col}')
        st.pyplot(fig)

        st.subheader("🔍 Pairplot")
        if st.checkbox("Enable Pairplot"):
            try:
                st.write("This may take a few seconds...")
                fig = sns.pairplot(df[numeric_cols + ['promoted']] if 'promoted' in df.columns else df[numeric_cols])
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"Pairplot failed: {e}")

    elif section == "Feature Importance":
        st.subheader("🧠 Feature Importance (Random Forest)")

        target_col = st.selectbox("🎯 Select Target Variable", df.columns)
        features = [col for col in df.columns if col != target_col]

        # Encode non-numeric
        df_encoded = df.copy()
        le = LabelEncoder()
        for col in categorical_cols:
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

        try:
            X = df_encoded[features]
            y = df_encoded[target_col]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            importances = pd.DataFrame({'Feature': features, 'Importance': model.feature_importances_})
            importances = importances.sort_values(by='Importance', ascending=False)

            fig = px.bar(importances, x='Feature', y='Importance', color='Importance', title='Feature Importance')
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f"⚠️ Could not train model: {e}")

    elif section == "PCA":
        st.subheader("🔬 PCA - Dimensionality Reduction")

        if len(numeric_cols) >= 2:
            scaled = StandardScaler().fit_transform(df[numeric_cols].dropna())
            pca = PCA(n_components=2)
            pcs = pca.fit_transform(scaled)
            pca_df = pd.DataFrame(pcs, columns=['PC1', 'PC2'])
            if 'promoted' in df.columns:
                pca_df['promoted'] = df['promoted']
                fig = px.scatter(pca_df, x='PC1', y='PC2', color='promoted', title='PCA with Promoted')
            else:
                fig = px.scatter(pca_df, x='PC1', y='PC2', title='PCA of Dataset')
            st.plotly_chart(fig)
        else:
            st.warning("Need at least 2 numerical columns for PCA")

    st.markdown("___")

st.markdown("</div>", unsafe_allow_html=True)
