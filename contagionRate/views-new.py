from django.shortcuts import render
from django.http import HttpResponse
import requests, re, math
import matplotlib.pyplot as plt 
import numpy as np; np.random.seed(1)
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
from datetime import datetime, timedelta
from threading import Thread

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

  results = {}


  def scrape_worldometers():
    url_alt = 'https://www.worldometers.info/coronavirus/country/israel/'
    req = requests.get(url_alt, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    #print(soup)
    mydivs = soup.find_all("div", class_="maincounter-number")
    #print(mydivs)
    divs = [ele.text.strip() for ele in mydivs]
    last_stat = divs[0]
    #print(last_stat)

    last_stat = re.sub(r'<div>.*>([\d,])<.*</div>', r'\1', last_stat, 0).replace(',', '')
    #print(last_stat)
    results['worldometers'] = last_stat


  threads = []
 
  process = Thread(target=scrape_worldometers, args=[])
  process.start()
  threads.append(process)

  for process in threads:
    process.join()
 
  last_stat = results['worldometers']
  
  
  today = datetime.today().strftime('%d-%m')
  fileHandle = open ( './data.txt',"r" )
  lineList = fileHandle.readlines()
  fileHandle.close()
  x = re.search(today+r'\s\d', lineList[-1])
  if x is None:
      f = open("./data.txt", "a")
      f.write(today + " " + last_stat + "\n")
      f.close()


  realDatesList = []
  datesList = []
  numSickList = []


  from urllib.request import urlopen
  file = open("filename","w")
  url = urlopen("url")
  for line in url:
      file.write(line + '\n')
  file.close()



  with open("./data.txt") as datafile:
    for line in datafile:
      s = line.split()
      datesList.append(s[0])
      numSickList.append(s[1])

  

  print(datesList)
  print(numSickList)


  plt.rcParams.update({'font.size': 16})
  DAY_RATE=3
  START_RANGE=0

  sickRate=[]
  labels=[]
  for i in range(START_RANGE, len(numSickList)-DAY_RATE):
      sickRate.append( int(numSickList[i+DAY_RATE]) / int(numSickList[i]))
      #print(datesList[i+DAY_RATE] + " : " + numSickList[i+DAY_RATE] + "/" + numSickList[i] + "= " + str(sickRate[i-4]))
      labels.append("<table><tr><td>" + numSickList[i+DAY_RATE] + "</td></tr><tr><td>" + numSickList[i] + "</td></tr><tr><td><b>" + str(round(sickRate[i],3)) + "</b></td></tr></table>")
      i=i+1

  # x axis values
  x = datesList[START_RANGE+DAY_RATE:len(datesList)]
  # corresponding y axis values 

  y = sickRate
  #print(x)
  #print(y)


  # plotting the points  
  graph = plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3, 
            marker='o', markerfacecolor='blue', markersize=20) 
    

  # setting x and y axis range 
  plt.ylim(0.95, 1.1) 
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
  current_sickRate = round(sickRate[len(sickRate)-1], 3)
  current_sick = numSickList[len(numSickList)-1]
  #future_sick = float(current_sick) * math.pow(current_sickRate, 10)

  '''
  last = len(numSickList)-1
  factor_two = int(current_sick)/2
  past_sick = numSickList[last-1]
  i = 0
  j = last-1
  while int(past_sick) > int(factor_two) and j>=0:
    #print('past:'+past_sick)
    i+=1 
    j-=1
    past_sick = numSickList[j]

  p = last-i
  #print( 'factor_two: ' +  str(factor_two))
  #print( 'past_sick: ' +  str(past_sick))
  #print("i: " + str(i))
  days_to_multiple = i
  mod = int(factor_two) - int(past_sick)
  #print('mod: ' + str(mod))

  avg = (float(current_sick)- float(numSickList[p]))/float(i)
  #print('numSickList[p]: ' + numSickList[p])
  #print('avg : ' + str(avg))
  factor_mod = mod/avg
  #print('factor_mod : ' + str(factor_mod))

  total_mult_days = float(days_to_multiple) + round(factor_mod, 2)
  #ax.set_title('[ 3-day Contagion Rate: ' + str(current_sickRate) + ']  [ In 30 days, total of: ' + f'{round(future_sick):,}' + ' sick ]  [ Number of sick multiplies every ' + str(total_mult_days) + ' days ]')
  '''
  
  today_sick = float(current_sick)
  yesterday_sick = float(numSickList[len(numSickList)-2])
  next_day_sick = float(current_sick)
  day_by_day_sickRate = today_sick/yesterday_sick
  #print(next_day_sick)
  i = 0
  while next_day_sick < 2.0 * float(current_sick) :
    i += 1
    next_day_sick = next_day_sick * day_by_day_sickRate
    #print(next_day_sick)

  total_mult_days = i
  future_sick = float(current_sick) * math.pow(day_by_day_sickRate, 30)

  ax.set_title('[ Contagion Rate - 3-day: ' + str(current_sickRate) + ' 1-day: ' + str(round(day_by_day_sickRate,3)) + ' ]  [ In 30 days, total of: ' + f'{round(future_sick):,}' + ' (+ ' + str(round(float(future_sick) - float(current_sick))) + ')  sick ]  [ Number of sick multiplies every ' + str(total_mult_days) + ' days ]')
        
  fig = plt.gcf()

  fig.set_size_inches(18.5, 7.5) 



  # function to show the plot 
  #print(mpld3.fig_to_html(fig))
  tooltip = plugins.PointHTMLTooltip(graph[0], labels,
                                      voffset=-80, hoffset=30, css=css)
  plugins.connect(fig, tooltip)

  #mpld3.show() 


  htmlText = ''' <html>\n<head> 
        <meta equiv="refresh" content="300">
        <meta name="MobileOptimized" content="width">
        <meta name="HandheldFriendly" content="true">
        <meta name="viewport" content="width=device-width">
        <meta name="viewport" content="width=device-width, initial-scale=1">'''
        
        
  htmlText += mpld3.fig_to_html(fig)
  htmlText += '</head>'
  #print(htmlText)
  #return HttpResponse(numSickList)
  #return HttpResponse(htmlText)
  print(htmlText)


index("aaa")