from django.shortcuts import render
import pandas as pd
# Create your views here.
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.template.response import TemplateResponse
import json 



def home(request):
    df = pd.read_csv("./telecom_users.csv")
    df = df[:10]
    # data = data.to_html()
    json_records = df.reset_index().to_json(orient ='records')
    arr = []
    arr = json.loads(json_records)
    contextt = {'d': arr}
    return  render(request,'index.html',contextt)




