/*=========================================================================================
*******************************************************************************************
                        
Course name: Environmental Economics 2
	       
Programmer:  Roshani Bulkunde, Research Assistant, IIMA
							
Last updated:  1/22/2013
						 					
						                     	      
******************************************************************************************						 						 
=========================================================================================*/

*Clear Everything
clear all 
set more off // Prevents you from having to click more to see more output

*Set up your working directory
local direc = "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework2\output" 
	
cd "`direc'" //Change the directory

*Import the data
import delimited "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework2\kwh.csv", clear

/*Check for balance between the treatment and control groups using Stata. Create a table that displayseach variable's sample mean, sample standard deviation, 
and p-values for the two-way t-test between treatment and control group means. Your table should have four columns: one with variable names, one with sample mean 
and standard deviation for the control group, one with sample mean and standard deviation for the treatment group, and one with the p-value for the difference-inmeans
test. Hint: https://www.statalist.org/forums/forum/general-stata-discussion/general/1519721-summarized-statistics-table-with-t-test-for-difference-in-means contains useful code.*/

*------------Summary Statistics
eststo control: quietly estpost summarize electricity sqft temp if retrofit == 0
eststo treatment: quietly estpost summarize electricity sqft temp if retrofit == 1
eststo diff: quietly estpost ttest electricity sqft temp, by(retrofit) unequal
esttab control treatment diff using summarystats.tex , cells("mean(pattern(1 1 0) fmt(3)) sd(pattern(1 1 0)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") label