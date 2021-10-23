import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle


df = pd.read_csv('models\clean_data.csv')
X= df.drop('price', axis= 1)
y= df.price
categorical_features = ['genre', 'format']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')
preprocessor = ColumnTransformer(transformers=[('cat', categorical_transformer, categorical_features)])

model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  GradientBoostingRegressor())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                    random_state=2)

model.fit(X_train, y_train)
with open("models\model.pkl", "wb") as f:
    pickle.dump(model, f)

