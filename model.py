import sqlite3
import pandas as pd
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from lightgbm import LGBMClassifier
import pickle


# 데이터베이스에 접속한다.
con = sqlite3.connect("./Diabetes.db")
# pandas의 read_sql함수를 이용해서 데이터베이스를 데이터프레임의 형태로 불러온다.
Diabetes = pd.read_sql("SELECT * FROM Diabetes_ML", con, index_col=None)

# index column을 제거해준다.
Diabetes = Diabetes.drop(columns = ['index'])
Diabetes

# feature들중 AnyHealthcare, CholCheck, NoDocbcCost은 제거해준다.
Diabetes = Diabetes.copy().drop(columns = ['AnyHealthcare', 'CholCheck', 'NoDocbcCost'])

#target을 설정해준다.
target = 'Diabetes_012'

#데이터를 훈련/테스트 세트로 분리한다.(train/test = 90%/10%의 비율로 나누어 주었다.)
train, test = train_test_split(Diabetes, train_size = 0.90, test_size = 0.10,
                               stratify = Diabetes[target], random_state = 42)

#target과 학습할 feature를 분리해준다.
y_train = train[target]
X_train = train.copy().drop(columns = [target])

y_test = test[target]
X_test = test.copy().drop(columns = [target])

# encoder, imputer를 preprocessing으로 묶었다. 후에 eli5 permutation 계산에 사용한다.
pipe = Pipeline([
    ('preprocessing', make_pipeline(SimpleImputer())),
    ('lbgm', LGBMClassifier(random_state = 42,
                            n_jobs = -1,
                            num_class = 3,
                            application = 'multiclass',
                            is_unbalance = True,
                            learning_rate = 0.1,
                            class_weight = 'balanced',
                            metric = 'multi_logloss',
                            max_depth = 14,
                            n_estimators = 498,
                            num_leaves = 58
                            ))
])

# 학습을 진행한다.
pipe.fit(X_train, y_train)


# 학습한 모델을 피클링 해준다.
with open('model.pkl','wb') as pickle_file:
    pickle.dump(pipe, pickle_file)