import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression


def feature_importance(data):
    x_train, y_train = data.drop(columns=["rating"]), data["rating"]
    rgr = RandomForestRegressor()
    rgr.fit(x_train, y_train.values.ravel())
    importances = rgr.feature_importances_
    feature_names_agg = ["itemId", "item_genre", "userId", "rating_timestamp", "user_median_income",
                         "user_mean_income", "user_population", "user_occupation", "user_gender", "user_age",
                         "user_zip", "item_release_date"] + list(x_train)[64:82]
    importances_agg = [importances[0], sum(importances[1:20]), importances[20], importances[21],
                       importances[22], importances[23], importances[24], sum(importances[25:46]),
                       sum(importances[46:48]), sum(importances[48:53]), sum(importances[53:63]),
                       importances[63]] + importances[64:82]
    sorting_mask = np.array(importances_agg).argsort()[::-1]
    sorted_feature_names_agg = np.array(feature_names_agg)[sorting_mask]
    sorted_importances_agg = np.array(importances_agg)[sorting_mask] * 100
    forest_importances = pd.Series(sorted_importances_agg, index=sorted_feature_names_agg)

    return forest_importances


def feature_selection(data, num_features):
    x_train, y_train = data.drop(columns=["rating"]), data["rating"]
    selector = SelectKBest(f_regression, k=num_features)
    selector.fit(x_train, y_train)
    selected_columns = np.array(list(x_train))[selector.get_support()]
    x_train = pd.DataFrame(selector.transform(x_train), columns=selected_columns)

    return pd.concat([x_train, y_train], axis=1)
