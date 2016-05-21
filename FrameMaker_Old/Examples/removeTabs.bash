mkdir noTabs
echo "noTabs created"
for foo in *.doc;  do  
echo $foo; 
d:/'Program Files'/'Microsoft Office'/OFFICE11/Winword.exe /mRemoveTabsNSave $foo
done

