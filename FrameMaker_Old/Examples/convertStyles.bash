echo "Convert styles of files" 
for foo in *.doc;  do  
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /mconvertStyles $foo
done

