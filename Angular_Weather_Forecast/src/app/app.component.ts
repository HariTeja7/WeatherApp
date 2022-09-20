import { Component, Input } from '@angular/core';
import { WeatherAppService } from 'src/weather-app.service';
import { InputObj } from './Weather';
import { MatDialog } from '@angular/material/dialog';
import { PopupComponent } from './popup/popup.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  constructor(private weatherAppService:WeatherAppService,private dialog:MatDialog) {
    //Re-assigns the current-time for every 1ms
    setInterval(() => { this.currentTime =new Date(); 
    this.display=this.weatherAppService.display;
    }, 1);
  }
  ngOnChanges(){
  }

  //It intializes the lat and long and location to default
  public ngOnInit(): void {
    this.getLocation();
  }
  //Blocks : Default Block, Serach Block, Current Weather, Forecast Weather, Chart

  title = 'WeatherApp';
  //Time for default location
  currentTime=new Date();
  //Time for  selected location
  locationTime:String=this.weatherAppService.locationTime;

  //Selected temp changes the scale
  selectedTemp:String='';
  tempScale=this.selectedTemp;
  
  //search-block
  //lat,lon and city
  cityName:String="";
  lat:number=this.weatherAppService.currentWeather.lat;
  lon:number=this.weatherAppService.currentWeather.lon;
  //currentLocation will be set by service class
  currentLocation=this.weatherAppService.currentWeather.cityName;

  // Current-Weather data
  currentWeather:any;

  //dispCurrentWeather
  display=this.weatherAppService.display;

  // Forecast Weathers data
  forecasts=this.weatherAppService.forecasts;

  //Chart Data and Attributes
  chartData=
  [
    {data:[],label:'Humidity in %',borderColor:'green'},
    {data: [],label:'Temperature '+'(1 unit = 5'+' °C)',borderColor:'yellow'},
    {data: [],label: ' Wind Speed '+'(1 unit = 5 m/s)',borderColor:'red'},
  ];;
  chartLabels = [];
  chartOptions = {responsive: true};
  lineChartPlugins = [];


  //Method to sort the 5 day weather forecast data
  sort()
  {
      let n=this.forecasts.length;
      for(let i=0;i<(this.forecasts.length)/2;i++)
      {
        let temp=this.forecasts[i];
        this.forecasts[i]=this.forecasts[n-1-i];
        this.forecasts[n-1-i]=temp;
      }
    }

  //Get Location gets the current position details from browser
    getLocation()
    {
      if (navigator.geolocation)
      {
        navigator.geolocation.getCurrentPosition((position) =>
        {
          if (position)
          {
            //Getting location coordinates from position{lat and lon}
            this.lat=position.coords.latitude;
            this.lon=position.coords.longitude;
            this.weatherAppService.display=true;
            let inputObj=new InputObj();
            inputObj.setInputObj("",this.lat,this.lon);
            this.weatherAppService.setCurrentWeather(inputObj);
            //Setting the current weather data
            setTimeout(()=>{this.currentWeather=this.weatherAppService.currentWeather;},500);
            //Setting forecast weather data
            setTimeout(()=>{this.forecasts=this.weatherAppService.temp;},1000);
            //Setting chart Data
            setTimeout(()=>
            {
              this.chartLabels=this.weatherAppService.chartDataTemp.timeStampdata;
              this.chartData[0].data=this.weatherAppService.chartDataTemp.temparatureData;
              this.chartData[1].data=this.weatherAppService.chartDataTemp.humidityData;
              this.chartData[2].data=this.weatherAppService.chartDataTemp.windSpeedData;
            },1000);

          }

        },(error) => console.log(error));

      }
      else
      {
        alert("Geolocation is not supported by this browser.");
      }
    }

    Search(cityName:any,lat:any,lon:any)
    {
      //Checking if there is empty input
      if((cityName=='') && (lat=='') && (lon==''))
      {
        this.dialog.open(PopupComponent, {data:{message:'Seach cannot be empty',id:1} } );
      }
      //If any of search or coordinates are filled then search will be exceuted
      else
      {
        this.weatherAppService.display=true;
        let inputObj=new InputObj();
        inputObj.setInputObj(cityName,lat,lon);
        //get the data of location
        this.weatherAppService.setCurrentWeather(inputObj);
        //Setting the data
        setTimeout(()=>{ this.currentWeather=this.weatherAppService.currentWeather;},2000);
        setTimeout(()=>{this.forecasts=this.weatherAppService.temp;},1000);
        setTimeout(()=>{
          this.chartLabels=this.weatherAppService.chartDataTemp.timeStampdata;
          this.chartData[0].data=this.weatherAppService.chartDataTemp.temparatureData;
          this.chartData[1].data=this.weatherAppService.chartDataTemp.humidityData;
          this.chartData[2].data=this.weatherAppService.chartDataTemp.windSpeedData;
                        },1000);

      }

    }

}