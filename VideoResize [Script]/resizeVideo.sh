INDIR="[PHOTOSDIR]"
CPVIDEODIR="[RESIZEDVIDEOSDIR]"
OUTDIR="/"

VIDEOLOG="[LOGDIR]/_vdo.log"
IMGLOG="[LOGDIR]/_img.log"

tmpfile=$(find "$INDIR" -name "*.vdi" -o -name "*.mov" -o -name "*.mp4" -type f -print0 -exec du -h {} +  | sort -rh | head -225 | cut -f2)	

ERROR="errorfile.txt"
SUCCESS="success.txt"


echo $(date) >> "$VIDEOLOG"

counter=0
IFS=$'\n'
for word in $tmpfile; do
  	 directory="$(dirname $word)"  
  	 sourcefile="$(basename $word)" 

     output="$directory$OUTDIR""Copy_""$sourcefile"
     echo $directory
     echo $sourcefile
     echo $output

     echo "$word" >> "$VIDEOLOG"

	   counter=$((counter+1))
  	 ffmpeg  -i "$word" -s 480x320 -c:a copy $output
  	 RC=$?
  	 if [ "${RC}" -ne "0" ]; then
      	printf "$word\n" >> $ERROR 
	   else 
      	printf "$word\n" >> $SUCCESS
	   fi

     mv  "$word" "$CPVIDEODIR"
done

echo "File Converted : "
echo $counter