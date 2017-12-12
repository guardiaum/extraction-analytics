import numpy as np

# GEOGRAPHIC PROPERTIES CATEGORIZATION
latitudeProps = np.array(['latD', 'latM', 'latS', 'latNs', 'latitude', 'latDeg', 'latMin', 'latMax', 'lonDeg', 'latSec', 'latDir', 'latd', 'latm', 'lats', 'latns', 'lat',  'latDegrees', 'latMinutes', 'latSeconds', 'latDirection',])
longitudeProps = np.array(['longitude', 'longD', 'longM', 'longS', 'longEw', 'longd', 'longm', 'longs', 'longew', 'long', 'longDegrees', 'longMinutes', 'longSeconds', 'longDirection', 'lonDir', 'lonMin', 'lonSec'])
locationProps = np.array(['locationMap', 'locationMapSize', 'country', 'city', 'location', 'region', 'birthPlace', 'location_city', 'location_country', 'address', 'birthPlace', 'deathPlace'])
areaProps = np.array([ 'area', 'area_land_sq_mi', 'area_water_sq_mi', 'area_percentage', 'geo_cogenerationarea_total_sq_mi'])
coordinatesProps= np.array(['coordinatesType', 'coordinatesDisplay', 'coordinatesFormat', 'coordinatesRegion',  'coordinatesRef'     'coordDisplay', 'coordParameters'])
otherProps = np.array(['geo_type', 'geo_temp_requirement', 'geo_well_count', 'geo_well_depth', 'geo_water_output'])
altitudeProps = np.array(['altitude_m', 'altitude_ref'])
geoPropertiesNames = np.hstack([latitudeProps, longitudeProps, locationProps, areaProps, coordinatesProps, otherProps, altitudeProps])

# DATE AND TIME PROPERTIES CATEGORIZATION
year = np.array(['years', 'year', 'startyear', 'endyear', 'productionYearOil', 'peakYear', 'reargueyear', 'years_active', 'birthYear', 'deathYear', 'undraftedYear', 'draftYear', 'formationYear', 'extinctionYear', 'foundingYear'])
date = np.array(['date', 'birthDate', 'electionDate', 'opened_date', 'inauguration_date', 'election_date', 'birth_date', 'death_date', 'deathDate', 'electionDate', 'foundedDate',  'dateSigned', 'dateEffective', 'dateExpiration', 'rearguedate', 'signeddate', 'dateDrafted', 'discovery', 'peakofproduction',  'expectedabandonment', 'activeYearsStartDate', 'activeYearsEndDate', 'formationDate', 'foundingDate'])
period = np.array(['duration', 'start_date', 'stop_date', 'date_end', 'date_start', 'term_start', 'term_end', 'firstdate', 'finaldate', 'dateStart', 'dateEnd', 'startDate', 'stopDate', 'termStart', 'termEnd', 'governorStart', 'governorEnd', 'educationStart', 'educationEnd', 'publicServiceEnd', 'publicServiceStart', 'start', 'end', 'laborEnd', 'laborStart', 'startDevelopment', 'startofproduction', 'activeYearsStartYear', 'activeYearsEndYear', 'serviceStartYear', 'serviceEndYear'])
time = np.array(['timestamp', 'time', 'timezone'])
month = np.array(['month', 'months'])
other = np.array([])
dateTimePropertiesNames = np.hstack([year, date, period, time, month, other])
