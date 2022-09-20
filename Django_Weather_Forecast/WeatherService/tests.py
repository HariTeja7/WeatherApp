from django.test import TestCase, Client

class Test_currentWeather_WeatherService(TestCase):

#Testing with City Name as Inputs

    #Testing API with existing city name like 'chennai
    def test_currentWeather_with_proper_input_city(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?city=chennai')
        self.assertEquals(response.json()['cod'],200)
    
    #Testing API with non-existing city name like 'abc'
    def test_currentWeather_with_improper_input_city(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?city=abc')
        self.assertEquals(response.json()['cod'],'400')
    
    #Testing API with blank or no input city name like ''
    def test_currentWeather_with_no_input_city(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?city=')
        self.assertEquals(response.json()['cod'],'400')
    
    #Testing API with invalid city names; few cities have number Id like 123, so invalid city name can be a mixture of alphabets and numbers and connot be only numbers or alphabets
    def test_currentWeather_with_invalid_input_city(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?city=1bg2')
        self.assertEquals(response.json()['cod'],'400')

#Testing with Coords as Inputs

    #Testing API with existing Coords
    def test_currentWeather_with_proper_input_coords(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?lat=17.3753&lon=78.4744')
        self.assertEquals(response.json()['cod'],200)
    
    #Testing API with non-existing Coords
    def test_currentWeather_with_improper_input_coords(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?lat=90&lon=87')
        self.assertEquals(response.json()['cod'],'404')#Throws an Exception
    
    #Testing API with blank or no input Coords
    def test_currentWeather_with_no_input_coords(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?lat=&lon=')
        self.assertEquals(response.json()['cod'],'400')
    
    #Testing API with invalid coords
    def test_currentWeather_with_invalid_input_coords(self):
        client=Client()
        response=client.get('/weatherApp/currentWeather/?lat=2&lon=c34')
        self.assertEquals(response.json()['cod'],'400')

class Test_currentWeatherChart_WeatherService(TestCase):
    #Testing API with proper date format
    def test_currentWeatherChart_with_proper_date(self):
        client=Client()
        response=client.get('/weatherApp/currentWeatherChart/?city=Mumbai&date=2022-09-19')
        self.assertNotEquals(response.json()['timeStampdata'],[])
    
    #Testing API with imp
    def test_currentWeatherChart_with_improper_date(self):
        client=Client()
        response=client.get('/weatherApp/currentWeatherChart/?city=Mumbai&date=2022-0919')
        self.assertEquals(response.json()['timeStampdata'],[])
    
    def test_currentWeatherChart_with_invalid_coords(self):
        client=Client()
        response=client.get('/weatherApp/currentWeatherChart/?lat=90&lon=87&date=2022-09-19')
        self.assertEquals(response.json()['cod'],'404')

class Test_forecastWeather_WeatherService(TestCase):
    
    def test_forecastWeather_with_improper_city(self):
        client=Client()
        response=client.get('/weatherApp/forecastWeather/?city=cheai')
        self.assertEquals(response.json()['cod'],'400')
    
    def test_forecastWeather_with_no_city(self):
        client=Client()
        response=client.get('/weatherApp/forecastWeather/?city=')
        self.assertEquals(response.json()['cod'],'400')
    
    
    