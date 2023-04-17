/* ============================================================================ *
    Course Name    : ECON 7103- Environmental Economics 2
	Programmer     : Roshani Bulkunde
	Last Updated   : 4/12/2023
	Notes          : Homework 8
 ==============================================================================*/
 
 
clear all
capture log close
set more off

set maxvar 32767

*-----Directory------*
global hw8dir "C:\Users\rosha\Dropbox (GaTech)\PhD-2023-Env2\phdee-2023-RB\homework8"

*----- Export the data
use "$hw8dir\recycling_hw.dta", clear

*---- Change directory to output folder
cd "$hw8dir\output" // export all the output tables and figures 

/*---------------------      Question 1. -------------------------------*
Produce a yearly plot of the recycling rate for NYC and the controls to examine the effect of the recycling pause and the possibility of parallel trends.*/
bys year: egen mean_recyclingrate_nyc=mean(recyclingrate) if nyc == 1
bys year: egen mean_recyclingrate_control=mean(recyclingrate) if nyc == 0

twoway connected mean_recyclingrate_nyc mean_recyclingrate_control year, legend(label (1 "New York City") label (2 "Controls")) ytitle(Fraction of waste recycled) xline(2001.5 2004.5) xlabel(1995(1)2010, labsize(vsmall)) ylabel(0(0.05).4, labsize(vsmall)) 

graph export "hw8_q1parallel.pdf", replace

**********************************************************************************************************************************



/*---------------------      Question 2. -------------------------------
 Estimate the effect of the pause on the recycling rate in NYC using a TWFE regression and the data from 1997-2004. Cluster your standard errors at the region level. Report the average treatment effect estimate and the standard error. */
xtset id year
xtreg recyclingrate nyc i.year, fe vce(cluster region)

**********************************************************************************************************************************



/*---------------------      Question 3. -------------------------------
 Use the command sdid to estimate the synthetic DID version of the TWFE regression in equation 2. */

/*sdid Y S T D [if] [in], vce(method) seed(#) reps(#) covariates(varlist [, method]) method(methodtype)
                        unstandardized graph_export([stub] , type) mattitles
                        graph g1on g1_opt(string) g2_opt(string) msize() */

sdid recyclingrate region year nyc, vce(placebo) reps(100) seed(123) covariates(incomepercapita collegedegree2000 democratvoteshare2000 democratvoteshare2004 nonwhite) graph g1_opt(xtitle("") ylabel(0(0.05).4) xlabel(1995(1)2010, labsize(small)) scheme(plotplainblind)) g2_opt(xlabel(1995(1)2010, labsize(small)) ytitle("Packs per capita") xtitle("") graph_export([sdid_, .png] , type))

**********************************************************************************************************************************


/*---------------------      Question 4. -------------------------------*/





**********************************************************************************************************************************




/*---------------------      Question 5. -------------------------------
 Use the commands synth and synth_runner to generate synthetic control estimates of the dynamic treatment effects. Generate the synthetic control estimates using whichever matching variables you see as most appropriate. Use placebo inference. Report: */
 
 
*----------(a) The plot of raw outcomes for treated and control groups over time.
*----------(b) The plot of raw outcomes for treated group and synthetic control group over time.
*----------(c) The plot of estimated synthetic control effects and placebo effects over time.
*----------(d) The plot of final synthetic control estimates over time.


*----------(e) Hints: Note that all of these plots can be generated using postestimation commands that come with synth_runner. You will need to collapse all of New York City to one treated unit to usethe canned commands. Finally, remember that these estimates