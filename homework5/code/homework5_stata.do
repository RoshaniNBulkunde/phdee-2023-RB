/* ============================================================================ *
    Course Name    : ECON 7103- Environmental Economics 2
	Programmer     : Roshani Bulkunde
	Last Updated   : 2/5/2023
	Notes          : Homework 5
 ==============================================================================*/
 
 
clear all
capture log close
set more off

*-----Directory------*
global hw5dir "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework5"

*----- Export the data
import delimited "$hw5dir\instrumentalvehicles.csv"

*---- Change directory to output folder
cd "$hw5dir\output" // export all the output tables and figures 

*----Labeling variables
la var price "Price (USD)"
la var car "Car"
la var mpg "Fuel Efficiency (mpg)"
la var weight "Weight (Pounds)"
la var height "Height (Inches)"
la var length "Length (Inches)"

*=============== Question 1=========================*
/*1. Use the ivregress liml command to compute the limited information maximum likelihood estimate
using weight as the excluded instrument. Report your second-stage results in a nicely-formatted table
using outreg2. Use heteroskedasticity-robust standard errors. */



ivregress liml price car ( mpg= weight), vce(robust)
outreg2 using q1aIV_stata.tex, label tex(fragment) replace

*=============== Question 2=========================*
/*2. Use weakivtest to estimate the Montiel-Olea-Pflueger effective F-statistic. What is the 5% critical
value, the F-statistic, and conclusion? */