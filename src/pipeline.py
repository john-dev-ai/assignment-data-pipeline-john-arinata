import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def extract_data() -> pd.DataFrame:
    path = "data/raw/automobileEDA_dirty_training.csv"
    df = pd.read_csv(path)
    return df


def inspect_dataset(df: pd.DataFrame) -> None:

    print("\n" + "=" * 60)
    print("DATA INSPECTION")
    print("=" * 60)

    print("\n5 baris pertama:")
    print(df.head())

    print("\nUkuran dataset:")
    print(f"Rows : {df.shape[0]}")
    print(f"Cols : {df.shape[1]}")

    print("\nNama kolom:")
    print(df.columns.tolist())

    print("\nTipe data:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = df.isna().sum()
    print(missing[missing > 0])

    print(f"\nDuplicate records: {df.duplicated().sum()}")

    print("\nNilai unik kolom kategorikal:")

    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:
        values = df[col].dropna().unique().tolist()

        if len(values) <= 30:
            print(f"{col}: {values}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    data = df.copy()

    rows_before = len(data)
    missing_before = int(data.isna().sum().sum())

    data = data.drop_duplicates().reset_index(drop=True)
    data = data.drop(columns=["transaction_date"])

    categorical_cols = [
        "make",
        "aspiration",
        "num-of-doors",
        "body-style",
        "drive-wheels",
        "engine-location",
        "engine-type",
        "num-of-cylinders",
        "fuel-system",
        "horsepower-binned",
    ]

    for col in categorical_cols:
        data[col] = data[col].astype("string").str.strip().str.lower()

    for col in ["make", "num-of-doors", "horsepower-binned"]:
        data[col] = data[col].fillna(data[col].mode()[0])

    for col in ["stroke", "horsepower", "price"]:
        data[col] = data[col].fillna(data[col].median())

    rows_after = len(data)
    missing_after = int(data.isna().sum().sum())

    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)

    print(f"Rows before cleaning : {rows_before}")
    print(f"Rows after cleaning  : {rows_after}")
    print(f"Duplicates removed   : {rows_before - rows_after}")
    print(f"Missing before       : {missing_before}")
    print(f"Missing after        : {missing_after}")

    return data


def transform_data(data: pd.DataFrame) -> pd.DataFrame:

    data = data.copy()

    data["num-of-doors"] = np.select(
        [
            data["num-of-doors"].eq("two"),
            data["num-of-doors"].eq("four"),
        ],
        [
            0,
            1,
        ],
        default=np.nan,
    )

    data["num-of-cylinders"] = np.select(
        [
            data["num-of-cylinders"].eq("two"),
            data["num-of-cylinders"].eq("three"),
            data["num-of-cylinders"].eq("four"),
            data["num-of-cylinders"].eq("five"),
            data["num-of-cylinders"].eq("six"),
            data["num-of-cylinders"].eq("eight"),
            data["num-of-cylinders"].eq("twelve"),
        ],
        [
            0,
            1,
            2,
            3,
            4,
            6,
            10,
        ],
        default=np.nan,
    )

    data["num-of-cylinders"] = data["num-of-cylinders"] / 10

    data["horsepower_ordinal"] = np.select(
        [
            data["horsepower-binned"].eq("low"),
            data["horsepower-binned"].eq("medium"),
            data["horsepower-binned"].eq("high"),
        ],
        [
            0,
            1,
            2,
        ],
        default=np.nan,
    ).astype(np.int64)

    scaled_cols = [
        "symboling",
        "curb-weight",
        "num-of-cylinders",
        "engine-size",
        "horsepower",
        "peak-rpm",
        "city-mpg",
        "highway-mpg",
        "price",
    ]

    scaler = MinMaxScaler()

    data[scaled_cols] = scaler.fit_transform(data[scaled_cols])

    onehot_cols = [
        "body-style",
        "drive-wheels",
        "aspiration",
        "engine-type",
        "engine-location",
        "fuel-system",
    ]

    dummies = pd.get_dummies(data[onehot_cols], prefix=onehot_cols, dtype=int)

    print("\n Transformed Data:")
    print(data[["horsepower", "price", "horsepower_ordinal"]].head())

    base_cols = [
        "symboling",
        "normalized-losses",
        "num-of-doors",
        "wheel-base",
        "length",
        "width",
        "height",
        "curb-weight",
        "num-of-cylinders",
        "engine-size",
        "bore",
        "stroke",
        "compression-ratio",
        "horsepower",
        "peak-rpm",
        "city-mpg",
        "highway-mpg",
        "price",
        "city-L/100km",
        "diesel",
        "gas",
        "horsepower_ordinal",
    ]

    result = pd.concat([data[base_cols], dummies], axis=1)

    make_frequency = data["make"].value_counts(normalize=True)

    result["make_freq"] = data["make"].map(make_frequency)

    return result


def save_dataset(df: pd.DataFrame) -> None:

    path = "data/processed/automobileEDA_processed.csv"

    df.to_csv(path, index=False)

    print(f"\nProcessed dataset saved to: {path}")


def run_pipeline() -> None:

    df = extract_data()
    inspect_dataset(df)
    cleaned = clean_data(df)
    processed = transform_data(cleaned)
    save_dataset(processed)

    print(f"Final shape: {processed.shape}")
    print(f"Missing values: {processed.isna().sum().sum()}")


if __name__ == "__main__":
    run_pipeline()
