import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PopupComponent } from './app/popup/popup.component';
import { CurrentWeather, CurrentWeatherChart, EachDay, InputObj } from './app/Weather';

@Injectable({
  providedIn: 'root'
})
export class WeatherAppService
{

  constructor(private httpClient:HttpClient,private dialog:MatDialog) { }

  cityName:String="";
  emptyCurrentWeather=new CurrentWeather();
  locationTime:String='';
  tempCurrentWeather=new CurrentWeather();
  currentWeather=new CurrentWeather();
  currentWeatherChart=new CurrentWeatherChart();
  temp:any;
  forecasts:EachDay[]=[];
  chartDataTemp:any;
  chartLabels = [];
  display=false;

  setCurrentWeather(inputObj:InputObj)
  {

    if(inputObj.cityName!="")
    {
      const url='http://127.0.0.1:8000/weatherApp/currentWeather/?city='+inputObj.cityName;
      this.httpClient.get(url).subscribe( data =>
        {
          this.tempCurrentWeather.setCurrentWeather(data);
          if(this.tempCurrentWeather.cod=='200')
          {
            this.currentWeather=this.tempCurrentWeather;
            
            const urlf='http://127.0.0.1:8000/weatherApp/forecastWeather/?city='+inputObj.cityName;
            this.httpClient.get(urlf).subscribe( result => {this.temp=result;})

            const urlc='http://127.0.0.1:8000/weatherApp/currentWeatherChart/?city='+inputObj.cityName+"&date="+this.currentWeather.date;
            this.httpClient.get(urlc).subscribe( chartresult => {this.chartDataTemp=chartresult;})
          }
          else
          {
            this.display=false;
            this.dialog.open(PopupComponent,
            {
            data:{message:'City not found',id:3}
            })
          }

        })

      }

    else
    {

      let lats=String(inputObj.lat);
      let lons=String(inputObj.lon);
      const url='http://127.0.0.1:8000/weatherApp/currentWeather/?lat='+lats+'&lon='+lons;
      this.httpClient.get(url).subscribe( data =>
        {
            this.tempCurrentWeather.setCurrentWeather(data);
            if(this.tempCurrentWeather.cod=='200')
            {

              this.currentWeather=this.tempCurrentWeather;
              this.currentWeather.setCurrentWeather(data);
              this.cityName=this.currentWeather.cityName;

              const urlf='http://127.0.0.1:8000/weatherApp/forecastWeather/?lat='+lats+'&lon='+lons;
              this.httpClient.get(urlf).subscribe( result =>{this.temp=result;})

              const urlc='http://127.0.0.1:8000/weatherApp/currentWeatherChart/?lat='+lats+'&lon='+lons+"&date="+this.currentWeather.date;
              this.httpClient.get(urlc).subscribe( chartresult => {this.chartDataTemp=chartresult;})

            }

            else
            {
              this.display=false;
              this.dialog.open(PopupComponent,
                {
                data:{message:'Co-Ordinates Not Found',id:3}
                })
            }
        })
    }
  }


}
