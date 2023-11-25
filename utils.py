def get_features_domain(dataset):
    numeric_cols = []
    categorical_cols = []

    for col in dataset.columns:
        if((dataset[col].dtype == 'int64') or (dataset[col].dtype == 'float64')):
            numeric_cols.append(col)
        else:
            categorical_cols.append(col)
    return numeric_cols, categorical_cols