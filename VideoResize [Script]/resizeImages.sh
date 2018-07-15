INDIR="/Users/sundarkp/Documents/Personal/My Photos"
CPIMAGEDIR="/Users/sundarkp/Documents/Personal/_ResizeVideos/Images"
OUTDIR="/"

IMAGELOG="/Users/sundarkp/Documents/Personal/_ResizeVideos/_image.log"
tmpfile=$(find "$INDIR" -name "*.jpg" -type f -print0 -exec du -h {} +  | sort -rh |  cut -f2)	

ERROR="errorfile.txt"
SUCCESS="success.txt"


echo $(date) >> "$IMAGELOG"

counter=0
IFS=$'\n'
for word in $tmpfile; do
  	 directory="$(dirname $word)"  
  	 sourcefile="$(basename $word)" 

     cp  "$word" "$CPIMAGEDIR"
     output="$directory$OUTDIR$sourcefile"
     
     echo "$word" >> "$IMAGELOG"
     echo "$output"

	   counter=$((counter+1))
  	 sips -Z 960 "$output"
  	 RC=$?
  	 if [ "${RC}" -ne "0" ]; then
      	printf "$word\n" >> $ERROR 
	   else 
      	printf "$word\n" >> $SUCCESS
	   fi
done

echo "File Converted : "
echo $counter