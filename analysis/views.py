from django.shortcuts import render

# Create your views here.


def analysis_select(request) :
 

    return render(request,"analysis/analysis-select.html")


def analysis_result(request) :

    return render(request,"analysis/analysis-result.html")
