
filename source 'C:\adata\web_folders_files.txt';
proc http
url="https://meps.ahrq.gov/data_stats/download_data_files.jsp"
     out=source;
run;
options obs=max;
data one ;  
 length fn $ 10 des $ 85; 
 infile source length = recLen lrecl = 32767 truncover;                                                                                                
 input string $char200.;  

 s_position=prxmatch('m/"HC-\d{3,}/i',string); 
 if find(string,'cd-rom','i')>0 then
   s_position=0;

   if s_position > 0 then do;
   pos_1=findc(string, '"');
   pos_2=findc(string, '"', 'b');
   fn=substr(string,pos_1+1,pos_2-1-pos_1);
   
   des = scan(scan(string,2, "="), -2, '<');
   des = translate(des, , '"');
   des = translate(des, , '>');
   drop pos:; 
   if s_position >0 then output;
  end;
run;
options nocenter ls=132;
  proc freq data=one;
  table fn*des /list nopercent nocum;;
  run;

  data _null_;
  set one end=end;
  link = "https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=";
  count+1;
  call symputx('macvar'||left(count),compress(link)||compress(fn));
  call symputx('xmacvar'||left(count),compbl(des));

 if end then call symputx('max',count);
  put count =;
  run;  
  %put _global_;
options symbolgen mprint;
%macro runit;
  %do i = 1 %to &max;
	filename s&i.u "C:\adata\url&i..txt";
	proc http
	url="&&macvar&i"
     out=s&i.u;
	run;
  %end;
%mend  runit;
%runit


