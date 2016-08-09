echo "diff all txt files"
for foo in *.txt; do 
echo $foo
diff $foo d:/stuff/CIP4/spec/JDF1.4/testExamples/$foo 
done 
