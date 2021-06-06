from django.db import models
import pandas as pd
import matplotlib.pyplot as plt
# Create your models here.
import seaborn as sns
from django.shortcuts import render,redirect
import pickle
import json
from django.http import HttpResponse, JsonResponse
import os

data = pd.read_csv('./telecom_users.csv')
print(data)
y = data['Churn']
data.drop(['No','customerID','Churn'],axis=1,inplace=True)
data = pd.get_dummies(data,columns=['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
       'PaperlessBilling', 'PaymentMethod'],drop_first = True)
data = data.drop(['TotalCharges'],axis=1)
y=y.replace({"Yes":1,"No":0})


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=0)
m = {}

def training(request):
    if 'logit' in request.POST:
        
        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(random_state=0).fit(X_train, y_train)
        filename = 'lg.sav'
        pickle.dump(clf, open(filename, 'wb')) 
         
        return render(request,'index.html')

    if 'xgb' in request.POST:
        from xgboost import XGBClassifier
        xgb = XGBClassifier(learning_rate = 0.01,n_estimators=1000).fit(X_train, y_train)
        file_name = 'xgb.sav'
        pickle.dump(xgb,open(file_name,'wb'))
        return render(request,'index.html')

def testing(request):
    if 'lg' in request.POST:
        filename = 'lg.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(X_test)
        
        print(y_pred)
        y_pred = pd.DataFrame(y_pred,columns=['output'])
        y_pred.to_csv('lg.csv')
        
        filename = 'lg.csv'
        response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')               
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % 'lg.csv'
        return response
    
    if 'xg' in request.POST:
        filename = 'xgb.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(X_test)
        
        print(y_pred)
        y_pred = pd.DataFrame(y_pred,columns=['output'])
        y_pred.to_csv('xgb.csv')
        
        f = 'xgb.csv'
        response = HttpResponse(open(f, 'rb').read(), content_type='text/csv')               
        response['Content-Length'] = os.path.getsize(f)
        response['Content-Disposition'] = 'attachment; filename=%s' % 'xgb.csv'
        return response

def eval(request):

    if 'metric' in request.POST:

        loaded_model = pickle.load(open('lg.sav', 'rb'))
        y_pred = loaded_model.predict(X_test)
        
        from sklearn.metrics import accuracy_score, precision_score,f1_score
        acc = accuracy_score(y_pred,y_test)
        f1 = f1_score(y_test, y_pred, average='macro')
        f = {
            'accuracy':acc,
            'f1':f1
        }
        print(acc)
        # print(m['f1'])
        return render(request,'index.html',f)

    if 'xg_metric' in request.POST:
        loaded_model = pickle.load(open('xgb.sav', 'rb'))
        y_pred = loaded_model.predict(X_test)
        
        from sklearn.metrics import accuracy_score, precision_score,f1_score
        acc = accuracy_score(y_pred,y_test)
        f1 = f1_score(y_test, y_pred, average='macro')
        f = {
            'accuracy':acc,
            'f1':f1
        }
        print(acc)
        # print(m['f1'])
        return render(request,'index.html',f)


