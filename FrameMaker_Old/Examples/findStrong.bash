echo "find Strong Values"
for foo in *.doc; do  
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /mFindStrongNQuit $foo
done

