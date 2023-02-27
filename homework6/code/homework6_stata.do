/* ============================================================================ *
    Course Name    : ECON 7103- Environmental Economics 2
	Programmer     : Roshani Bulkunde
	Last Updated   : 2/18/2023
	Notes          : Homework 6
 ==============================================================================*/
 
 
clear all
capture log close
set more off

*-----Directory------*
global hw6dir "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework6"

*----- Export the data
import delimited "$hw6dir\instrumentalvehicles.csv"

*---- Change directory to output folder
cd "$hw6dir\output" // export all the output tables and figures 

*----Labeling variables
la var price "Price (USD)"
la var car "Car"
la var mpg "Fuel Efficiency (mpg)"
la var weight "Weight (Pounds)"
la var height "Height (Inches)"
la var length "Length (Inches)"

 scalar t4 = 225*225*225*225

gen length4= length* length* length* length


/*. Using the discontinuity as an instrument for miles per gallon, estimate the impact of mpg on the
vehicle's sale price. Use the rdrobust command in Stata. Use whatever degree polynomial you see
fit for the first stage. Use the CCT optimal bandwidth: bwselect(mserd). In the hedonic regression,
control for the class of the vehicle by including carv as in Homework 6. */

rdrobust mpg length, c(225) bwselect(mserd)

gen treatment = (length4>=t4)
*#
ivregress 2sls price car ( mpg= i.treatment), vce(robust)
outreg2 using Rd_2sls_stata.tex, label tex(fragment) replace

**Generate and report a plot of the results using rdplot.
**************************************************************************
rdplot mpg length, c(225) binselect(qspr) cov(car)
graph export rdplot_stata.pdf, replace
		