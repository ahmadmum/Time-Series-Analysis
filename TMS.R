
install.packages("openair v2.7-4")

install.packages("tidyverse")


install.packages("check_gaps")

install.packages("lubridate")

install.packages("zoo")
install.packages("gridExtra")
library(writexl)
library(openair)

library(ggplot2)
library(dplyr)
#########################################Step-1

setwd("C:/Users/mumta/Desktop/Time Series Analysis/Assignment 1/Time series analysis R/DWDFile_Assignment1")

#reading files

airtemp <-read.csv("weste_product_2010_air_temperature.csv",header = T, sep = ";", quote = "", dec = ",")

precipitation <-read.csv("weste_product_2010_precipitation.csv",header = T, sep = ";", quote = "", dec = ",")

soiltemp <-read.csv2("weste_product_2010_soil_temperature.csv",header = T, sep = ";", quote = "", dec = ",")

head(airtemp)
head(precipitation)
head(soiltemp)

#extracting column

newairtemp <- airtemp [,c("Datum","Wert")]
newprecipitation <- precipitation  [,c("Datum","Wert")]
newsoiltemp <- soiltemp  [,c("Datum","Wert")]

head(newairtemp)
head(newprecipitation)
head(newsoiltemp)


#converting time series string



newairtemp[,1]  <- as.POSIXct(newairtemp[,1],tz="UTC")
newprecipitation [,1] <- as.POSIXct(newprecipitation[,1],tz="UTC")
newsoiltemp [,1]    <- as.POSIXct(newsoiltemp [,1],tz="UTC")

print(newairtemp)


#####################################################step2

#identity gaps




check_gaps(newairtemp,1)
check_gaps(newsoiltemp,1)

# puttinng missing vlaue in excell


##EXporting Dataframe into excell

library(writexl)
write_xlsx(newairtemp, 'Air temp dataframe.xlsx')
write_xlsx(newprecipitation, 'Soil temp dataframe.xlsx')


## Importing filled missing values csv file into R

fullairtemp <-read.csv("fullairtemp.csv",header = T,  dec = ".",fileEncoding="UTF-8-BOM")
fullsoiltemp <-read.csv("fullsoiltemp.csv",header = T, quote = "", dec = ".", fileEncoding="UTF-8-BOM") 
fullprecipitation <- newprecipitation



fullairtemp[,1]  <- as.POSIXct(fullairtemp[,1],tz="UTC", )
fullprecipitation[,1]  <- as.POSIXct(fullprecipitation[,1],tz="UTC")
fullsoiltemp [,1]    <- as.POSIXct(fullsoiltemp [,1],tz="UTC")


head(fullairtemp)

#mean, min, max for newairtemp

mean(fullairtemp[,2])
min(fullairtemp[,2])
max(fullairtemp[,2])


#mean, min, max for newprecipitation

mean(fullprecipitation[,2])
min(fullprecipitation[,2])
max(fullprecipitation[,2])

#mean, min, max for newsoiltemp

mean(fullsoiltemp[,2])
min(fullsoiltemp[,2])
max(fullsoiltemp[,2])


##extract monthly sub time series


#Air temp mean, min, max 
library(zoo)
library(dplyr)  ## for %>%


fullairtemp$Datum <- as.yearmon(fullairtemp$Datum)

airt_monthly_mean<- fullairtemp %>%
  group_by(Datum) %>%
  summarise_all(mean)
print(airt_monthly_mean)


airt_monthly_min<- fullairtemp %>%
  group_by(Datum) %>%
  summarise_all(min)
print(airt_monthly_min)

airt_monthly_max<- fullairtemp %>%
  group_by(Datum) %>%
  summarise_all(max)
print(airt_monthly_max)

#Precipitation mean, min, max  and Sum

fullprecipitation$Datum <- as.yearmon(fullprecipitation$Datum)

precip_monthly_mean<- fullprecipitation %>%
  group_by(Datum) %>%
  summarise_all(mean)
print(precip_monthly_mean)

precip_monthly_min<- fullprecipitation %>%
  group_by(Datum) %>%
  summarise_all(min)
print(precip_monthly_min)

precip_monthly_max<- fullprecipitation %>%
  group_by(Datum) %>%
  summarise_all(max)
print(precip_monthly_max)

precip_monthly_sum<- fullprecipitation %>%
  group_by(Datum) %>%
  summarise(Wert = sum(Wert))
print(precip_monthly_sum)

### yearly sum of precipitation

precipi_sum_year <- sum(fullprecipitation$Wert, na.rm = FALSE)
print(precipi_sum_year) 


#Soil temp mean, min, max


fullsoiltemp$Datum <- as.yearmon(fullsoiltemp$Datum)

soilt_monthly_mean<- fullsoiltemp %>%
  group_by(Datum) %>%
  summarise_all(mean)
print(soilt_monthly_mean)

soilt_monthly_min<- fullsoiltemp %>%
  group_by(Datum) %>%
  summarise_all(min)
print(soilt_monthly_min)

soilt_monthly_max<- fullsoiltemp %>%
  group_by(Datum) %>%
  summarise_all(max)
print(soilt_monthly_max)

##scaling to daily and weekly values

library(xts)

## daily , weekly values of air temp

airt_xts<- xts(fullairtemp$Wert, order.by = fullairtemp$Datum ,dimnames(Datum))

airt_daily <-apply.daily(airt_xts, FUN=mean)
names(airt_daily)[1]<-"Wert"

airt_weekly<- apply.weekly(airt_xts, FUN=mean)
names(airt_weekly)[1]<-"Wert"

####2nd method for air temp

at_daily = scaleTimeSeries(fullairtemp,24,mean=TRUE)
at_weekly = scaleTimeSeries(fullairtemp,24*7,mean=TRUE)

## daily , weekly values of precipi

precipi_xts<- xts(fullprecipitation$Wert, order.by = fullprecipitation$Datum)

precipi_daily <-apply.daily(precipi_xts, FUN=sum)
names(precipi_daily)[1]<-"Wert"


precipi_weekly<- apply.weekly(precipi_xts, FUN=sum)
names(precipi_weekly)[1]<-"Wert"



## daily , weekly values of precipi


soilt_xts<- xts(fullsoiltemp$Wert, order.by = fullsoiltemp$Datum)

soilt_daily <-apply.daily(soilt_xts, FUN=mean)
names(soilt_daily)[1]<-"Wert"


soilt_weekly<- apply.weekly(soilt_xts, FUN=mean)
names(soilt_weekly)[1]<-"Wert"


#####################################################step3

  


##### three plots of the full three time series yearly

library(ggplot2)

fullairtemp %>%
  ggplot(aes(x = Datum, y = Wert)) +
  geom_line(color = "darkorchid4") +
  labs(title ="                                      Air temp yearly",
       subtitle = "The data frame is sent to the plot using pipes",
       y = "Air temp (Celsius)",
       x = "Date") + theme_bw(base_size = 15)

fullsoiltemp %>%
  ggplot(aes(x = Datum, y = Wert)) +
  geom_line(color = "blue") +
  labs(title = "                                    Soil temp yearly",
       subtitle = "The data frame is sent to the plot using pipes",
       y = "Soil temp (Celsius)",
       x = "Date") + theme_bw(base_size = 15)

fullprecipitation %>%
  ggplot(aes(x = Datum, y = Wert)) +
  geom_line(color = "brown") +
  labs(title = "                                             Precipitation yearly",
       subtitle = "The data frame is sent to the plot using pipes",
       y = "Precipi (mm)",
       x = "Date") + theme_bw(base_size = 15)





##one plot with the air and the soil temperature in June 2010 (two lines)



plot_month(fullairtemp,6,"Ts")
plot_line_month(fullsoiltemp,6)
legend("topleft", legend=c("Air temp", "Soil temp"),
       col=c("lightgreen","Red", "green"), lty=1:2, cex=1)



#####one plot with the hourly, daily and weekly time step for air temperature (three lines)



plot(fullairtemp,type="l",col="lightgreen" )
lines(at_daily,type="l",col="red")
lines(at_weekly,type="l",col="black")
title("Hourly, Daily and Weekly Air Temp")
legend("topleft", legend=c("Hourly", "Daily","Weekly"),
       col=c("lightgreen","red", "black"), lty=1:2, cex=1)



