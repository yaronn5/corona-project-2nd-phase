from django.shortcuts import render
from django.http import HttpResponse
import requests, re
import matplotlib.pyplot as plt 
import numpy as np; np.random.seed(1)
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins

# Create your views here.



def index(request):

    # Define some CSS to control our custom labels
    css = """
    table
    {
      border-collapse: collapse;
    }
    th
    {
      color: #ffffff;
      background-color: #000000;
    }
    td
    {
      background-color: #FFA500;
    }
    table, th, td
    {
      font-family:Arial, Helvetica, sans-serif;
      font-size:20;
      border: 1px solid black;
      text-align: right;
    }
    """

    # Set headers
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

    from bs4 import BeautifulSoup

    ...
    url = "http://corona.mako.co.il"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    #print(soup)

    tag = soup.find("script")
    #print(tag)

    script = soup.findAll('script')[0].string


    plt.rcParams.update({'font.size': 22})
    DAY_RATE=3
    START_RANGE=4
    varList = script.replace("\r\n", "").replace(";","").replace(" ", "").split("var")
    allValues = " "
    allValues = allValues.join(varList)
    #print(numSick)
    numSick = re.sub(r'.*_globalGraphValues=\[(.*?)\].*', r'\1', allValues, 0)
    dates = re.sub(r'.*_globalGraphKeys=\[(.*?)\].*', r'\1', allValues, 0).replace('"', '').replace('.20','')
    numSickList = numSick.split(',')
    datesList = dates.split(',')
    #print(numSickList)
    #print(datesList)

    sickRate=[]
    labels=[]
    for i in range(START_RANGE, len(numSickList)-DAY_RATE):
        sickRate.append( int(numSickList[i+DAY_RATE]) / int(numSickList[i]))
        #print(datesList[i+DAY_RATE] + " : " + numSickList[i+DAY_RATE] + "/" + numSickList[i] + "= " + str(sickRate[i-4]))
        labels.append("<table><tr><td>" + numSickList[i+DAY_RATE] + " / " + numSickList[i] + " = " + str(round(sickRate[i-4],2)) + "</td></tr></table>")
        i=i+1

    # x axis values
    x = datesList[START_RANGE+DAY_RATE:len(datesList)]
    # corresponding y axis values 

    y = sickRate
    #print(x)
    #print(y)


    # plotting the points  
    graph = plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3, 
             marker='o', markerfacecolor='blue', markersize=12) 
      

    # setting x and y axis range 
    plt.ylim(0, 3) 
    plt.xlim(0,len(datesList)-START_RANGE) 


    #fig, ax = plt.subplots()

    ax = plt.gca()
    ax.set_xticklabels(x)
    ax.set_xticks(x)
      
    # naming the x axis 
    plt.xlabel('x - Date') 
    # naming the y axis 
    plt.ylabel('y - 3 day rate') 
      
    # giving a title to my graph 
    current_sickRate = round(sickRate[len(sickRate)-1], 2)
    current_sick = numSickList[len(numSickList)-1]
    future_sick= current_sick
    for i in range(0,10):
        future_sick = float(future_sick) * current_sickRate
    plt.title('Contagion 3-Day-Rate: ' + str(current_sickRate) + ' - 30-days projection: ' + f'{round(future_sick):,}' + ' sick' )
      
    fig = plt.gcf()

    fig.set_size_inches(18.5, 7.5) 



    # function to show the plot 
    #print(mpld3.fig_to_html(fig))
    tooltip = plugins.PointHTMLTooltip(graph[0], labels,
                                       voffset=10, hoffset=40, css=css)
    plugins.connect(fig, tooltip)

    #mpld3.show() 
    
    htmlText = ''' <html>\n<head> 
          <meta name="MobileOptimized" content="width">
          <meta name="HandheldFriendly" content="true">
          <meta name="viewport" content="width=device-width">
          <meta name="viewport" content="width=device-width, initial-scale=1">'''
          
          
    htmlText += mpld3.fig_to_html(fig)
    htmlText += '</head>'

    return HttpResponse(htmlText)