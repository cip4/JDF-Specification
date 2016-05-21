#for foo in $*; do 
for foo in *.doc; do 
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /msaveUTF $foo
done

