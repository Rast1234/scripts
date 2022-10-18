LoadPlugin("ffms2.dll")
Import("ffms2.avsi")

function GetVideoName()
{
    try
    {
        assert(false)
    }
    catch(err_msg)
    {
        err_msg = MidStr(err_msg, FindStr(err_msg, "(") + 1)
        filename = LeftStr(err_msg, StrLen(err_msg) - FindStr(RevStr(err_msg), "."))
        return filename
    }
}

function findFrame(clip src, string img, int "start", int "thresh")
{
	img1 = ImageSource(img, end=1)
	img2 = ConvertToYUV444(img1)
	thresh = Default(thresh, 2)
	start= Default(start, 0)
	img = img2.Loop(src.FrameCount, 0, 0)
	x = findFrameInternal(src, img, start, thresh)
	#if ( x == -1 )
	#{
	#	#return BlankClip(src, 0)
	#	assert(false)
	#}
	return x
}

function findFrameInternal(clip src, clip img, int start, int thresh) {
	for( i = start, src.FrameCount-1, 1 )
	{
		current_frame = i
		if( LumaDifference(src, img) <= thresh )
		{
			return i
		}
	}
	return -1
}

function findAnyFrame(v, skip_frames, thresh)
{
	x = findFrame(v, "1.png", skip_frames, thresh)
	if ( x != -1 )
	{
		return x
	}
	
	x = findFrame(v, "2.png", skip_frames, thresh)
	if ( x != -1 )
	{
		return x
	}
	
	x = findFrame(v, "3.png", skip_frames, thresh)
	if ( x != -1 )
	{
		return x
	}
	
	x = findFrame(v, "4.png", skip_frames, thresh)
	if ( x != -1 )
	{
		return x
	}
	
	assert(false)
}

#return BlankClip(color=$000000, pixel_type="RGB24").Subtitle("You would process the video [" + GetVideoName()+ "]")
v = FFmpegSource2(GetVideoName())
#return v
skip_frames = int(40*60*v.FrameRate)  # skip first 40 min

# validate first image is readable
img = ImageSource("1.png", end=1)
img2 = ConvertToYUV444(img)

x = findAnyFrame(v, skip_frames, 15)
return v.Trim(0, x)
