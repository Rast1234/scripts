from vapoursynth import core
import vapoursynth as vs

def InterFrame(Input, Preset='Medium', Tuning='Film', NewNum=None, NewDen=1, GPU=False, InputType='2D', OverrideAlgo=None, OverrideArea=None, FrameDouble=False):
    core = vs.get_core()
    
    if not isinstance(Input, vs.VideoNode):
        raise TypeError('InterFrame: This is not a clip')
    
    # Validate inputs
    Preset = Preset.lower()
    Tuning = Tuning.lower()
    InputType = InputType.upper()
    if Preset not in ['medium', 'fast', 'faster', 'fastest']:
        raise ValueError("InterFrame: '{Preset}' is not a valid preset".format(Preset=Preset))
    if Tuning not in ['film', 'smooth', 'animation', 'weak']:
        raise ValueError("InterFrame: '{Tuning}' is not a valid tuning".format(Tuning=Tuning))
    if InputType not in ['2D', 'SBS', 'OU', 'HSBS', 'HOU']:
        raise ValueError("InterFrame: '{InputType}' is not a valid InputType".format(InputType=InputType))
    
    def InterFrameProcess(clip):
        # Create SuperString
        # force default values
        ss = {
            "pel": 2,
            "gpu": 0,
            "full": True,
            #"scale": {
            #    "up": 2,
            #    "down": 4
            #},
            #"rc": 0
        }
        if Preset in ['fast', 'faster', 'fastest']:
            #SuperString = '{pel:1,'
            ss['pel'] = 1
        else:
            #SuperString = '{'
            ss['pel'] = 2  # docs say that PEL=4 not recommended. ok then.
            pass
        
        #SuperString += 'gpu:1}' if GPU else 'gpu:0}'
        ss['gpu'] = 1 if GPU else 0
        
        # Create VectorsString
        # force default values
        vs = {  
            # 'gpu': 0,
            'vectors': 3,
            'block': {
                # 'w': 16,#
                # 'h': 16,
                # 'overlap': 2#
            },
            'main': {
                # 'levels': 0,
                'search': {
                    # 'type': 4,
                    # 'distance': -2*ss['pel'],
                    # 'sort': True,
                    # 'satd': False,
                    'coarse': {
                        # 'width': 1050,
                        # 'type': 4,
                        # 'distance': 0,
                        # 'satd': True,
                        # 'trymany': False,
                        'bad': {
                            # 'sad': 1000,
                            # 'range': -24
                        }
                    }
                },
                'penalty': {
                    # 'lambda': 10.0,
                    # 'plevel': 1.5,
                    # 'lsad': 8000,
                    # 'pnew': 50,
                    # 'pglobal': 50,
                    # 'pzero': 100,
                    # 'pnbour': 50,
                    # 'prev': 0,
                }
            },
            'refine': [ {
                # 'thsad': 200,
                'search': {
                    # 'type': 4,
                    # 'distance': ss['pel'],
                    # 'satd': False
                },
                'penalty': {
                    # 'pnew': 50
                }
            } ],
            'special': {
                # 'delta': 1
            }
        }
        if Tuning == 'animation' or Preset == 'fastest':
            #VectorsString = '{block:{w:32,'
            vs['block']['w'] = 32
            vs['block']['h'] = 32
        elif Preset in ['fast', 'faster'] or not GPU:
            #VectorsString = '{block:{w:16,'
            vs['block']['w'] = 16
            vs['block']['h'] = 16
        else:
            #VectorsString = '{block:{w:8,'
            vs['block']['w'] = 8
            vs['block']['h'] = 8
        
        if Tuning == 'animation' or Preset == 'fastest':
            #VectorsString += 'overlap:0'
            vs['block']['overlap'] = 0
        elif Preset == 'faster' and GPU:
            #VectorsString += 'overlap:1'
            vs['block']['overlap'] = 1
        else:
            #VectorsString += 'overlap:2'
            vs['block']['overlap'] = 2
        
        if Tuning == 'animation':
            #VectorsString += '},main:{search:{coarse:{type:2,'
            vs['main']['search']['coarse']['type'] = 2
        elif Preset == 'faster':
            #VectorsString += '},main:{search:{coarse:{'
            pass
        else:
            #VectorsString += '},main:{search:{distance:0,coarse:{'
            vs['main']['search']['distance'] = 0
        
        if Tuning == 'animation':
            #VectorsString += 'distance:-6,satd:false},distance:0,'
            vs['main']['search']['coarse']['distance'] = -6
            vs['main']['search']['coarse']['satd'] = False
            vs['main']['search']['distance'] = 0
        elif Tuning == 'weak':
            #VectorsString += 'distance:-1,trymany:true,'
            vs['main']['search']['coarse']['distance'] = -6
            vs['main']['search']['coarse']['trymany'] = True
        else:
            #VectorsString += 'distance:-10,'
            vs['main']['search']['coarse']['distance'] = -10
        
        vs['main']['search']['coarse']['bad']['sad'] = 2000
        if Tuning == 'animation' or Preset in ['faster', 'fastest']:
            #VectorsString += 'bad:{sad:2000}}}}}'
            pass
        elif Tuning == 'weak':
            #VectorsString += 'bad:{sad:2000}}}},refine:[{thsad:250,search:{distance:-1,satd:true}}]}'
            vs['refine'][0]['thsad'] = 250
            vs['refine'][0]['search']['distance'] = -1
            vs['refine'][0]['search']['satd'] = True
        else:
            #VectorsString += 'bad:{sad:2000}}}},refine:[{thsad:250}]}'
            vs['refine'][0]['thsad'] = 250
        
        # Create SmoothString
        sm = {   
            'rate': {
                # 'num': 2,#
                # 'den': 1,#
                # 'abs': False#
            },
            # 'algo': 13,#
            # 'block': False,
            # 'cubic': 0,
            # 'gpuid': 1,
            # 'linear': False,
            'mask': {
                # 'cover': 100,#
                # 'area': 0,#
                # 'area_sharp': 1.0#
            },
            'scene': {
                # 'mode': 3,#
                # 'blend': False,#
                'limits': {
                    #'m1': 1600,
                    #'m2': 2800,
                    #'scene': 4000,
                    #'zero': 200,
                    # 'blocks': 20#
                },
                #'luma': 1.5
            },
            # 'light': {
            #     'aspect': 0.0,
            #     'sar': 1.0,
            #     'zoom': 0.0,
            #     'lights': 16,
            #     'length': 100,
            #     'cell': 1.0,
            #     'border': 12
            # }
        }


        if NewNum is not None:
            #SmoothString = '{rate:{num:' + repr(NewNum) + ',den:' + repr(NewDen) + ',abs:true},'
            sm["rate"]["num"] = repr(NewNum)
            sm["rate"]["den"] = repr(NewDen)
            sm["rate"]["abs"] = True
        elif clip.fps_num / clip.fps_den in [15, 25, 30] or FrameDouble:
            #SmoothString = '{rate:{num:2,den:1,abs:false},'
            sm["rate"]["num"] = 2
            sm["rate"]["den"] = 1
            sm["rate"]["abs"] = False
        else:
            #SmoothString = '{rate:{num:60000,den:1001,abs:true},'
            sm["rate"]["num"] = 60000
            sm["rate"]["den"] = 1001
            sm["rate"]["abs"] = True
        
        if OverrideAlgo is not None:
            #SmoothString += 'algo:' + repr(OverrideAlgo) + ',mask:{cover:80,'
            sm["algo"] = repr(OverrideAlgo)
            sm["mask"]["cover"] = 80
        elif Tuning == 'animation':
            #SmoothString += 'algo:2,mask:{'
            sm["algo"] = 2
        elif Tuning == 'smooth':
            #SmoothString += 'algo:23,mask:{'
            sm["algo"] = 23
        else:
            #SmoothString += 'algo:13,mask:{cover:80,'
            sm["algo"] = 13
            sm["mask"]["cover"] = 80
        
        if OverrideArea is not None:
            #SmoothString += 'area:{OverrideArea}'.format(OverrideArea=OverrideArea)
            sm["mask"]["area"] = OverrideArea
        elif Tuning == 'smooth':
            #SmoothString += 'area:150'
            sm["mask"]["area"] = 150
        else:
            #SmoothString += 'area:0'
            sm["mask"]["area"] = 0
        
        if Tuning == 'weak':
            #SmoothString += ',area_sharp:1.2},scene:{blend:true,mode:0,limits:{blocks:50}}}'
            sm["mask"]["area_sharp"] = 1.2
            sm["scene"]["blend"] = True
            sm["scene"]["mode"] = 0
            sm["scene"]["limits"]["blocks"] = 50
        else:
            #SmoothString += ',area_sharp:1.2},scene:{blend:true,mode:0}}'
            sm["mask"]["area_sharp"] = 1.2
            sm["scene"]["blend"] = True
            sm["scene"]["mode"] = 0
        
        # Make interpolation vector clip
        import json

        SuperString = json.dumps(ss)
        #raise Exception(SuperString)
        Super = core.svp1.Super(clip, SuperString)
        
        VectorsString = json.dumps(vs)
        #raise Exception(VectorsString)
        Vectors = core.svp1.Analyse(Super['clip'], Super['data'], clip, VectorsString)
        
        # Put it together
        SmoothString = json.dumps(sm)
        #raise Exception(SmoothString)
        return core.svp2.SmoothFps(clip, Super['clip'], Super['data'], Vectors['clip'], Vectors['data'], SmoothString)
    
    # Get either 1 or 2 clips depending on InputType
    if InputType == 'SBS':
        FirstEye = InterFrameProcess(core.std.CropRel(Input, right=Input.width // 2))
        SecondEye = InterFrameProcess(core.std.CropRel(Input, left=Input.width // 2))
        return core.std.StackHorizontal([FirstEye, SecondEye])
    elif InputType == 'OU':
        FirstEye = InterFrameProcess(core.std.CropRel(Input, bottom=Input.height // 2))
        SecondEye = InterFrameProcess(core.std.CropRel(Input, top=Input.height // 2))
        return core.std.StackVertical([FirstEye, SecondEye])
    elif InputType == 'HSBS':
        FirstEye = InterFrameProcess(core.std.CropRel(Input, right=Input.width // 2).resize.Spline36(Input.width, Input.height))
        SecondEye = InterFrameProcess(core.std.CropRel(Input, left=Input.width // 2).resize.Spline36(Input.width, Input.height))
        return core.std.StackHorizontal([core.resize.Spline36(FirstEye, Input.width // 2, Input.height),
                                         core.resize.Spline36(SecondEye, Input.width // 2, Input.height)])
    elif InputType == 'HOU':
        FirstEye = InterFrameProcess(core.std.CropRel(Input, bottom=Input.height // 2).resize.Spline36(Input.width, Input.height))
        SecondEye = InterFrameProcess(core.std.CropRel(Input, top=Input.height // 2).resize.Spline36(Input.width, Input.height))
        return core.std.StackVertical([core.resize.Spline36(FirstEye, Input.width, Input.height // 2),
                                       core.resize.Spline36(SecondEye, Input.width, Input.height // 2)])
    else:
        return InterFrameProcess(Input)



# 'src' should be set as arg of vspipe
video = core.ffms2.Source(src)
# svpflow only accepts YV12
video = video.resize.Bicubic(format=vs.YUV420P8)
video = InterFrame(video, Tuning='animation')
video.set_output()
