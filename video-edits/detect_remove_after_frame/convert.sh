# for Doctor Who
# detect and remove content starting from given frames
# to avoid spoilers at the end of each episode
#
# requires actual frame examples taken from video files (same resolution!)
# also requires extra ffmpeg libs (included)

set -e

# multiply script for each video
for f in *.mkv
do
	cp convert.avs "${f}.avs"
done

mkdir result || true

# test pass to see if all videos have desired frame
for avs in *.mkv.avs
do
	src=${avs%.avs*}
	echo "testing: $avs $src"
	ffmpeg -y -hide_banner -loglevel error  -i "$src" -i "$avs" -map 1:v -c:a copy -c:v libx264 -shortest -crf 30 -preset fast -t 1 "result/test_$src"
done

# process each script
for avs in *.mkv.avs
do
	src=${avs%.avs*}
	echo "$avs $src"
	# low quality fast test
	#ffmpeg -y -hide_banner  -i "$src" -i "$avs" -map 0:a -map 0:s -map 1:v -c:a copy -c:v libx264 -shortest -vf "scale=iw/4:ih/4" -crf 30 -preset ultrafast "result/$src"
	#
	# normal pass
	ffmpeg -y -hide_banner -i "$src" -i "$avs" -map 0:a -map 0:s -map 1:v -c:a copy -c:v libx264 -shortest -crf 18 -preset slower "result/$src"
	#-t 60
	#break
done

# for f in *.mkv; do ffmpeg -i $f -acodec copy -map 0:a ${f}.mka ; done
# ffmpeg-normalize.exe *.mka -c:a ac3 -b:a 640K -ar 48000 -vn -sn -mn -cn -d
# for f in *.mkv; do ffmpeg -i $f -i normalized/${f}.mkv -i ${f}.srt -map 0:v -map_metadata 0 -map_chapters 0 -map 1:a -map 2:s "-metadata:s:s:0" "language=eng" "-metadata:s:s:0" "handler_name=English" "-metadata:s:s:0" "title=English"  -acodec copy -vcodec copy -c:s srt result/${f} ; done
