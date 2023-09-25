=======
History
=======

0.1.0 (2022-03-08)
------------------

* First release on PyPI.

0.2.0 (2022-07-07)
------------------

* documentation on readthedocs
* tests
* new cli arguments added

0.2.1 (2022-07-12)
------------------

* install data and tables via pip

0.3.0 (2022-07-19)
------------------

* new indices implemented

  * CD: number of cold and dry days
  * CHDYYx: Maximum number of consecutive heat days
  * CSDI: Cold spell duration index
  * CW: Number of cold and wet days
  * DTR: Mean of daily temperature range
  * GD: Number of growing degree days
  * GDYYx: Number of consecutive growing degree days
  * HD17: Number of heating degree days
  * PRCPTOT: Total precipitation amount
  * RDYYp: Number of wet days with precip over percentile
  * RYYpTOT: Precipitation fraction with precip over percentile
  * TG10p: Fraction of days with mean temperature under 10th percentile
  * TG90p: Fraction of days with mean temperature under 90th percentile
  * TX10p: Fraction of days with maximum temperature under 10th percentile
  * TX90p: Fraction of days with maximum temperature under 90th percentile
  * TN10p: Fraction of days with minimum temperature under 10th percentile
  * TN90p: Fraction of days with minimum temperature under 90th percentile
  * WD: Number of warm and dry days
  * WSDI: Warm spell duration index
  * WW: Number of warm and wet days

0.3.1 (2022-07-20)
------------------

* adjustments fro automatically project-specific outfile name generation

0.3.2 (2022-07-21)
------------------

* project-specific directory structure for cordex, cmip5 and cmip6

0.3.3 (2022-08-10)
------------------

* more documentation
* properties to classes
* classes automatically call functions

0.4.0 (2022-11-25)
------------------

* split output files into several files
* restructuring time encoding
* properties removed

0.5.0 (2023-01-04)
------------------

* new indices:

  * CSf (Number of cold spells)
  * HSf (Number of hot spells)
  * HSx (Maximum length of hot spells)
  * SD (Number od snow days)
  * SCD (Snow cover duration)
  * Sint (Snowfall intensity)
  * Sfreq (Snowfall freqeuncy)
  * UTCI (Universal Thermal Climate Index)

* add time bounds
* index-calculator version in DRS

0.5.1 (2023-01-23)
-------------------

* add grid mapping if necessary

0.5.2 (2023-02-07)
------------------

* add input format and component information to index_calculation.pjson

0.5.3 (2023-02-13)
------------------

* new projects E-OBS and ERA5 included

0.5.4 (2023-02-15)
------------------

* new project HYRAS
* ignore time-dependent data variables other than input variable

0.5.5 (2023-02-16)
------------------

* new index (WI): number of winter days (tas<-10°C)
* use pyhomogenize>=0.2.9
* write time and time_bnds to float

0.5.6 (2023-02-22)
------------------

* time controlling to pyhomogenize

0.6.0 (2023-03-03)
------------------

* new indices:

  * HW: maximum length of heat waves
  * GSS: start of growing season
  * GSE: end of growing season
  * FFS: start of frost-free season
  * FFE: end of frost-free season
  * RRm: mean daily precipitation
  * RRYYp: precipitation percentile value

* rename RYYp to RYYpABS and RDYYP to RYYp according to ICCLIM
* optional argument perc woth percentile indicators

0.6.1 (2023-03-09)
------------------

* some metadata corrections

0.6.2 (2023-03-10)
------------------

* component name adjusments with HYRAS

0.6.3 (2023-03-13)
------------------

* take coordinate attributes from input dataset

0.6.4 (2023-03-13)
------------------

* HYRAS file naming convention
* convert precip units from mm to mm day-1


0.6.5 (2023-03-16)
------------------

* rename variavle names to CF variable names
* metadata with SQI, CHDYY and CHDYYx

0.6.6 (2023-03-21)
------------------

* filter out small values before calculating precipitation percentiles
* raw percentile indicators (`RR95p`) has to time axis but a dayofyear axis

0.6.7 (2023-03-22)
------------------

* HYRAS file naming convention
* delete blanks from output file name
* calcualte indicators woth length of time axis is 1

0.7.0 (2023-03-22)
------------------

* published in zenodo

0.7.1 (2023-03-29)
------------------

* calculating percentile indices with non-standard calendar

0.7.2 (2023-05-10)
------------------

* new indicators implemented:

  * FG (mean daily wind speed)
  * FGn (minimum od mean daily wind speed)
  * FGx (maximum of mean daily wind speed)
  * FX (mean of maximum daily wind speed)
  * FXn (minimum of daily maximum wind speed)
  * FXx (maximum of daily maximum wind speed)

0.7.3 (2023-06-06)
------------------

* rework metadata and make it more flexible regarding threshold values
* more parameter information in cliamte indices docstrings
* adjust parameter names to xclim
* set threshold for dry day incides from 0.1 mm/day to 1 mm/day
* set threshold from snowfall rate to liquid water equivalent snowfall rate with SD, Sint and Sfreq -> those changes are not implemented in xclim yet, PR will be accepted with xclim>=0.45

0.7.4 (2023-06-08)
------------------

* rename DSP to DSf according to other spell indicators
* rename HW to HWx according to other spell indicators
* new indicator: DSx, HWf
* rename tables/indices.json to tables/metadata.json
* expand some docstrings and rework metadata
* those changes are not implemented in xclim yet
* as soon as this is done index_calculator goes v0.8.0

0.7.5 (2023-06-19)
------------------

* if dataset frequency is not equal input frequency, convert it
* adding hourly test data
* calcualte climate indicators for ERA5 data
* input variable for WI is tasmin not tas

0.7.6 (2023-06-20)
------------------

* outsourcing test data to github repository https://github.com/ludwiglierhammer/test_data

0.8.0 (2023-07-13)
------------------
* optionally: calculate SCD with water equivalent input
* replace '.' with '-' in directory structure and output file names
* new climate indicators:

  * DSn: total number of days in dry spells
  * WSn: total number of days in wet spells
  * CSx: maximum length of cold spell
  * CSn: total number of days in cold spells
  * HSn: total number of days in hot spells
  * HWn: total number of days in heat waves
  * LFD: number of late frost days

* metadata: set mm/day to mm
* fixing v0.7.3 and v0.7.4 with xclim>=0.44
* redo v0.7.5 (if dataset frequency is not equal input frequency, convert it; adding hourly test data)

0.8.1 (2023-08-18)
------------------

* new drs format and file naming convention for project E-OBS

0.8.2 (2023-08-31)
------------------

* calculate indices with neagtive thresholds

0.9.0 (2023-09-25)
------------------

* convert time frequencies to requested time frequency
* rename variable name(s) to requested variable name(s)
* convert input variable(s) to requested input variable(s): sfcWind, snd
* SCD: set default threshold to `3mm day-1`
* set left and right bounds for `yearAC` (yyyy1-07-01 to yyyy2-06-30) and for `yearHydro` (yyyy1-09-01 to yyyy2-08-31)
* new ERA5 DRS structure and file naming convention
* type of components in `pjson` from `str` to `list`
