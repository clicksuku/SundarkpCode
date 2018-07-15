INDIR="[PHOTOSDIR]"

tmpfile=$(find "$INDIR" -name "Copy_*"  -type f)	

echo $tmpfile

IFS=$'\n'
for word in $tmpfile; do
  	 mv "$word" "`echo $word | sed 's/Copy_//'`"
done
