#for foo in $*; do 
for foo in *-valid.doc; do 
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /msaveUTFwTabs $foo
done

