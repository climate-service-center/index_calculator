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
