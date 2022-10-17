# for Gurrenn Lagann
# experimental interploation to add FPS

i=4
result=""
for f in \[Winter*.mkv
do
	ext="${f##*.}"
	fn="${f%.*}"
	v=f
	a="RUS Sound/${fn}.mka"
	
	preset='faster'
	
	#file "${f}"

	#ffmpeg -i "$f" -i "$a" -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 "${i}.conv.${ext}"
	
	echo _${f}_
	
	#for preset in "ultrafast" "superfast" "veryfast" "faster" "fast" "medium"
	#do
	#for crf in 18 19 20 21 22 23 24 25 26
	#do
		preset="medium"
		crf=18
		out="${i}.60.crf${crf}.${preset}.${ext}"
		echo "$preset $out"
		SECONDS=0
		vspipe -y test.vpy -a src="$f" - \
		| ffmpeg -i pipe:0 -i "$a" -c:a copy -map 0:v:0 -map 1:a:0 \
		-c:v libx265 -preset $preset -crf $crf \
		-x265-params log-level=error \
		-y -hide_banner "${out}"
		#-t 120 \
		#crf=22:qcomp=0.8:aq-mode=1:aq_strength=1.0:qg-size=16:psy-rd=0.7:psy-rdoq=5.0:rdoq-level=1:merange=44 \
		# vspipe -a key=value
		filesize=`du "$out" | cut -f 1`
		result="${result}${crf} ${preset} = ${SECONDS}s size=${filesize}k\n"
	#done
	#done
	
		
	let i++
	#break
done

echo -e "${result}" > result.txt
echo -e "${result}"

# vapoursynth hybrid interframe mvtools2
# https://github.com/HomeOfVapourSynthEvolution/havsfunc/blob/master/havsfunc.py
