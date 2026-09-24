import json
import requests
import pandas as pd
import streamlit as st

# Setting up the page
st.title("SuperKart Sales Prediction")
st.write(
    "This app predicts the total sales revenue a product will generate "
    "in a given store, using SuperKart's trained ML model."
)

# NOTE: Replace this with your own backend's forwarded Codespace URL for port 7860
model_root_url = "_____"

online_url = model_root_url + "/v1/predict"
batch_url = model_root_url + "/v1/predictbatch"

tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

# ---------------- Single (online) prediction ----------------
with tab1:
    st.header("Enter product & store details")

    Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
    Product_Sugar_Content = st.selectbox(
        "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
    )
    Product_Allocated_Area = st.number_input(
        "Product Allocated Area (ratio)", min_value=0.0, max_value=1.0, value=0.027
    )
    Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
    Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    Store_Location_City_Type = st.selectbox(
        "Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"]
    )
    Store_Type = st.selectbox(
        "Store Type",
        ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"],
    )
    Product_Id_char = st.selectbox("Product Id Prefix", ["FD", "NC", "DR"])
    Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
    Product_Type_Category = st.selectbox(
        "Product Type Category", ["Perishables", "Non Perishables"]
    )

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": Product_Weight,
            "Product_Sugar_Content": Product_Sugar_Content,
            "Product_Allocated_Area": Product_Allocated_Area,
            "Product_MRP": Product_MRP,
            "Store_Size": Store_Size,
            "Store_Location_City_Type": Store_Location_City_Type,
            "Store_Type": Store_Type,
            "Product_Id_char": Product_Id_char,
            "Store_Age_Years": Store_Age_Years,
            "Product_Type_Category": Product_Type_Category,
        }

        try:
            response = requests.post(online_url, json=payload)
            result = response.json()
            st.success(
                f"Predicted Sales: {result['Predicted_Product_Store_Sales_Total']:.2f}"
            )
        except Exception as e:
            st.error(f"Something went wrong calling the API: {e}")

# ---------------- Batch prediction ----------------
with tab2:
    st.header("Upload a CSV for batch prediction")
    st.write(
        "The CSV must contain the columns: Product_Weight, Product_Sugar_Content, "
        "Product_Allocated_Area, Product_MRP, Store_Size, Store_Location_City_Type, "
        "Store_Type, Product_Id_char, Store_Age_Years, Product_Type_Category"
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(batch_df.head())

        if st.button("Run Batch Prediction"):
            files = {"file": batch_df.to_csv(index=False).encode("utf-8")}
            try:
                response = requests.post(batch_url, files=files)
                predictions = json.loads(response.text)
                batch_df["Predicted_Product_Store_Sales_Total"] = [
                    predictions[str(i)] for i in range(len(batch_df))
                ]
                st.write("Predictions:")
                st.dataframe(batch_df)
            except Exception as e:
                st.error(f"Something went wrong calling the API: {e}")
