######  Enter path to tagcount files folder
dir=counts
######

#convert SAS file to Excel (one case per row)

ls $dir > files

while read file
do
 echo "------- doing $file ---------"
 tr -d '\r' < $dir/$file | split -a 5 -l 12 
 for xfile in `ls x?????`
 do
  filename=$( sed -n 1p $xfile | cut -c1-60 | tr -d ' ' )
  c11=$( sed -n 1p $xfile | cut -c61-65 | tr -d ' ' )
  c12=$( sed -n 1p $xfile | cut -c66-70 | tr -d ' ' )
#  c13=$( sed -n 1p $xfile | cut -c71-75 | tr -d ' ' )  #wrcount bigger than 99999 got cut off
#  c13=$( sed -n 1p $xfile | cut -c71-76 | tr -d ' ' )
  c13=$( sed -n 1p $xfile | cut -c71- | tr -d ' ' )
   c121=$( sed -n 12p $xfile | cut -c1-10 | tr -d ' ' )
  c122=$( sed -n 12p $xfile | cut -c11-20 | tr -d ' ' )
  c123=$( sed -n 12p $xfile | cut -c21-30 | tr -d ' ' )
  c124=$( sed -n 12p $xfile | cut -c31-40 | tr -d ' ' )
  c125=$( sed -n 12p $xfile | cut -c41-50 | tr -d ' ' )
    for line in `seq 2 11`
    do
	eval c"$line"1=$(sed -n "$line"p  $xfile | cut -c1-5 | tr -d ' ' )
	eval c"$line"2=$(sed -n "$line"p  $xfile | cut -c6-10 | tr -d ' ' )
	eval c"$line"3=$(sed -n "$line"p  $xfile | cut -c11-15 | tr -d ' ' )
	eval c"$line"4=$(sed -n "$line"p  $xfile | cut -c16-20 | tr -d ' ' )
	eval c"$line"5=$(sed -n "$line"p  $xfile | cut -c21-25 | tr -d ' ' )
	eval c"$line"6=$(sed -n "$line"p  $xfile | cut -c26-30 | tr -d ' ' )
	eval c"$line"7=$(sed -n "$line"p  $xfile | cut -c31-35 | tr -d ' ' ) 
	eval c"$line"8=$(sed -n "$line"p  $xfile | cut -c36-40 | tr -d ' '  )
	eval c"$line"9=$(sed -n "$line"p  $xfile | cut -c41-45 | tr -d ' '  )
	eval c"$line"10=$(sed -n "$line"p  $xfile | cut -c46-50 | tr -d ' '  )
	eval c"$line"11=$(sed -n "$line"p  $xfile | cut -c51-55 | tr -d ' '  )
	eval c"$line"12=$(sed -n "$line"p  $xfile | cut -c56-60 | tr -d ' '  )
	eval c"$line"13=$(sed -n "$line"p  $xfile | cut -c61-65 | tr -d ' '  )
	eval c"$line"14=$(sed -n "$line"p  $xfile | cut -c66-70 | tr -d ' '  )
	eval c"$line"15=$(sed -n "$line"p  $xfile | cut -c71-75 | tr -d ' '  )
    done
  echo "$filename	$c11	$c12	$c13	$c21	$c22	$c23	$c24	$c25	$c26	$c27	$c28	$c29	$c210	$c211	$c212	$c213	$c214	$c215	$c31	$c32	$c33	$c34	$c35	$c36	$c37	$c38	$c39	$c310	$c311	$c312	$c313	$c314	$c315	$c41	$c42	$c43	$c44	$c45	$c46	$c47	$c48	$c49	$c410	$c411	$c412	$c413	$c414	$c415	$c51	$c52	$c53	$c54	$c55	$c56	$c57	$c58	$c59	$c510	$c511	$c512	$c513	$c514	$c515	$c61	$c62	$c74	$c75	$c76	$c77	$c78	$c79	$c710	$c711	$c712	$c713	$c714	$c715	$c81	$c82	$c83	$c84	$c85	$c86	$c87	$c88	$c89	$c810	$c811	$c812	$c813	$c814	$c91	$c92	$c93	$c94	$c95	$c96	$c97	$c98	$c101	$c102	$c103	$c104	$c105	$c106	$c107	$c108	$c109	$c1010	$c1011	$c1012	$c1013	$c1014	$c1015	$c111	$c112	$c113	$c114	$c115	$c116	$c117	$c118	$c119	$c1110	$c1111	$c1112	$c1113	$c1114	$c121	$c122	$c123	$c124	$c125"
 done  > "$file".temp
 cat biber_counter_header "$file".temp | grep -v '^$' > "$file".excel.tab
done < files 


rm x????? # $file.temp

###### header:
###### biber_counter_header



