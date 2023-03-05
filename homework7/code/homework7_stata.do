/* ============================================================================ *
    Course Name    : ECON 7103- Environmental Economics 2
	Programmer     : Roshani Bulkunde
	Last Updated   : 3/1/2023
	Notes          : Homework 7
 ==============================================================================*/
 
 
clear all
capture log close
set more off

set maxvar 32767

*-----Directory------*
global hw7dir "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework7"

*----- Export the data
use "$hw7dir\electric_matching.dta", clear

*---- Change directory to output folder
cd "$hw7dir\output" // export all the output tables and figures 

/*================================================================================
                          Question 1
==================================================================================*/

**Generate a log electricity consumption variable
gen lnmw = log(mw)

**binary treatment variable that is equal to one for all time eriods March 1, 2020 and after
gen treatment = 0
replace treatment = 1  if (month>=3 & day>=1 & year>=2020 )

** Encode zone to convert it into interger value
encode zone, gen(zone1)

*------------- Question 1 (a)
** Estimate the equation
reg lnmw i.zone1 i.month i.dow i.hour treatment temp pcp, vce(robust)
outreg2 using output1a_stata.tex, label keep(treatment temp pcp) tex(fragment) replace


*------------- Question 1 (b)

** Generate hour of the day variable
g hod = hh(time)

**drop months 1 and 2 to get overlap for the matching estimate
drop if month==1 | month==2

** Estimate the equation
teffects nnmatch (lnmw temp pcp) (treatment), ematch(zone1 month dow hod) vce(robust) osample(overlap1)
outreg2 using output1b_stata.tex, label tex(fragment) replace
/*================================================================================
                          Question 2
==================================================================================*/
*----- Export the data
use "$hw7dir\electric_matching.dta", clear

**Generate a log electricity consumption variable
gen lnmw = log(mw)

** Encode zone to convert it into interger value
encode zone, gen(zone1)

** Generate hour of the day variable
g hod = hh(time)

**binary treatment variable that is equal to one for all time eriods March 1, 2020 and after
gen treatment = 0
replace treatment = 1  if (month>=3 & day>=1 & year>=2020 )

** Estimate the equation
reg lnmw i.zone1 i.month i.dow i.hod i.year treatment temp pcp, vce(robust)

/*================================================================================
                          Question 3
==================================================================================*/
*------------- Question 3 (a)
** Generate binary variable year2020 equal to one during all of 2020.
gen y2020 = (year==2020)

keep if year==2020 | year==2019

** Estimate the equation
teffects nnmatch (lnmw temp pcp) (y2020), ematch(zone1 dow hod month) vce(robust) osample(overlap2) gen(logmw_hat) //logmw_hat equal to the matched electricity consumption
outreg2 using output3a_stata.tex, label tex(fragment) replace

keep if year==2020
**generate a variable for difference between log electricity consumption and matched log electricity consumption
gen diff_lgmw = lnmw - logmw_hat1

reg diff_lgmw treatment, vce(robust)
outreg2 using output3a2_stata.tex, label tex(fragment) replace









