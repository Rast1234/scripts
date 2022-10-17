# srt is taken from a file with 25FPS
# current file is 23.97FPS
# -itsscale (25/23.97) applied to input scales it, apparently back to 1.0 scale
# also srt is given language code in output
ffmpeg -i $i.mkv -itsscale 1.0427 -i $i.srt -c:v copy -c:a copy -c:s copy -map 1:s:0 -map 0:v:0 -map 0:a:1 -metadata:s:s:0 language=eng out_$i.mkv;
