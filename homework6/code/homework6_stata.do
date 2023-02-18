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