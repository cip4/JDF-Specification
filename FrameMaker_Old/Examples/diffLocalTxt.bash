echo "diff all txt files"
cd txt0
for foo in *.txt; do 
echo $foo
diff $foo ../txt1/$foo 
done
echo "grep all txt0"
grep '^ ' *.txt
echo "grep all txt1"
cd ../txt1
grep '^ ' *.txt

