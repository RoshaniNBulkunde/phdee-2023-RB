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

*--------------
bys year: egen mean_recyclingrate_nj=mean(recyclingrate) if nj == 1
bys year: egen mean_recyclingrate_ma=mean(recyclingrate) if ma == 1

twoway connected mean_recyclingrate_nyc mean_recyclingrate_nj  mean_recyclingrate_ma year, legend(label (1 "New York City") label (2 "New Jersey") label (3 "Massachusetts")) ytitle(Fraction of waste recycled) xline(2001.5 2004.5) xlabel(1995(1)2010, labsize(vsmall)) ylabel(0(0.05).4, labsize(vsmall)) 

graph export "hw8_q1parallel_2.pdf", replace

**********************************************************************************************************************************



/*---------------------      Question 2. -------------------------------
Estimate the effect of the pause on the recycling rate in NYC using a TWFE regression and the data from 1997-2004. Cluster your standard errors at the region level. Report the average treatment effect estimate and the standard error. */

*-------Data only for 1997 to2004
preserve

	drop if year> 2004

	*--- Create region id variable
	encode region, generate(regionid) label(region)

	*----Set panel setting for dataset
	xtset regionid year

	*---Twoway fixed effect
	gen treat = 0
	replace treat = 1 if year>=2002
	lab var treat "Treated"

	xtreg recyclingrate nyc##treat i.year,fe vce(cluster regionid)

**********************************************************************************************************************************


/*---------------------      Question 3. -------------------------------
 Use the command sdid to estimate the synthetic DID version of the TWFE regression in equation 2. */

/*sdid Y S T D [if] [in], vce(method) seed(#) reps(#) covariates(varlist [, method]) method(methodtype) unstandardized graph_export([stub] , type) mattitles
                        graph g1on g1_opt(string) g2_opt(string) msize() */
    gen interaction = nyc*treat
	sdid recyclingrate regionid year interaction, vce(bootstrap) seed(1000) graph graph_export(sdid_graph, .pdf)
	*graph export "sdid_graph.pdf", replace
	
	**Import the table
	eststo sdid: sdid recyclingrate regionid year interaction, vce(bootstrap) seed(100)

	*create a table
	esttab sdid using "q3_sdid.tex", replace starlevel ("*" 0.10 "**" 0.05 "***" 0.01) b(%-9.3f) se(%-9.3f) 
	
restore
**********************************************************************************************************************************


/*---------------------      Question 4. -------------------------------*/

** Year 2001 are not included in the analysis
gen l = year
replace l = . if year == 2001


gen treated = 0
replace treated = 1 if l>=2002 & nyc==1
lab var treated "Treated"

encode region, generate(regionid) label(region)

xtset regionid year

*---Regression
reg recyclingrate treated incomepercapita nonwhite i.regionid i.year, vce(cluster regionid)
estimates store q4reg
*coefplot, vertical keep (recyclingrate treated incomepercapita nonwhite)

*---DID
reghdfe recyclingrate treated incomepercapita nonwhite, absorb(regionid year) vce(cluster regionid)
estimates store q4reghdfe

*----Set panel setting for dataset

xtreg recyclingrate treated i.year incomepercapita nonwhite,fe vce(cluster regionid)
estimates store q4xtreg

***Coefficient plots
coefplot (q4reg \ q4reghdfe \ q4xtreg), vertical keep (recyclingrate treated incomepercapita nonwhite) aseq swapnames ///
    coeflabels(q4reg = "reg" q4reghdfe = "reghdfe" q4xtreg = "xtreg") ytitle(Coefficient) title(Estimates)

graph export "hw8_q4_coefplot.pdf", replace
	
**********************************************************************************************************************************


/*---------------------      Question 5. -------------------------------
Use the commands synth and synth_runner to generate synthetic control estimates of the dynamic treatment effects. Generate the synthetic control estimates using whichever matching variables you see as most appropriate. Use placebo inference. Report: */

/*                 Note: to install synth packages
ssc install synth, all
cap ado uninstall synth_runner //in-case already installed
net install synth_runner, from(https://raw.github.com/bquistorff/synth_runner/master/) replace */
 
use "$hw8dir\recycling_hw.dta", clear

*----------(a) The plot of raw outcomes for treated and control groups over time.
encode region, gen(regionid)
tsset regionid year

replace regionid =  0 if nyc == 1 // Set NewYork regionid = 0

collapse nyc nj ma recyclingrate id fips collegedegree2000 incomepercapita munipop2000 democratvoteshare2000 democratvoteshare2004 nonwhite, by(year regionid)

**Synth
synth recyclingrate nonwhite incomepercapita munipop2000, trunit(0) trperiod(2002) figure keep(SynthData.dta) replace //trunit=0 (treatment unit)
graph export "hw8_q5a_synth.pdf", replace

**Synth_runner
synth_runner recyclingrate nonwhite incomepercapita munipop2000, trunit(0) trperiod(2002) gen_vars
save "SynthRunnerData.dta", replace


*----------(b) The plot of raw outcomes for treated group and synthetic control group over time.
effect_graphs, treated_name("NYC") tc_options(title("Synthetic Control and Treatment Group") xsc(r(1997,2008)) xlabel(1997(1)2008) ysc(r(0.05,0.4)) ylabel(0.05(0.05)0.4) xtitle("Year") ytitle("Recycling Rate")) effect_options(title("Synthetic Control Estimates") xsc(r(1997,2008)) xlabel(1997(1)2008) ysc(r(-0.23,-0.13)) ylabel(-0.23(0.01)-0.13) xtitle("Year") ytitle("Change in Recycling Rate")) 

graph export "Q5b_synth.pdf", replace

graph export "Q5d_synth.pdf", as(pdf) name("effect") replace

*-----------------------------------
single_treatment_graphs, do_color(green) treated_name("NYC") donors_name("All Other Regions") raw_options(title("Raw Outcomes") xsc(r(1997,2008)) xlabel(1997(1)2008) ysc(r(0.05,0.85)) ylabel(0.05(0.05)0.85) xtitle("Year") ytitle("Recycling Rate")) effects_options(title("Raw Effects") xsc(r(1997,2008)) xlabel(1997(1)2008) ysc(r(-0.35,0.45)) ylabel(-0.35(0.05)0.45) xtitle("Year") ytitle("Change in Recycling Rate"))

graph export "Q5a_synth.pdf", as(pdf) name("raw") replace


*-----------
pval_graphs, pvals_options(title("Placebo Effects") xsc(r(0,7)) xlabel(0(1)7) ysc(r(0,0.3)) ylabel(0(0.05)0.3))

graph export "Q5c_synth.pdf", as(pdf) name("pvals") replace

*----------(c) The plot of estimated synthetic control effects and placebo effects over time.




*----------(d) The plot of final synthetic control estimates over time.



/*
cd "$hw8dir\output\synth"

encode region, gen(regionid)
tsset regionid year

replace regionid =  0 if nyc == 1

collapse nyc nj ma recyclingrate id fips collegedegree2000 incomepercapita munipop2000 democratvoteshare2000 democratvoteshare2004 nonwhite, by(year regionid)

tempname resmat
        forvalues i = 0/26 {
        quietly synth recyclingrate nonwhite incomepercapita munipop2000, trunit(`i') trperiod(2002) keep(synth_`i', replace)
        matrix `resmat' = nullmat(`resmat') \ e(RMSPE)
        local names `"`names' `"`i'"'"'
		}
        mat colnames `resmat' = "RMSPE"
        mat rownames `resmat' = `names'
        matlist `resmat' , row("Treated Unit")
		
forval i=0/26 {

	use synth_`i', clear
	rename _time years
	gen tr_effect_`i' = _Y_treated - _Y_synthetic
	keep years tr_effect_`i'
	drop if missing(years)
	save synth_`i', replace
}

use synth_0, clear

forval i=1/26 {
	qui merge 1:1 years using synth_`i', nogenerate
}

save synth_0.dta, replace

*--------
use "$hw8dir\recycling_hw.dta", clear

encode region, gen(regionid)
tsset regionid year

replace regionid =  0 if nyc == 1

collapse nyc nj ma recyclingrate id fips collegedegree2000 incomepercapita munipop2000 democratvoteshare2000 democratvoteshare2004 nonwhite, by(year regionid)

tempname resmat
        forvalues i = 29/124 {
        quietly synth recyclingrate nonwhite incomepercapita munipop2000, trunit(`i') trperiod(2002) keep(synth_`i', replace)
        matrix `resmat' = nullmat(`resmat') \ e(RMSPE)
        local names `"`names' `"`i'"'"'
		
        }
        mat colnames `resmat' = "RMSPE"
        mat rownames `resmat' = `names'
        matlist `resmat' , row("Treated Unit")
		
forval i=29/124 {

	use synth_`i', clear
	rename _time years
	gen tr_effect_`i' = _Y_treated - _Y_synthetic
	keep years tr_effect_`i'
	drop if missing(years)
	save synth_`i', replace
}

use synth_0, clear

forval i=29/124 {

	qui merge 1:1 years using synth_`i', nogenerate
}

save synth_0.dta, replace

*--------
use "$hw8dir\recycling_hw.dta", clear

encode region, gen(regionid)
tsset regionid year

replace regionid =  0 if nyc == 1

collapse nyc nj ma recyclingrate id fips collegedegree2000 incomepercapita munipop2000 democratvoteshare2000 democratvoteshare2004 nonwhite, by(year regionid)

tempname resmat
        forvalues i = 126/210 {
        quietly synth recyclingrate nonwhite incomepercapita munipop2000, trunit(`i') trperiod(2002) keep(synth_`i', replace)
        matrix `resmat' = nullmat(`resmat') \ e(RMSPE)
        local names `"`names' `"`i'"'"'
		
        }
		
forval i=126/210 {

	use synth_`i', clear
	rename _time years
	gen tr_effect_`i' = _Y_treated - _Y_synthetic
	keep years tr_effect_`i'
	drop if missing(years)
	save synth_`i', replace
}

use synth_0, clear

forval i=126/210 {

	qui merge 1:1 years using synth_`i', nogenerate
}

save synth_0.dta, replace

*****************************


*---------- rename
forval i = 0/26 {
   rename tr_effect_`i' tr_`i'
}

forval i = 29/124 {
	
	local j = `i'-2
   rename tr_effect_`i' tr_`j'
}

forval i = 126/210 {
	
	local j = `i'-3
   rename tr_effect_`i' tr_`j'
}


// plot
local lp

forval i = 0/207 {
   local lp `lp' line tr_`i' years, lcolor(gs12) ||
}

*-----create plot
twoway line tr_1-tr_99 years|| line tr_0 years, lcolor(orange) legend(off) xline(2002, lpattern(dash))

graph export "$hw8dir\output\hw8_q5c.pdf", replace

*/



*----------(e) Hints: Note that all of these plots can be generated using postestimation commands that come with synth_runner. You will need to collapse all of New York City to one treated unit to usethe canned commands. Finally, remember that these estimates