for foo in *.jdf; do 
#echo $foo
#root=`echo $foo|sed s/.j.f//`
echo $foo
diff $foo d:/stuff/CIP4/spec/JDF1.4/testExamples/$foo 
done 
for foo in *.jmf; do 
#echo $foo
#root=`echo $foo|sed s/.j.f//`
echo $foo
diff $foo d:/stuff/CIP4/spec/JDF1.4/testExamples/$foo
done 
