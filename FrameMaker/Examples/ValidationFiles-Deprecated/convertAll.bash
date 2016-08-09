../word2txtU.bash
echo "move files to created txt0"
mkdir txt0
mv d:/stuff/CIP4/spec/JDF1.4/testExamples/* txt0
../convertStyles.bash
echo "save files as text with tabs"
../saveWTabs.bash
cd txt0
../../diffAllTxt.bash | tee ../diff2.txt
echo "grep all txt files for initial blanks"
grep '^ ' *.txt | tee ../grep2.txt
cd ..
echo "move files to created txt1"
mkdir txt1
mv d:/stuff/CIP4/spec/JDF1.4/testExamples/* txt1

