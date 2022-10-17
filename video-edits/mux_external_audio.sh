# for Cowboy Bebop
# generates a script to mux all external audio tracks
# into single file
# for each mkv

# for d in Rus\ Sound/*/; do echo $d; done
a='Rus Sound/Azazel (мужской, одноголосый)/'
b='Rus Sound/Digital Force (мужской, одноголосый)/'
c='Rus Sound/SkyFy (мужской, одноголосый)/'
d='Rus Sound/Евгения Лурье (женский, одноголосый)/'
e='Rus Sound/Юрий Сербин (мужской, одноголосый)/'

for x in *.mkv
do
	echo "ffmpeg -i '${x}' -i '${a}${x/mkv/mka}' -i '${b}${x/mkv/mka}' -i '${c}${x/mkv/mka}' -i '${d}${x/mkv/mka}' -i '${e}${x/mkv/mka}' \\"
	echo "-map 0:v -map 1:a -map 2:a -map 3:a -map 4:a -map 5:a -map 0:a \\"
	echo "-metadata:s:a:0 language=rus -metadata:s:a:0 title='${a}' \\"
	echo "-metadata:s:a:1 language=rus -metadata:s:a:1 title='${b}' \\"
	echo "-metadata:s:a:2 language=rus -metadata:s:a:2 title='${c}' \\"
	echo "-metadata:s:a:3 language=rus -metadata:s:a:3 title='${d}' \\"
	echo "-metadata:s:a:4 language=rus -metadata:s:a:4 title='${e}' \\"
	echo "-metadata:s:a:5 language=jpn -metadata:s:a:5 title='Original' \\"
	echo "-c:v copy -c:a copy 'converted/${x}'"
done


# ffmpeg \
# -i "[fussoir] Cowboy Bebop 01 [BDRip 1448x1080 x264 FLAC].mkv" \
# -i "Rus Sound\Azazel (мужской, одноголосый)\[fussoir] Cowboy Bebop 01 [BDRip 1448x1080 x264 FLAC].mka" \
# -i "Rus Sound\Digital Force (мужской, одноголосый)\[fussoir] Cowboy Bebop 01 [BDRip 1448x1080 x264 FLAC].mka" \
# -map 0:v -map 1:a -map 2:a -map 0:a \
# -metadata:s:a:0 language=rus -metadata:s:a:0 title="Azazel (мужской, одноголосый)" \
# -metadata:s:a:1 language=rus -metadata:s:a:1 title="Digital Force (мужской, одноголосый)" \
# -metadata:s:a:2 language=jpn -metadata:s:a:4 title="Original" \
# -c:v copy -c:a copy output.mkv