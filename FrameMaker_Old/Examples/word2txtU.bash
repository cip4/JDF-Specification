#for foo in $*; do 
echo "save files as text"
for foo in *.doc; do 
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /msaveTxt $foo
done

