/* ============================================================================ *
    Course Name    : ECON 7103- Environmental Economics 2
	Programmer     : Roshani Bulkunde
	Last Updated   : 2/5/2023
	Notes          : Homework 4
 ==============================================================================*/
 
 
clear all
capture log close
set more off

*-----Directory------*
global hw4dir "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework4"

*----- Export the data
import delimited "$hw4dir\fishbycatch.csv"

*---- Change directory to output folder
cd "$hw4dir\output" // export all the output tables and figures 

*-------Reshape the data from wide to long
reshape long shrimp salmon bycatch, i(firm) j(month)



***********************************************
*        Question 1 a
***********************************************
*----Generate indicator variables for each firm.
gen post=(month>12) //post=1 if month>12 else zero
gen treatment=post*treated //The firmis treated if treated=1 and post=1

****Without Cluster Standard Errors
**Include these indicator variables in your OLS regression to control for fixed effects directly
regress bycatch firm month treatment firmsize shrimp salmon

*----- Labeling variables
la var firm "Firm ID"
la var month "Month"
la var treatment "Treatment"
la var firmsize "Firmsize"
la var shrimp "Shrimp (Pounds)"
la var salmon "Salmon (Pounds)"
la var bycatch "Bycatch"
** Output table
outreg2 using q1a_stata.tex, label tex(fragment) replace


*********** With Cluster Standard Errors***************
regress bycatch firm month treatment firmsize shrimp salmon, cluster(firm)

outreg2 using q1a_cluster_stata.tex, label tex(fragment) replace



/************************************************************************
*        Question 1 b
Perform the "within-transformation" on all of the dependent and independent variables by demeaning each variable
***************************************************************************/

** Demean bycatch
egen bycatch_mean = mean(bycatch), by(firm)
generate demeaned_bycatch = bycatch- bycatch_mean

** Demean treatment
egen treatment_mean = mean(treatment), by(firm)
generate demeaned_treatment = treatment- treatment_mean

** Demean firmsize
egen firmsize_mean = mean(firmsize), by(firm)
generate demeaned_firmsize = firmsize - firmsize_mean

** Demean shrimp
egen shrimp_mean = mean(shrimp), by(firm)
generate demeaned_shrimp = shrimp- shrimp_mean

** Demean salmon
egen salmon_mean = mean(salmon), by(firm)
generate demeaned_salmon = salmon- salmon_mean

***** Without Cluster Standard Errors
** Estimate the within-transformation
regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon

*----- Labeling variables
la var demeaned_treatment "Demeaned Treatment"
la var demeaned_firmsize "Demeaned Firmsize"
la var demeaned_shrimp "Demeaned Shrimp (Pounds)"
la var demeaned_salmon "Demeaned Salmon (Pounds)"
la var demeaned_bycatch "Demeaned Bycatch"

** Output table
outreg2 using q1b_stata.tex, label tex(fragment) replace

****** With Cluster standard Errors**************************

** Estimate the within-transformation
regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon, cluster(firm)
outreg2 using q1b_cluster_stata.tex, label tex(fragment) replace

/************************************************************************
*        Question 1 c
Display the results of your estimates from (a) and (b) in the same table, reporting the same clustered
standard errors or confidence intervals as previously
***************************************************************************/

eststo reg1:quietly regress bycatch firm month treatment firmsize shrimp salmon, cluster(firm)
eststo reg2: quietly regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon, cluster(firm)
	
esttab reg1 reg2 using DID_stata.tex, replace b(%3.2f) se(%3.2f) sfmt(%12.0fc) ///
fragment booktabs ///
drop(firm month) ///
mtitles(DID Within-Transformation) ///
varlabels(treatment "Treatment" firmsize "Firmsize" shrimp "Shrimp (Pounds)" salmon "Salmon (Pounds)" bycatch "Bycatch" ///
demeaned_treatment "Demeaned Treatment" demeaned_firmsize "Demeaned Firmsize" demeaned_shrimp "Demeaned Shrimp (Pounds)" demeaned_salmon "Demeaned Salmon (Pounds)")




