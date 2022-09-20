from email import message
from django.shortcuts import render
import requests
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView

class currentWeather(APIView):
    #Getting the current weather details
    def get(self,request):
        s=service()
        json_data=s.getJson(request)

        #Checking for correct data
        if(json_data['cod']!='200'):
            return Response(json_data)
            
        try :
            group={}
            city=json_data['city']
            #List contains 8 elements
            #extracting the first list for default details
            list=json_data['list'][0]

            #Adding cityName, Time Zone (secs), Coord to group
            group.update({'cityName':city['name']})
            group.update({'country':city['country']})
            group.update({'timezone':str(datetime.timedelta(seconds=city['timezone']))})
            group.update({'lat':city['coord']['lat']})
            group.update({'lon':city['coord']['lon']})

            #Extracting the date in yyyy-mm-dd format from dt_txt
            date=str(list['dt_txt'])[0:10]

            #Adding date,day,max and min temp, pressure, humidity,windspeed and description
            group.update({'day':s.getDay(date)})
            group.update({'date':date})
            group.update({'maxTemp':list['main']['temp_max']})
            group.update({'minTemp':list['main']['temp_min']})
            group.update({'pressure':list['main']['pressure']})
            group.update({'humidity':list['main']['humidity']})
            group.update({'windSpeed':list['wind']['speed']})
            group.update({'description':list['weather'][0]['description']})

            #Icon Id is needed to diplay the icon form iconUrl
            group.update({'icon':list['weather'][0]['icon']})
            #Cod and status message for conformation at front end
            group.update({'cod':200})
            group.update({'message':'call successful'})
            return Response(group)

        except : 
            return Response({'cod': '404', 'message': 'city not found'})
    
class currentWeatherChart(APIView):
    # Getting parameters for chart of selected date
    def get(self,request):
        s=service()
        json_data=s.getJson(request)

        #Checking for correct data
        if(json_data['cod']!='200'):return Response(json_data)

        try :

            target_date=request.GET.get('date')

            next_date=str(datetime.datetime(int(target_date[0:4]),int(target_date[5:7]),int(target_date[8:10]))+datetime.timedelta(days = 1))[0:10]
            #Temparature and WindSpeed data are plotted aganist TimeStamps
            temparatureData=[]
            timeStampdata=[]
            windSpeedData=[]
            humidityData=[]

            for item in json_data['list']:
                date=str(item['dt_txt'])[0:10]
                if(date==target_date):
                    timeStampdata.append(str(int(item['dt_txt'][11:13]))+':00')
                    temparatureData.append(item['main']['temp'])
                    humidityData.append(item['main']['humidity'])
                    windSpeedData.append(item['wind']['speed'])
                elif(date==next_date):
                    #if date is next_data that is the end data needed
                    time=int(item['dt_txt'][11:13])
                    if time==0:timeStampdata.append('24:00')
                    else: timeStampdata.append(time+':00')
                    temparatureData.append(item['main']['temp'])
                    humidityData.append(item['main']['humidity'])
                    windSpeedData.append(item['wind']['speed'])
                    break

            group={'timeStampdata':timeStampdata,'temparatureData':temparatureData,'windSpeedData':windSpeedData,'humidityData':humidityData,'date':target_date}

            return Response(group)

        except : return Response({'cod': '404', 'message': 'date not found'})

class forecastWeather(APIView):
    def get(self,request):
        s=service()
        json_data=s.getJson(request)

        #Checking for correct data
        if(json_data['cod']!='200'):return Response(json_data)

        try :

            group=[]

            target_date=json_data['list'][0]['dt_txt'][0:10]
            next_date=str(datetime.datetime(int(target_date[0:4]),int(target_date[5:7]),int(target_date[8:10]))+datetime.timedelta(days = 1))[0:10]
            #Forecasting details should be displayed from next date to choosen date
            target_date=next_date

            for item in json_data['list']:
                if(target_date==item['dt_txt'][0:10] and int(item['dt_txt'][11:13])==9):

                    #date holds the data of each day of forecast
                    data={}
                    url="http://openweathermap.org/img/wn/"+str(item['weather'][0]['icon'])+"@2x.png"
                    data.update({'iconUrl':url})
                    data.update({'date':target_date})
                    data.update({'day':s.getDay(target_date)})
                    data.update({'temp':item['main']['temp_max']})
                    data.update({'pressure':item['main']['pressure']})
                    data.update({'humidity':item['main']['humidity']})
                    data.update({'windSpeed':item['wind']['speed']})
                    group.append(data)

                    #After the data is put in group the target_date is updated to next_date
                    next_date=str(datetime.datetime(int(target_date[0:4]),int(target_date[5:7]),int(target_date[8:10]))+datetime.timedelta(days = 1))[0:10]
                    target_date=next_date
            if(len(group)!=5):
                item=json_data['list'][len(json_data['list'])-1]
                data={}
                url="http://openweathermap.org/img/wn/"+str(item['weather'][0]['icon'])+"@2x.png"
                data.update({'iconUrl':url})
                data.update({'date':target_date})
                data.update({'day':s.getDay(target_date)})
                data.update({'temp':item['main']['temp_max']})
                data.update({'pressure':item['main']['pressure']})
                data.update({'humidity':item['main']['humidity']})
                data.update({'windSpeed':item['wind']['speed']})
                group.append(data)
            
            return Response(group)
        except : return Response({'cod': '404', 'message': 'city not found'})

class service:

    def getJson(self,request):
        try :
            if ( 'city' in request.GET ):
                city=request.GET.get("city")
                link='http://api.openweathermap.org/data/2.5/forecast?q='+city+'&APPID=b0b2a8c6eb68cf455d2b353ed0537b55&units=metric'
                data=requests.get(link)
                json_data=data.json()
                if(json_data['city']['name']==''):return {'cod': '404', 'message': 'city not found'}
                return json_data
            if (('lat' in request.GET) and ('lon' in request.GET)):
                lat=request.GET.get("lat")
                lon=request.GET.get("lon")
                link='http://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(lon)+'&APPID=b0b2a8c6eb68cf455d2b353ed0537b55&units=metric'
                data=requests.get(link)
                json_data=data.json()
                if(json_data['city']['name']==''):return {'cod': '404', 'message': 'city not found'}
                return json_data
            else:
                return {'cod':'400','message':'Error no Input Found'}
        except:
            return {'cod':'400','message':'Incomplete Request'}

    #getDay() take returns the day pf corresponding date String
    def getDay(self,dateString):
        #date is in yyyy-mm-dd format
        Day={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
        yyyy=int(dateString[0:4])
        mm=int(dateString[5:7])
        dd=int(dateString[8:10])
        #weekday() returns a number for day like 0 for monday or 6 for sunday
        day = datetime.datetime(yyyy,mm,dd).weekday()
        return Day[day]
