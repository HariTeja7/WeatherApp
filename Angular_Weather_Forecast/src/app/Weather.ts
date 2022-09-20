
export class CurrentWeather{
    constructor(){
        
    }
    cityName:String="";
    timezone:String="";
    lat:number=0;
    lon:number=0;
    day: String="";
    date: String="";
    maxTemp:String="";
    minTemp: String="";
    pressure: String="";
    humidity:String="";
    windSpeed:String="";
    description:String="";
    icon:String="";
    iconUrl:String="";
    country:String="";
    cod:String="";
    message="";
    setCurrentWeather(data:any)
    {
        this.cityName=data.cityName;
        this.country=data.country;
        this.timezone=data.timezone;
        this.lat=data.lat;
        this.lon=data.lon;
        this.date=data.date;
        this.day=data.day;
        this.maxTemp=data.maxTemp;
        this.minTemp=data.minTemp;
        this.pressure=data.pressure;
        this.humidity=data.humidity;
        this.windSpeed=data.windSpeed;
        this.description=data.description;
        this.icon=data.icon;
        this.iconUrl="http://openweathermap.org/img/wn/"+this.icon+"@4x.png";
        this.cod=data.cod;
        this.message=data.message;
    }
}

export class CurrentWeatherChart{
    constructor(){}
    timeStampdata=[];
    temparatureData=[];
    windSpeedData=[];
    humidityData=[];
    date:String='';
    setCurrentWeatherChart(data:any){
        this.date=data.date;
        this.timeStampdata=data.timeStampdata;
        this.temparatureData=data.temparatureData;
        this.humidityData=data.humidityData;
        this.windSpeedData=data.windSpeedData;
    }
}

export class EachDay{
    date!:String;
    day!: String;
    temp!:String;
    pressure!:String;
    humidity!: String;
    windSpeed!: String;
    icon:String="";
    iconUrl:String="";
    setEachDay(data:any){
        this.date=data.date;
        this.day=data.day;
        this.temp=data.temp;
        this.pressure=data.pressure;
        this.humidity=data.humidity;
        this.windSpeed=data.windSpeed;
        this.icon=data.icon;
        this.iconUrl="http://openweathermap.org/img/wn/"+this.icon+"@4x.png";
    }
}
export class InputObj{
    lat:number=0;
    lon:number=0;
    cityName:String="";
    setInputObj(cityName:String,lat:number,lon:number){
        this.lat=lat;
        this.lon=lon;
        this.cityName=cityName;
    }
}