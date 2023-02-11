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

 forvalues i = 1/50 {
             generate firm`i' = (firm==`i')
                     }

*----- Generate Interaction term
gen post=(month>12) //post=1 if month>12 else zero
gen treatment=post*treated //The firmis treated if treated=1 and post=1

*----- Labeling variables
la var firm "Firm"
la var month "Month"
la var treatment "post*treated"
la var firmsize "Firmsize"
la var shrimp "Shrimp (Pounds)"
la var salmon "Salmon (Pounds)"
la var bycatch "Bycatch"


/*
# 
regress bycatch firm1 firm2 firm3 firm4 firm5 firm6 firm7 firm8 firm9 firm10 firm11 firm12 firm13 firm14 ///
firm15 firm16 firm17 firm18 firm19 firm20 firm21 firm22 firm23 firm24 firm25 firm26 firm27 firm28 firm29 firm30 ///
firm31 firm32 firm33 firm34 firm35 firm36 firm37 firm38 firm39 firm40 firm41 firm42 firm43 firm44 firm45 ///
firm47 firm48 firm49 firm50 month treatment firmsize shrimp salmon, vce(cluster firm) */

*********** With Cluster Standard Errors***************

* Method 2
regress bycatch i.firm month treatment firmsize shrimp salmon, vce(cluster firm)
*outreg2 using q1a_cluster_stata.tex, label tex(fragment) keep(treatment firmsize shrimp salmon) replace
	
outreg2 using q1a_cluster_stata.tex, label tex(fragment) drop(i.firm month) replace

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
la var demeaned_treatment "Demeaned post*treated"
la var demeaned_firmsize "Demeaned Firmsize"
la var demeaned_shrimp "Demeaned Shrimp (Pounds)"
la var demeaned_salmon "Demeaned Salmon (Pounds)"
la var demeaned_bycatch "Demeaned Bycatch"

** Output table
outreg2 using q1b_stata.tex, label tex(fragment) replace

****** With Cluster standard Errors**************************

** Estimate the within-transformation
regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon, vce(cluster firm)
outreg2 using q1b_cluster_stata.tex, label tex(fragment) replace

/************************************************************************
*        Question 1 c
Display the results of your estimates from (a) and (b) in the same table, reporting the same clustered
standard errors or confidence intervals as previously
***************************************************************************/

regress bycatch i.firm month treatment firmsize shrimp salmon, vce(cluster firm)	
outreg2 using q1c_stata.tex, label tex(fragment) drop(i.firm month) replace

regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon, vce(cluster firm)
outreg2 using q1c_stata.tex, label tex(fragment) append


/*
eststo reg1:quietly regress bycatch i.firm month treatment firmsize shrimp salmon, vce(cluster firm)
eststo reg2: quietly regress demeaned_bycatch demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon, vce(cluster firm)


esttab reg1 reg2 using DID_stata.tex, replace b(%3.2f) se(%3.2f) sfmt(%12.0fc) ///
fragment booktabs nostar unstack ///
keep(treatment firmsize shrimp salmon demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon) ///
varlabels(treatment "Treatment" firmsize "Firmsize" shrimp "Shrimp (Pounds)" salmon "Salmon (Pounds)" bycatch "Bycatch" ///
demeaned_treatment "Demeaned Treatment" demeaned_firmsize "Demeaned Firmsize" demeaned_shrimp "Demeaned Shrimp (Pounds)" demeaned_salmon "Demeaned Salmon (Pounds)") 


esttab reg1 reg2 using DID_stata.tex, replace ///
cells( "b(star pattern(1 1) fmt(%9.2fc) label(coef.))" "se(pattern(1 1) par label(SD))") stats(N obs, fmt(%9.0fc) labels("Observations")) starlevels(* 0.05 ** 0.01) ///
mtitles(Treated Controls  ) label replace prehead({\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{3}{cc}} \hline) ///
prefoot( & & \\) postfoot(\hline \multicolumn{4}{c}{ ** p$<$0.01, * p$<$0.05} \\ \end{tabular} }) ///
fragment booktabs nostar unstack ///
keep(treatment firmsize shrimp salmon demeaned_treatment demeaned_firmsize demeaned_shrimp demeaned_salmon) ///
varlabels(treatment "Treatment" firmsize "Firmsize" shrimp "Shrimp (Pounds)" salmon "Salmon (Pounds)" bycatch "Bycatch" ///
demeaned_treatment "Demeaned Treatment" demeaned_firmsize "Demeaned Firmsize" demeaned_shrimp "Demeaned Shrimp (Pounds)" demeaned_salmon "Demeaned Salmon (Pounds)")
*/
