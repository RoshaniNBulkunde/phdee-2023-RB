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