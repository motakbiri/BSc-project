import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score ,fbeta_score,recall_score,precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn import preprocessing


data = pd.read_csv("data.csv")
data = data.drop('name',1)

#shuffle data
data = data.sample(frac=1).reset_index(drop=True)

#normalization
scaler = preprocessing.MinMaxScaler()
data[data.columns] = scaler.fit_transform(data[data.columns])



# 10 k-fold cross validation
kf = KFold(n_splits=10)
sum_acc_l = 0
sum_rec_l = 0
sum_per_l = 0
sum_acc_s = 0
sum_rec_s = 0
sum_per_s = 0

for train, test in kf.split(data.drop(['malware'], axis=1),data['malware']):
    train_data = data.iloc[train]
    test_data = data.iloc[test]

    x_train = train_data.drop(['malware'],1)
    y_train = train_data['malware']

    x_val = test_data.drop(['malware'],1)
    y_val = test_data['malware']


    #over sampling
    sm = SMOTE(random_state=12)
    x_train_res, y_train_res = sm.fit_sample(x_train, y_train)

    #logistic regression
    logistic = LogisticRegression()
    svm = SVC(probability=True)


    logistic.fit(x_train_res, y_train_res)
    svm.fit(x_train_res, y_train_res)


    y_predict_logistic = logistic.predict(x_val)
    #y_predict_logistic_con = logistic.predict_proba(x_val)

    y_predict_svm = svm.predict(x_val)
    #y_predict_svm_con = svm.predict_proba(x_val)
    #print y_predict_con
    # print y_predict


    sum_acc_l += accuracy_score(y_val, y_predict_logistic)
    sum_rec_l += recall_score(y_val, y_predict_logistic)
    sum_per_l += precision_score(y_val, y_predict_logistic)

    sum_acc_s += accuracy_score(y_val, y_predict_svm)
    sum_rec_s += recall_score(y_val, y_predict_svm)
    sum_per_s += precision_score(y_val, y_predict_svm)

print "Logistic Regression"
print "accuracy:  " + str(sum_acc_l/10)
print "recall:  " + str(sum_rec_l/10)
print "precision:  " + str(sum_per_l/10)
print "----------"
print "SVM"
print "accuracy:  " + str(sum_acc_s/10)
print "recall:  " + str(sum_rec_s/10)
print "precision:  " + str(sum_per_s/10)
