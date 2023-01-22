/*=========================================================================================
*******************************************************************************************
                        
Course name: Environmental Economics 2
	       
Programmer:  Roshani Bulkunde, Georgia Institute of Technology
							
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


** Question 1
/*Check for balance between the treatment and control groups using Stata. Create a table that displayseach variable's sample mean, sample standard deviation, 
and p-values for the two-way t-test between treatment and control group means. Your table should have four columns: one with variable names, one with sample mean 
and standard deviation for the control group, one with sample mean and standard deviation for the treatment group, and one with the p-value for the difference-inmeans
test. Hint: https://www.statalist.org/forums/forum/general-stata-discussion/general/1519721-summarized-statistics-table-with-t-test-for-difference-in-means contains useful code.*/

*------------Summary Statistics
eststo control: quietly estpost summarize electricity sqft temp if retrofit == 0
eststo treatment: quietly estpost summarize electricity sqft temp if retrofit == 1
eststo diff: quietly estpost ttest electricity sqft temp, by(retrofit) unequal
esttab control treatment diff using summaryStata.tex , replace cells("mean(pattern(1 1 0) fmt(3)) sd(pattern(1 1 0)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") label

** Question 2
/*2. Create a two-way scatterplot with electricity consumption on the y-axis and square feet on the x-axis
using Stata's twoway command. Make sure to label the axes. */
twoway (scatter electricity sqft), ytitle(Electricity Consumption (kWh)) xtitle(Home (sqft))
graph export Stata_twowayscatter.pdf, replace

**Question 3
/*Estimate the same regression as in #3 above using Stata's regress command, estimating heteroskedasticityrobust
standard errors. Report the results in a new LaTeX table (including standard errors) using
Stata's outreg2 command. */
reg electricity retrofit sqft temp, vce(robust)
outreg2 using stata_regress.tex, label 2aster tex(frag) dec(2) replace ctitle("Ordinary least squares")





