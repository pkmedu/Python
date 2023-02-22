%macro runit_x;
%let max = 420;
%do i = 1 %to &max;
	filename source "C:\adata\url&i..txt";
	data suburl&i (keep= des cat SAS_url); 
	 length SAS_url $ 75; 
 	 infile source truncover;                                                                                                
     input string $char200.; 
     d_position=prxmatch('m/class="OrangeBox"/',string); 
     u_position=prxmatch('m/class="sectionDividerGrey"/',string); 
 
     if d_position >0 then do;
	    des = scan(scan(scan(string, 2, '#'), 2, '>'), -2,'<') ;
		cat=1;
	 end;
	
     if u_position >0 and index(string, 'zip') > 0 then do;
 	   SAS_URL = cats('https://meps.ahrq.gov',
                     scan(string, 2, '.'),
					 '.zip'
                     );
	 cat =2;
 
 end;
  if (d_position > 0  |  u_position > 0) and cat ne .;
 
run;
%end;
%mend runit_x;
%runit_x
;

%macro allf (start, stop);
libname new 'c:\data';
 data new.allfiles;
   set 
   %do i = &start %to &stop;
     suburl&i(in=in&i)
   %end;;
 run;
%mend allf;
%allf (1,420)

/*
ods excel file = 'C:\Data\SAS_generated_URL1.xlsx'
   options (embedded_titles='on'  sheet_name='Sheet1'); 
title "Listing of MEPS SAS Data File URLS";

  proc print data= new.allfiles ;
  var SAS_url;
run;
ods excel close;
ods listing;
*/

title ;
proc sort data=new.allfiles noduprec
    out=allfiles; 
 by sas_url;
run;
ods excel file = 'C:\Data\Only_SAS_URL1.xlsx'
   options (embedded_titles='on'  sheet_name='Sheet1'); 
 proc print data= new.allfiles ;
  var SAS_url;
  where SAS_url ne ' ';
run;
ods excel close;
ods listing;
/*
 proc freq data= new.allfiles ;
  tables SAS_url /nopercent;
  where SAS_url ne ' ';
run;

title;
ods excel file = 'C:\Data\SAS_Des.xlsx'
   options (embedded_titles='on'  sheet_name='Sheet1'); 
 proc print data= new.allfiles noobs ;
  var des;
  where des ne ' ';
run;
ods excel close;
ods listing;
*/

proc print data=suburl419;
run;
