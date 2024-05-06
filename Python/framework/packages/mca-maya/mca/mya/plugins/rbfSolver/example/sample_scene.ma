//Maya ASCII 2015ff05 scene
//Name: sample_scene.ma
//Last modified: Wed, Mar 11, 2015 11:13:54 AM
//Codeset: 1252
requires maya "2015ff05";
requires -nodeType "rbfSolver" "rbfSolver.py" "1.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201501210954-000000-1";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
fileInfo "RNLoadStates" "{}";
fileInfo "outsourceData" "(dp1\nS'format'\np2\nF1\nsS'misc'\np3\n(lp4\nsS'actors'\np5\n(lp6\nsS'shaders'\np7\n(lp8\nsS'references'\np9\n(lp10\nsS'audio'\np11\n(lp12\ns.";
createNode transform -s -n "persp";
	rename -uid "51DB830D-49A1-D5AD-658B-DFBCB3696828";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.0275504944504785 1.499152659415544 2.7425234857725012 ;
	setAttr ".r" -type "double3" -18.738352619143857 -1403.4000000003336 -1.980870359537586e-015 ;
	setAttr ".rp" -type "double3" 8.8817841970012523e-016 1.1102230246251565e-016 0 ;
	setAttr ".rpt" -type "double3" 1.2853862214060714e-014 1.0059808350258281e-014 7.2560219602380234e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "78AD42AB-45F7-00D4-47C4-929011E38875";
	addAttr -ci true -sn "qdbbr" -ln "qdBrightBlurRadius" -dv 8 -min 0 -max 25 -at "float";
	addAttr -ci true -sn "qdbth" -ln "qdBrightThreshold" -dv 0.5 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbmx" -ln "qdBrightMax" -dv 1 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbin" -ln "qdBrightIntensity" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdblsat" -ln "qdBloomSaturation" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdobthres" -ln "qdObjectBrightThreshold" -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdebl" -ln "qdEnableBloom" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdestar" -ln "qdEnableStars" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdedof" -ln "qdEnableDof" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdfardof" -ln "qdFarDof" -dv 6 -min 0.0010000000474974513 
		-smx 500 -at "float";
	addAttr -ci true -sn "qdfocuspl" -ln "qdFocusPlane" -dv 4 -min -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdfocusbi" -ln "qdFocusBias" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdfocusrng" -ln "qdFocusRange" -dv 1.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocussaferng" -ln "qdFocusSafeRange" -dv 0.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfrng" -ln "qdFocusFarRange" -dv 50 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfsaferng" -ln "qdFocusFarSafeRange" -dv 25 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusasymlens" -ln "qdFocusAsymmetricalLens" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "qdcircleofconf" -ln "qdCircleOfConfusion" -dv 5 -min 1 -smx 
		20 -at "float";
	addAttr -ci true -sn "qdstarsdiff" -ln "qdStarsDiffraction" -min 0 -smx 1 -at "float";
	addAttr -ci true -sn "qdstarsint" -ln "qdStarsIntensity" -dv 0.5 -min 0 -smx 12 
		-at "float";
	addAttr -ci true -sn "qdstarssize" -ln "qdStarsSize" -dv 8 -min 0 -smx 20 -at "float";
	addAttr -ci true -sn "qdstarsang" -ln "qdStarsAngle" -min 0 -max 180 -at "float";
	addAttr -ci true -sn "qdstarbranches" -ln "qdStarBranches" -dv 1 -min 0 -max 2 -en 
		"2 (streak):4 (sunny cross):6 (snow flake)" -at "enum";
	addAttr -ci true -sn "qdehdr" -ln "qdEnableHDR" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmexp" -ln "qdManualExposure" -smn -10 -smx 10 -at "float";
	addAttr -ci true -sn "qdtmoperator" -ln "qdToneMappingOperator" -min 0 -max 11 -en 
		"Linear:Reinhard:Filmic:Uncharted 2:Exponential:Logarithmic:Debug_Luminance_0:Debug_Luminance_1:Debug_Luminance_2:Debug_Luminance_3:Debug_Luminance_4:Debug_Luminance_5" 
		-at "enum";
	addAttr -ci true -sn "qdautoexp" -ln "qdAutoExposure" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmdgrey" -ln "qdMiddleGrey" -dv 0.18000000715255737 -smn 
		0.0099999997764825821 -smx 1 -at "float";
	addAttr -ci true -sn "qdautomgrey" -ln "qdAutoMiddleGrey" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdtau" -ln "qdTau" -dv 0.5 -min 0.10000000149011612 -smx 5 
		-at "float";
	addAttr -ci true -sn "qdmik" -ln "qdMinKey" -dv -8 -smn -16 -smx 0 -at "float";
	addAttr -ci true -sn "qdmak" -ln "qdMaxKey" -dv 8 -smn 0 -smx 16 -at "float";
	addAttr -ci true -sn "qdenoise" -ln "qdEnableNoise" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdnoiseint" -ln "qdNoiseIntensity" -dv 0.30000001192092896 
		-min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisecut" -ln "qdNoiseCutoff" -dv 0.5 -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisescl" -ln "qdNoiseScale" -dv 3 -min 1 -smx 10 -at "float";
	addAttr -ci true -sn "qdnoisefps" -ln "qdNoiseFPS" -dv 15 -min 1 -smx 25 -at "float";
	addAttr -ci true -sn "qdcolorfade" -ln "qdColorControlFade" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdstg0op" -ln "qdStage0_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg0prm0" -ln "qdStage0_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm1" -ln "qdStage0_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm2" -ln "qdStage0_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1op" -ln "qdStage1_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg1prm0" -ln "qdStage1_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm1" -ln "qdStage1_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm2" -ln "qdStage1_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2op" -ln "qdStage2_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg2prm0" -ln "qdStage2_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm1" -ln "qdStage2_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm2" -ln "qdStage2_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3op" -ln "qdStage3_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg3prm0" -ln "qdStage3_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm1" -ln "qdStage3_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm2" -ln "qdStage3_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4op" -ln "qdStage4_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg4prm0" -ln "qdStage4_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm1" -ln "qdStage4_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm2" -ln "qdStage4_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5op" -ln "qdStage5_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg5prm0" -ln "qdStage5_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm1" -ln "qdStage5_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm2" -ln "qdStage5_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6op" -ln "qdStage6_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg6prm0" -ln "qdStage6_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm1" -ln "qdStage6_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm2" -ln "qdStage6_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7op" -ln "qdStage7_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg7prm0" -ln "qdStage7_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm1" -ln "qdStage7_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm2" -ln "qdStage7_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8op" -ln "qdStage8_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg8prm0" -ln "qdStage8_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm1" -ln "qdStage8_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm2" -ln "qdStage8_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9op" -ln "qdStage9_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg9prm0" -ln "qdStage9_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm1" -ln "qdStage9_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm2" -ln "qdStage9_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdbleachamt" -ln "qdBleachAmount" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdbleachctst" -ln "qdBleachContrast" -dv 1.5 -min 0 -max 10 
		-at "float";
	addAttr -ci true -sn "qdbleachbias" -ln "qdBleachBias" -min -10 -max 10 -at "float";
	addAttr -ci true -uac -k true -sn "qdbleachcol" -ln "qdBleachColor" -at "float3" 
		-nc 3;
	addAttr -ci true -k true -sn "qdbleachcolr" -ln "qdBleachColorR" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolg" -ln "qdBleachColorG" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolb" -ln "qdBleachColorB" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -sn "qdcamshader" -ln "qdCameraShader" -at "float";
	addAttr -ci true -uac -k true -sn "qdblc1" -ln "qdBloomColor1" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc1r" -ln "qdBloomColor1R" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1g" -ln "qdBloomColor1G" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1b" -ln "qdBloomColor1B" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -uac -k true -sn "qdblc2" -ln "qdBloomColor2" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc2r" -ln "qdBloomColor2R" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2g" -ln "qdBloomColor2G" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2b" -ln "qdBloomColor2B" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -uac -k true -sn "qdblc3" -ln "qdBloomColor3" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc3r" -ln "qdBloomColor3R" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3g" -ln "qdBloomColor3G" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3b" -ln "qdBloomColor3B" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -uac -k true -sn "qdblc4" -ln "qdBloomColor4" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc4r" -ln "qdBloomColor4R" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4g" -ln "qdBloomColor4G" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4b" -ln "qdBloomColor4B" -dv 1 -at "float" -p "qdBloomColor4";
	setAttr -k off ".v" no;
	setAttr ".cap" -type "double2" 1 1 ;
	setAttr ".fl" 16.551;
	setAttr ".coi" 3.9440432594686365;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -1.1102230246251565e-016 0 0 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "470D2422-40D5-278F-68C2-D399468496BD";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999972 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "2EB72397-43E1-1567-9FE8-35A2908E9E25";
	addAttr -ci true -sn "qdbbr" -ln "qdBrightBlurRadius" -dv 8 -min 0 -max 25 -at "float";
	addAttr -ci true -sn "qdbth" -ln "qdBrightThreshold" -dv 0.5 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbmx" -ln "qdBrightMax" -dv 1 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbin" -ln "qdBrightIntensity" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdblsat" -ln "qdBloomSaturation" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdobthres" -ln "qdObjectBrightThreshold" -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdebl" -ln "qdEnableBloom" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdestar" -ln "qdEnableStars" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdedof" -ln "qdEnableDof" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdfardof" -ln "qdFarDof" -dv 6 -min 0.0010000000474974513 
		-smx 500 -at "float";
	addAttr -ci true -sn "qdfocuspl" -ln "qdFocusPlane" -dv 4 -min -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdfocusbi" -ln "qdFocusBias" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdfocusrng" -ln "qdFocusRange" -dv 1.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocussaferng" -ln "qdFocusSafeRange" -dv 0.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfrng" -ln "qdFocusFarRange" -dv 50 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfsaferng" -ln "qdFocusFarSafeRange" -dv 25 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusasymlens" -ln "qdFocusAsymmetricalLens" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "qdcircleofconf" -ln "qdCircleOfConfusion" -dv 5 -min 1 -smx 
		20 -at "float";
	addAttr -ci true -sn "qdstarsdiff" -ln "qdStarsDiffraction" -min 0 -smx 1 -at "float";
	addAttr -ci true -sn "qdstarsint" -ln "qdStarsIntensity" -dv 0.5 -min 0 -smx 12 
		-at "float";
	addAttr -ci true -sn "qdstarssize" -ln "qdStarsSize" -dv 8 -min 0 -smx 20 -at "float";
	addAttr -ci true -sn "qdstarsang" -ln "qdStarsAngle" -min 0 -max 180 -at "float";
	addAttr -ci true -sn "qdstarbranches" -ln "qdStarBranches" -dv 1 -min 0 -max 2 -en 
		"2 (streak):4 (sunny cross):6 (snow flake)" -at "enum";
	addAttr -ci true -sn "qdehdr" -ln "qdEnableHDR" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmexp" -ln "qdManualExposure" -smn -10 -smx 10 -at "float";
	addAttr -ci true -sn "qdtmoperator" -ln "qdToneMappingOperator" -min 0 -max 11 -en 
		"Linear:Reinhard:Filmic:Uncharted 2:Exponential:Logarithmic:Debug_Luminance_0:Debug_Luminance_1:Debug_Luminance_2:Debug_Luminance_3:Debug_Luminance_4:Debug_Luminance_5" 
		-at "enum";
	addAttr -ci true -sn "qdautoexp" -ln "qdAutoExposure" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmdgrey" -ln "qdMiddleGrey" -dv 0.18000000715255737 -smn 
		0.0099999997764825821 -smx 1 -at "float";
	addAttr -ci true -sn "qdautomgrey" -ln "qdAutoMiddleGrey" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdtau" -ln "qdTau" -dv 0.5 -min 0.10000000149011612 -smx 5 
		-at "float";
	addAttr -ci true -sn "qdmik" -ln "qdMinKey" -dv -8 -smn -16 -smx 0 -at "float";
	addAttr -ci true -sn "qdmak" -ln "qdMaxKey" -dv 8 -smn 0 -smx 16 -at "float";
	addAttr -ci true -sn "qdenoise" -ln "qdEnableNoise" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdnoiseint" -ln "qdNoiseIntensity" -dv 0.30000001192092896 
		-min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisecut" -ln "qdNoiseCutoff" -dv 0.5 -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisescl" -ln "qdNoiseScale" -dv 3 -min 1 -smx 10 -at "float";
	addAttr -ci true -sn "qdnoisefps" -ln "qdNoiseFPS" -dv 15 -min 1 -smx 25 -at "float";
	addAttr -ci true -sn "qdcolorfade" -ln "qdColorControlFade" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdstg0op" -ln "qdStage0_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg0prm0" -ln "qdStage0_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm1" -ln "qdStage0_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm2" -ln "qdStage0_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1op" -ln "qdStage1_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg1prm0" -ln "qdStage1_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm1" -ln "qdStage1_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm2" -ln "qdStage1_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2op" -ln "qdStage2_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg2prm0" -ln "qdStage2_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm1" -ln "qdStage2_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm2" -ln "qdStage2_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3op" -ln "qdStage3_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg3prm0" -ln "qdStage3_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm1" -ln "qdStage3_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm2" -ln "qdStage3_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4op" -ln "qdStage4_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg4prm0" -ln "qdStage4_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm1" -ln "qdStage4_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm2" -ln "qdStage4_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5op" -ln "qdStage5_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg5prm0" -ln "qdStage5_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm1" -ln "qdStage5_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm2" -ln "qdStage5_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6op" -ln "qdStage6_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg6prm0" -ln "qdStage6_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm1" -ln "qdStage6_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm2" -ln "qdStage6_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7op" -ln "qdStage7_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg7prm0" -ln "qdStage7_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm1" -ln "qdStage7_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm2" -ln "qdStage7_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8op" -ln "qdStage8_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg8prm0" -ln "qdStage8_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm1" -ln "qdStage8_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm2" -ln "qdStage8_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9op" -ln "qdStage9_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg9prm0" -ln "qdStage9_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm1" -ln "qdStage9_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm2" -ln "qdStage9_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdbleachamt" -ln "qdBleachAmount" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdbleachctst" -ln "qdBleachContrast" -dv 1.5 -min 0 -max 10 
		-at "float";
	addAttr -ci true -sn "qdbleachbias" -ln "qdBleachBias" -min -10 -max 10 -at "float";
	addAttr -ci true -uac -k true -sn "qdbleachcol" -ln "qdBleachColor" -at "float3" 
		-nc 3;
	addAttr -ci true -k true -sn "qdbleachcolr" -ln "qdBleachColorR" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolg" -ln "qdBleachColorG" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolb" -ln "qdBleachColorB" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -sn "qdcamshader" -ln "qdCameraShader" -at "float";
	addAttr -ci true -uac -k true -sn "qdblc1" -ln "qdBloomColor1" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc1r" -ln "qdBloomColor1R" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1g" -ln "qdBloomColor1G" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1b" -ln "qdBloomColor1B" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -uac -k true -sn "qdblc2" -ln "qdBloomColor2" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc2r" -ln "qdBloomColor2R" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2g" -ln "qdBloomColor2G" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2b" -ln "qdBloomColor2B" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -uac -k true -sn "qdblc3" -ln "qdBloomColor3" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc3r" -ln "qdBloomColor3R" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3g" -ln "qdBloomColor3G" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3b" -ln "qdBloomColor3B" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -uac -k true -sn "qdblc4" -ln "qdBloomColor4" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc4r" -ln "qdBloomColor4R" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4g" -ln "qdBloomColor4G" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4b" -ln "qdBloomColor4B" -dv 1 -at "float" -p "qdBloomColor4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "2FFCFA13-4751-2C45-BEA2-21ADF3474310";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "DF853DC4-448F-D0CF-C1DE-61B6A56414F9";
	addAttr -ci true -sn "qdbbr" -ln "qdBrightBlurRadius" -dv 8 -min 0 -max 25 -at "float";
	addAttr -ci true -sn "qdbth" -ln "qdBrightThreshold" -dv 0.5 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbmx" -ln "qdBrightMax" -dv 1 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbin" -ln "qdBrightIntensity" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdblsat" -ln "qdBloomSaturation" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdobthres" -ln "qdObjectBrightThreshold" -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdebl" -ln "qdEnableBloom" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdestar" -ln "qdEnableStars" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdedof" -ln "qdEnableDof" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdfardof" -ln "qdFarDof" -dv 6 -min 0.0010000000474974513 
		-smx 500 -at "float";
	addAttr -ci true -sn "qdfocuspl" -ln "qdFocusPlane" -dv 4 -min -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdfocusbi" -ln "qdFocusBias" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdfocusrng" -ln "qdFocusRange" -dv 1.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocussaferng" -ln "qdFocusSafeRange" -dv 0.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfrng" -ln "qdFocusFarRange" -dv 50 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfsaferng" -ln "qdFocusFarSafeRange" -dv 25 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusasymlens" -ln "qdFocusAsymmetricalLens" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "qdcircleofconf" -ln "qdCircleOfConfusion" -dv 5 -min 1 -smx 
		20 -at "float";
	addAttr -ci true -sn "qdstarsdiff" -ln "qdStarsDiffraction" -min 0 -smx 1 -at "float";
	addAttr -ci true -sn "qdstarsint" -ln "qdStarsIntensity" -dv 0.5 -min 0 -smx 12 
		-at "float";
	addAttr -ci true -sn "qdstarssize" -ln "qdStarsSize" -dv 8 -min 0 -smx 20 -at "float";
	addAttr -ci true -sn "qdstarsang" -ln "qdStarsAngle" -min 0 -max 180 -at "float";
	addAttr -ci true -sn "qdstarbranches" -ln "qdStarBranches" -dv 1 -min 0 -max 2 -en 
		"2 (streak):4 (sunny cross):6 (snow flake)" -at "enum";
	addAttr -ci true -sn "qdehdr" -ln "qdEnableHDR" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmexp" -ln "qdManualExposure" -smn -10 -smx 10 -at "float";
	addAttr -ci true -sn "qdtmoperator" -ln "qdToneMappingOperator" -min 0 -max 11 -en 
		"Linear:Reinhard:Filmic:Uncharted 2:Exponential:Logarithmic:Debug_Luminance_0:Debug_Luminance_1:Debug_Luminance_2:Debug_Luminance_3:Debug_Luminance_4:Debug_Luminance_5" 
		-at "enum";
	addAttr -ci true -sn "qdautoexp" -ln "qdAutoExposure" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmdgrey" -ln "qdMiddleGrey" -dv 0.18000000715255737 -smn 
		0.0099999997764825821 -smx 1 -at "float";
	addAttr -ci true -sn "qdautomgrey" -ln "qdAutoMiddleGrey" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdtau" -ln "qdTau" -dv 0.5 -min 0.10000000149011612 -smx 5 
		-at "float";
	addAttr -ci true -sn "qdmik" -ln "qdMinKey" -dv -8 -smn -16 -smx 0 -at "float";
	addAttr -ci true -sn "qdmak" -ln "qdMaxKey" -dv 8 -smn 0 -smx 16 -at "float";
	addAttr -ci true -sn "qdenoise" -ln "qdEnableNoise" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdnoiseint" -ln "qdNoiseIntensity" -dv 0.30000001192092896 
		-min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisecut" -ln "qdNoiseCutoff" -dv 0.5 -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisescl" -ln "qdNoiseScale" -dv 3 -min 1 -smx 10 -at "float";
	addAttr -ci true -sn "qdnoisefps" -ln "qdNoiseFPS" -dv 15 -min 1 -smx 25 -at "float";
	addAttr -ci true -sn "qdcolorfade" -ln "qdColorControlFade" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdstg0op" -ln "qdStage0_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg0prm0" -ln "qdStage0_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm1" -ln "qdStage0_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm2" -ln "qdStage0_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1op" -ln "qdStage1_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg1prm0" -ln "qdStage1_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm1" -ln "qdStage1_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm2" -ln "qdStage1_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2op" -ln "qdStage2_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg2prm0" -ln "qdStage2_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm1" -ln "qdStage2_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm2" -ln "qdStage2_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3op" -ln "qdStage3_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg3prm0" -ln "qdStage3_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm1" -ln "qdStage3_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm2" -ln "qdStage3_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4op" -ln "qdStage4_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg4prm0" -ln "qdStage4_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm1" -ln "qdStage4_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm2" -ln "qdStage4_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5op" -ln "qdStage5_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg5prm0" -ln "qdStage5_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm1" -ln "qdStage5_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm2" -ln "qdStage5_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6op" -ln "qdStage6_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg6prm0" -ln "qdStage6_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm1" -ln "qdStage6_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm2" -ln "qdStage6_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7op" -ln "qdStage7_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg7prm0" -ln "qdStage7_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm1" -ln "qdStage7_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm2" -ln "qdStage7_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8op" -ln "qdStage8_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg8prm0" -ln "qdStage8_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm1" -ln "qdStage8_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm2" -ln "qdStage8_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9op" -ln "qdStage9_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg9prm0" -ln "qdStage9_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm1" -ln "qdStage9_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm2" -ln "qdStage9_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdbleachamt" -ln "qdBleachAmount" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdbleachctst" -ln "qdBleachContrast" -dv 1.5 -min 0 -max 10 
		-at "float";
	addAttr -ci true -sn "qdbleachbias" -ln "qdBleachBias" -min -10 -max 10 -at "float";
	addAttr -ci true -uac -k true -sn "qdbleachcol" -ln "qdBleachColor" -at "float3" 
		-nc 3;
	addAttr -ci true -k true -sn "qdbleachcolr" -ln "qdBleachColorR" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolg" -ln "qdBleachColorG" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolb" -ln "qdBleachColorB" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -sn "qdcamshader" -ln "qdCameraShader" -at "float";
	addAttr -ci true -uac -k true -sn "qdblc1" -ln "qdBloomColor1" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc1r" -ln "qdBloomColor1R" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1g" -ln "qdBloomColor1G" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1b" -ln "qdBloomColor1B" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -uac -k true -sn "qdblc2" -ln "qdBloomColor2" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc2r" -ln "qdBloomColor2R" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2g" -ln "qdBloomColor2G" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2b" -ln "qdBloomColor2B" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -uac -k true -sn "qdblc3" -ln "qdBloomColor3" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc3r" -ln "qdBloomColor3R" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3g" -ln "qdBloomColor3G" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3b" -ln "qdBloomColor3B" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -uac -k true -sn "qdblc4" -ln "qdBloomColor4" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc4r" -ln "qdBloomColor4R" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4g" -ln "qdBloomColor4G" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4b" -ln "qdBloomColor4B" -dv 1 -at "float" -p "qdBloomColor4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "FDD1E8FB-486B-952E-1579-97841F24C204";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999972 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "D88973B0-47AD-BE01-6AA0-FD8676F8DE46";
	addAttr -ci true -sn "qdbbr" -ln "qdBrightBlurRadius" -dv 8 -min 0 -max 25 -at "float";
	addAttr -ci true -sn "qdbth" -ln "qdBrightThreshold" -dv 0.5 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbmx" -ln "qdBrightMax" -dv 1 -min 0 -max 16 -at "float";
	addAttr -ci true -sn "qdbin" -ln "qdBrightIntensity" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdblsat" -ln "qdBloomSaturation" -dv 1 -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdobthres" -ln "qdObjectBrightThreshold" -min 0 -smx 5 -at "float";
	addAttr -ci true -sn "qdebl" -ln "qdEnableBloom" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdestar" -ln "qdEnableStars" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdedof" -ln "qdEnableDof" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdfardof" -ln "qdFarDof" -dv 6 -min 0.0010000000474974513 
		-smx 500 -at "float";
	addAttr -ci true -sn "qdfocuspl" -ln "qdFocusPlane" -dv 4 -min -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdfocusbi" -ln "qdFocusBias" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdfocusrng" -ln "qdFocusRange" -dv 1.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocussaferng" -ln "qdFocusSafeRange" -dv 0.5 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfrng" -ln "qdFocusFarRange" -dv 50 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusfsaferng" -ln "qdFocusFarSafeRange" -dv 25 -min 0.0010000000474974513 
		-smx 5 -at "float";
	addAttr -ci true -sn "qdfocusasymlens" -ln "qdFocusAsymmetricalLens" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "qdcircleofconf" -ln "qdCircleOfConfusion" -dv 5 -min 1 -smx 
		20 -at "float";
	addAttr -ci true -sn "qdstarsdiff" -ln "qdStarsDiffraction" -min 0 -smx 1 -at "float";
	addAttr -ci true -sn "qdstarsint" -ln "qdStarsIntensity" -dv 0.5 -min 0 -smx 12 
		-at "float";
	addAttr -ci true -sn "qdstarssize" -ln "qdStarsSize" -dv 8 -min 0 -smx 20 -at "float";
	addAttr -ci true -sn "qdstarsang" -ln "qdStarsAngle" -min 0 -max 180 -at "float";
	addAttr -ci true -sn "qdstarbranches" -ln "qdStarBranches" -dv 1 -min 0 -max 2 -en 
		"2 (streak):4 (sunny cross):6 (snow flake)" -at "enum";
	addAttr -ci true -sn "qdehdr" -ln "qdEnableHDR" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmexp" -ln "qdManualExposure" -smn -10 -smx 10 -at "float";
	addAttr -ci true -sn "qdtmoperator" -ln "qdToneMappingOperator" -min 0 -max 11 -en 
		"Linear:Reinhard:Filmic:Uncharted 2:Exponential:Logarithmic:Debug_Luminance_0:Debug_Luminance_1:Debug_Luminance_2:Debug_Luminance_3:Debug_Luminance_4:Debug_Luminance_5" 
		-at "enum";
	addAttr -ci true -sn "qdautoexp" -ln "qdAutoExposure" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdmdgrey" -ln "qdMiddleGrey" -dv 0.18000000715255737 -smn 
		0.0099999997764825821 -smx 1 -at "float";
	addAttr -ci true -sn "qdautomgrey" -ln "qdAutoMiddleGrey" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdtau" -ln "qdTau" -dv 0.5 -min 0.10000000149011612 -smx 5 
		-at "float";
	addAttr -ci true -sn "qdmik" -ln "qdMinKey" -dv -8 -smn -16 -smx 0 -at "float";
	addAttr -ci true -sn "qdmak" -ln "qdMaxKey" -dv 8 -smn 0 -smx 16 -at "float";
	addAttr -ci true -sn "qdenoise" -ln "qdEnableNoise" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "qdnoiseint" -ln "qdNoiseIntensity" -dv 0.30000001192092896 
		-min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisecut" -ln "qdNoiseCutoff" -dv 0.5 -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdnoisescl" -ln "qdNoiseScale" -dv 3 -min 1 -smx 10 -at "float";
	addAttr -ci true -sn "qdnoisefps" -ln "qdNoiseFPS" -dv 15 -min 1 -smx 25 -at "float";
	addAttr -ci true -sn "qdcolorfade" -ln "qdColorControlFade" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdstg0op" -ln "qdStage0_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg0prm0" -ln "qdStage0_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm1" -ln "qdStage0_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg0prm2" -ln "qdStage0_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1op" -ln "qdStage1_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg1prm0" -ln "qdStage1_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm1" -ln "qdStage1_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg1prm2" -ln "qdStage1_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2op" -ln "qdStage2_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg2prm0" -ln "qdStage2_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm1" -ln "qdStage2_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg2prm2" -ln "qdStage2_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3op" -ln "qdStage3_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg3prm0" -ln "qdStage3_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm1" -ln "qdStage3_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg3prm2" -ln "qdStage3_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4op" -ln "qdStage4_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg4prm0" -ln "qdStage4_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm1" -ln "qdStage4_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg4prm2" -ln "qdStage4_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5op" -ln "qdStage5_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg5prm0" -ln "qdStage5_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm1" -ln "qdStage5_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg5prm2" -ln "qdStage5_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6op" -ln "qdStage6_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg6prm0" -ln "qdStage6_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm1" -ln "qdStage6_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg6prm2" -ln "qdStage6_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7op" -ln "qdStage7_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg7prm0" -ln "qdStage7_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm1" -ln "qdStage7_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg7prm2" -ln "qdStage7_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8op" -ln "qdStage8_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg8prm0" -ln "qdStage8_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm1" -ln "qdStage8_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg8prm2" -ln "qdStage8_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9op" -ln "qdStage9_Op" -min 0 -max 7 -en "(None):Add:Multiply:Hue:Saturation:Invert:Screen:Brightness/Contrast" 
		-at "enum";
	addAttr -ci true -sn "qdstg9prm0" -ln "qdStage9_Param0" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm1" -ln "qdStage9_Param1" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdstg9prm2" -ln "qdStage9_Param2" -smn -1 -smx 1 -at "float";
	addAttr -ci true -sn "qdbleachamt" -ln "qdBleachAmount" -min 0 -max 1 -at "float";
	addAttr -ci true -sn "qdbleachctst" -ln "qdBleachContrast" -dv 1.5 -min 0 -max 10 
		-at "float";
	addAttr -ci true -sn "qdbleachbias" -ln "qdBleachBias" -min -10 -max 10 -at "float";
	addAttr -ci true -uac -k true -sn "qdbleachcol" -ln "qdBleachColor" -at "float3" 
		-nc 3;
	addAttr -ci true -k true -sn "qdbleachcolr" -ln "qdBleachColorR" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolg" -ln "qdBleachColorG" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -k true -sn "qdbleachcolb" -ln "qdBleachColorB" -dv 1 -at "float" 
		-p "qdBleachColor";
	addAttr -ci true -sn "qdcamshader" -ln "qdCameraShader" -at "float";
	addAttr -ci true -uac -k true -sn "qdblc1" -ln "qdBloomColor1" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc1r" -ln "qdBloomColor1R" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1g" -ln "qdBloomColor1G" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -k true -sn "qdblc1b" -ln "qdBloomColor1B" -dv 1 -at "float" -p "qdBloomColor1";
	addAttr -ci true -uac -k true -sn "qdblc2" -ln "qdBloomColor2" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc2r" -ln "qdBloomColor2R" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2g" -ln "qdBloomColor2G" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -k true -sn "qdblc2b" -ln "qdBloomColor2B" -dv 1 -at "float" -p "qdBloomColor2";
	addAttr -ci true -uac -k true -sn "qdblc3" -ln "qdBloomColor3" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc3r" -ln "qdBloomColor3R" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3g" -ln "qdBloomColor3G" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -k true -sn "qdblc3b" -ln "qdBloomColor3B" -dv 1 -at "float" -p "qdBloomColor3";
	addAttr -ci true -uac -k true -sn "qdblc4" -ln "qdBloomColor4" -at "float3" -nc 
		3;
	addAttr -ci true -k true -sn "qdblc4r" -ln "qdBloomColor4R" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4g" -ln "qdBloomColor4G" -dv 1 -at "float" -p "qdBloomColor4";
	addAttr -ci true -k true -sn "qdblc4b" -ln "qdBloomColor4B" -dv 1 -at "float" -p "qdBloomColor4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "unused";
	rename -uid "0865E8BB-4793-2A02-493E-00B83FF0CB5E";
createNode nurbsSurface -n "unusedShape" -p "unused";
	rename -uid "A9AB8D57-406C-CDB5-ED70-A3989566A516";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode joint -n "rotate_me";
	rename -uid "F8470021-48CD-6C00-098E-39B1ED69564A";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0;
createNode nurbsCurve -n "nurbsCurve4" -p "rotate_me";
	rename -uid "D1C121E9-4253-E22C-079E-23894C71FC23";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 1;
	setAttr ".cc" -type "nurbsCurve" 
		3 14 0 no 3
		19 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 14 14
		17
		0 0 0
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 0.1003006354 -2.227121496e-017
		1.4032587030951462 0.1332686387 -2.9591582230000001e-017
		1.4362264956951463 0.1504507424 -3.340677566e-017
		1.6368271343951462 0.1504507424 -3.340677566e-017
		1.6697959804951461 0.1332686387 -2.9591582230000001e-017
		1.6869780842951463 0.1003006354 -2.227121496e-017
		1.6869780842951463 -0.1003006354 2.227121496e-017
		1.6697959804951461 -0.1332686387 2.9591582230000001e-017
		1.6368271343951462 -0.1504507424 3.340677566e-017
		1.4362264956951463 -0.1504507424 3.340677566e-017
		1.4032587030951462 -0.1332686387 2.9591582230000001e-017
		1.3860765993951463 -0.1003006354 2.227121496e-017
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		;
createNode nurbsCurve -n "nurbsCurve11" -p "rotate_me";
	rename -uid "208D60BB-49AB-D804-ED48-2BA627CF2007";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 1;
	setAttr ".cc" -type "nurbsCurve" 
		3 14 0 no 3
		19 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 14 14
		17
		0 0 0
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		1.3860765993951463 0.1003006354 -2.227121496e-017
		1.4032587030951462 0.1332686387 -2.9591582230000001e-017
		1.4362264956951463 0.1504507424 -3.340677566e-017
		1.6368271343951462 0.1504507424 -3.340677566e-017
		1.6697959804951461 0.1332686387 -2.9591582230000001e-017
		1.6869780842951463 0.1003006354 -2.227121496e-017
		1.6869780842951463 -0.1003006354 2.227121496e-017
		1.6697959804951461 -0.1332686387 2.9591582230000001e-017
		1.6368271343951462 -0.1504507424 3.340677566e-017
		1.4362264956951463 -0.1504507424 3.340677566e-017
		1.4032587030951462 -0.1332686387 2.9591582230000001e-017
		1.3860765993951463 -0.1003006354 2.227121496e-017
		1.3860765993951463 -1.5529999780000001e-016 3.4483526649999999e-032
		;
createNode transform -n "poses";
	rename -uid "BEC1DF52-4228-9A2C-D016-A3B53CB9347E";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	setAttr ".qdGuid" -type "string" "7433ad6f-8fcf-47d0-85d0-d0353fd6b3e9";
createNode transform -n "pose1" -p "poses";
	rename -uid "9C1F64F1-4D6D-806C-6AB2-E7BE6AE30332";
	setAttr ".t" -type "double3" -0.65416021571030991 -0.72649113069564186 -0.21044013210984439 ;
createNode nurbsSurface -n "pose1Shape" -p "pose1";
	rename -uid "35121E36-4E91-02A2-BFB2-B09119B6D124";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose2" -p "poses";
	rename -uid "436233BB-4A30-A6EA-FF31-0FB4352C497A";
	setAttr ".t" -type "double3" -0.95433688629961055 -0.29434428493716491 0.035710205049174881 ;
createNode nurbsSurface -n "pose2Shape" -p "pose2";
	rename -uid "67333308-40DD-652F-6A0D-55803FCC295D";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose3" -p "poses";
	rename -uid "62660309-4820-95DF-7F04-96A48F736D15";
	setAttr ".t" -type "double3" -0.89774139812676812 0.033254202014351669 -0.43926591051182717 ;
createNode nurbsSurface -n "pose3Shape" -p "pose3";
	rename -uid "80F26467-427B-6B45-C751-22A0E58A4E1A";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose4" -p "poses";
	rename -uid "C9E4DB2A-4858-3E9B-1908-8AACFDC63A16";
	setAttr ".t" -type "double3" -0.69158269045915544 0.34944324081231892 0.63103747395052101 ;
createNode nurbsSurface -n "pose4Shape" -p "pose4";
	rename -uid "C1938BC4-451E-A0FC-6E58-93A669AA7834";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose5" -p "poses";
	rename -uid "7750C8BC-4407-0D29-E8CE-FB85E519A5DF";
	setAttr ".t" -type "double3" -0.68362636490402084 0.65267241306960777 -0.32660942182675878 ;
createNode nurbsSurface -n "pose5Shape" -p "pose5";
	rename -uid "1B4D0235-4B21-1138-A139-92AB7BCB007C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose6" -p "poses";
	rename -uid "81FD7B91-4DA7-0936-893B-4C8C897B3324";
	setAttr ".t" -type "double3" 0 0.99487688422663934 0.097082476949578125 ;
createNode nurbsSurface -n "pose6Shape" -p "pose6";
	rename -uid "14EE3C4C-45D6-3516-F87A-33B6CA3E745A";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose7" -p "poses";
	rename -uid "72A11936-4660-DD31-B29F-009BF1A19392";
	setAttr ".t" -type "double3" 0.10821742144295798 0.29369797852085294 -0.94882431946263157 ;
createNode nurbsSurface -n "pose7Shape" -p "pose7";
	rename -uid "EAACDBE9-463C-6E31-44F9-FFAF7B855A11";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose8" -p "poses";
	rename -uid "4D4F8379-426F-47D4-CD41-A89D3D62E64E";
	setAttr ".t" -type "double3" -0.52787528114839966 0.061001280190414064 -0.84613841500284848 ;
createNode nurbsSurface -n "pose8Shape" -p "pose8";
	rename -uid "F0BFCF3E-49EF-C809-4354-4BA6D88CE621";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose9" -p "poses";
	rename -uid "E2C5DB3E-4F05-6B0A-0416-A79692726E92";
	setAttr ".t" -type "double3" -0.35655666610487641 -0.18331873660987158 0.91611221182993552 ;
createNode nurbsSurface -n "pose9Shape" -p "pose9";
	rename -uid "2083B8E8-4B1D-BD28-A8CC-8DA69B6453D1";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose10" -p "poses";
	rename -uid "55589E7C-456E-E6E9-001C-B29E3450F144";
	setAttr ".t" -type "double3" -0.095749777900253893 -0.98945011606460065 -0.10872188304016978 ;
createNode nurbsSurface -n "pose10Shape" -p "pose10";
	rename -uid "141EED56-45AC-CE9A-5D1E-48BEEA659ED6";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose11" -p "poses";
	rename -uid "9B9844F7-4987-08B8-6C7C-39B5CD554E50";
	setAttr ".t" -type "double3" 0.63134196198639914 0.77358741614350479 -0.054496207387123199 ;
createNode nurbsSurface -n "pose11Shape" -p "pose11";
	rename -uid "F5A50063-4DB1-D55C-6D73-57BC362D957F";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose12" -p "poses";
	rename -uid "A59D8DAF-491C-D756-E8E0-DE8EC6CB6DC6";
	setAttr ".t" -type "double3" -0.22780039646518935 0.55024455651172155 0.80332926462287002 ;
createNode nurbsSurface -n "pose12Shape" -p "pose12";
	rename -uid "1C30B0AB-48F4-DA6E-48FE-05A71C85680C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose13" -p "poses";
	rename -uid "6F2A18FC-4BF1-9F46-70B0-0C9E204478A9";
	setAttr ".t" -type "double3" -0.50549629082437408 0.80253480035254654 0.31261113257394219 ;
createNode nurbsSurface -n "pose13Shape" -p "pose13";
	rename -uid "242CDB67-46B6-8F31-7607-C9A1CDBF514E";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose14" -p "poses";
	rename -uid "398D9CDE-42EB-26DE-5A35-29979E831201";
	setAttr ".t" -type "double3" 0.8680232743919637 -0.038407499808486345 -0.49310028512058746 ;
createNode nurbsSurface -n "pose14Shape" -p "pose14";
	rename -uid "227DD60D-4262-7838-852C-FAB5AC5EC576";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose15" -p "poses";
	rename -uid "EE8CD225-4298-0EAB-4386-1A9FB63D4478";
	setAttr ".t" -type "double3" -0.065471071184461244 -0.34813005613344206 0.93515720756164078 ;
createNode nurbsSurface -n "pose15Shape" -p "pose15";
	rename -uid "6476A1ED-40F9-9E41-DAEC-39AFAA7C7020";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose16" -p "poses";
	rename -uid "14DCD696-4DF0-C82A-37F8-7D86EC2ABC0B";
	setAttr ".t" -type "double3" -0.82548290351213804 -0.31065932343468733 0.46807948061642668 ;
createNode nurbsSurface -n "pose16Shape" -p "pose16";
	rename -uid "3C3FB7F2-48D8-AA0E-D6CF-BD844854D102";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose17" -p "poses";
	rename -uid "2D7932CB-45F6-40D5-4683-898201FDA6D4";
	setAttr ".t" -type "double3" 0.16193986151930134 -0.98537564839269887 0.053012383513456753 ;
createNode nurbsSurface -n "pose17Shape" -p "pose17";
	rename -uid "7FE25BF1-4DAB-BA13-8B6C-74B0579E815B";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose18" -p "poses";
	rename -uid "C2C50826-4F76-48AE-0294-BE92E068B830";
	setAttr ".t" -type "double3" -0.29481923714592101 0.72836197248920653 0.61852280025907658 ;
createNode nurbsSurface -n "pose18Shape" -p "pose18";
	rename -uid "09DAD972-457F-C016-008F-01A233920860";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose19" -p "poses";
	rename -uid "62726868-4077-D213-57C4-8997A20D763C";
	setAttr ".t" -type "double3" 0.98706270362554682 0.11468311370821323 0.11204910772342079 ;
createNode nurbsSurface -n "pose19Shape" -p "pose19";
	rename -uid "74188A84-46FB-0A00-9886-72A6638D7167";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose20" -p "poses";
	rename -uid "0BCDB3E9-49A5-9B74-86FA-05A3EEC9BFEF";
	setAttr ".t" -type "double3" 0.70856950520234108 -0.62723051552598985 0.32328182239388348 ;
createNode nurbsSurface -n "pose20Shape" -p "pose20";
	rename -uid "B64E44C6-4EED-D02D-B719-079A2D3C264E";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose21" -p "poses";
	rename -uid "A218E67A-485B-4B94-D5DD-CBB08C219380";
	setAttr ".t" -type "double3" -0.65034580621659077 -0.1938402925445388 0.73449048552227025 ;
createNode nurbsSurface -n "pose21Shape" -p "pose21";
	rename -uid "26113D9E-423D-7BDB-CDDE-87ABCB9073B3";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose22" -p "poses";
	rename -uid "38F73709-4CDD-A38E-351C-598FDE6E0AD2";
	setAttr ".t" -type "double3" 0.0068058161327845604 -0.36638622287992478 -0.93043797028633168 ;
createNode nurbsSurface -n "pose22Shape" -p "pose22";
	rename -uid "6399E896-480C-861C-3349-AEA24DDDAE12";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose23" -p "poses";
	rename -uid "FB6652AC-4193-BF3A-B821-E59A44F5FEAF";
	setAttr ".t" -type "double3" 0.4933232850076531 -0.79070266908274545 -0.36252093122284706 ;
createNode nurbsSurface -n "pose23Shape" -p "pose23";
	rename -uid "02D61CAA-472D-0E8B-714D-B88F6A706713";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose24" -p "poses";
	rename -uid "E1544BFE-4088-1537-B327-EA9A095305C5";
	setAttr ".t" -type "double3" 0.40632217221769334 -0.91089471203815131 -0.071924376571704696 ;
createNode nurbsSurface -n "pose24Shape" -p "pose24";
	rename -uid "B10AF232-4FDD-1FF1-5AD9-6FAEA6A89E9A";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose25" -p "poses";
	rename -uid "1C97B597-4714-8837-FB60-7CBC7B0CB240";
	setAttr ".t" -type "double3" -0.6263128302592641 -0.44653613129745573 0.63901308445017879 ;
createNode nurbsSurface -n "pose25Shape" -p "pose25";
	rename -uid "A9B85EB2-42D8-8861-6999-9BADA344F332";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose26" -p "poses";
	rename -uid "BFA5DEB6-446B-1E91-55C7-B2A43136408D";
	setAttr ".t" -type "double3" 0.41117537764917256 -0.081577097053283532 0.90789866507855344 ;
createNode nurbsSurface -n "pose26Shape" -p "pose26";
	rename -uid "61669C37-4AA1-C5E7-F91D-24BD4F0CB857";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose27" -p "poses";
	rename -uid "6B881E9E-4EF3-8AAD-DDD9-53BF152AF180";
	setAttr ".t" -type "double3" -0.95887331135215315 0.27804023562568403 0.043996904542479953 ;
createNode nurbsSurface -n "pose27Shape" -p "pose27";
	rename -uid "09B77C0E-479B-B790-9F15-77AD1B9333B8";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose28" -p "poses";
	rename -uid "302BEC4B-44B6-2610-9F06-6692AB7FF247";
	setAttr ".t" -type "double3" 0.5624423966840566 -0.70069556053904147 0.43895817779507529 ;
createNode nurbsSurface -n "pose28Shape" -p "pose28";
	rename -uid "8169226A-48C8-B3B9-4029-18A86AC527FE";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose29" -p "poses";
	rename -uid "6F75E5B7-4723-C2B3-7B3F-90A8AF2151F5";
	setAttr ".t" -type "double3" 0.19158733309181178 -0.59442776629886873 0.78099290934790477 ;
createNode nurbsSurface -n "pose29Shape" -p "pose29";
	rename -uid "727D4063-49A6-82B6-324D-B39CF44AEACB";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose30" -p "poses";
	rename -uid "ABD3182E-42A5-AAF3-FD95-4BB2AB7EEFCD";
	setAttr ".t" -type "double3" -0.45586335199193162 0.54302686572017678 -0.7042785136180808 ;
createNode nurbsSurface -n "pose30Shape" -p "pose30";
	rename -uid "C8C68988-4B59-18C1-663A-8EA30DBD8363";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose31" -p "poses";
	rename -uid "A43A7996-4F12-B9B7-C6E2-A28336A08FCC";
	setAttr ".t" -type "double3" 0.55524103657522661 0.68708384212751883 -0.4686397178965464 ;
createNode nurbsSurface -n "pose31Shape" -p "pose31";
	rename -uid "6F383749-4297-933A-E8AD-FB88C8069D00";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose32" -p "poses";
	rename -uid "99D4069D-484E-CCF1-F9B4-1DA38DA8063B";
	setAttr ".t" -type "double3" 0.72758606929714054 0.57769752687748921 0.36997848478576334 ;
createNode nurbsSurface -n "pose32Shape" -p "pose32";
	rename -uid "8A990C5B-4BB0-7E47-AA18-B3A67B17ED8F";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose33" -p "poses";
	rename -uid "AF9D2440-4587-225E-8228-6C931BF5C9BD";
	setAttr ".t" -type "double3" 0.087004385689344002 -0.7075468414631908 -0.70129002845205368 ;
createNode nurbsSurface -n "pose33Shape" -p "pose33";
	rename -uid "23C4E7E4-40A4-CF08-757E-20AC58CEB440";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose34" -p "poses";
	rename -uid "1AE32C5C-41B9-E656-FA95-498752A96873";
	setAttr ".t" -type "double3" -0.74963694459448804 0.64929580254621444 0.1282942403029376 ;
createNode nurbsSurface -n "pose34Shape" -p "pose34";
	rename -uid "DB4648D5-4A37-2D2B-4D8A-D291EBECBE53";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose35" -p "poses";
	rename -uid "9739FF3A-4F1D-6CD2-9C50-96886F175B34";
	setAttr ".t" -type "double3" 0.070681426359613567 0.13217917272336616 0.9887025853440139 ;
createNode nurbsSurface -n "pose35Shape" -p "pose35";
	rename -uid "9004381D-422A-99B1-A245-20865998C1F6";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose36" -p "poses";
	rename -uid "FC94FF37-4D15-FB78-EAEC-A59769396223";
	setAttr ".t" -type "double3" 0.66109304469175745 0.30280404235806585 0.6864879446806017 ;
createNode nurbsSurface -n "pose36Shape" -p "pose36";
	rename -uid "19E66C1A-4879-AFF4-8923-F1810C59324F";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose37" -p "poses";
	rename -uid "118283F9-47AE-7935-F0D5-E3A897500E36";
	setAttr ".t" -type "double3" 0.084549049839154941 0.57975378320253279 0.81039312005572128 ;
createNode nurbsSurface -n "pose37Shape" -p "pose37";
	rename -uid "9B0CCE4E-47F6-28E4-96A6-92A9288B25E4";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose38" -p "poses";
	rename -uid "DECC2A8B-4B71-EF08-177A-8D813125D493";
	setAttr ".t" -type "double3" 0.4713246688670098 0.33635247790404427 -0.81530366559044309 ;
createNode nurbsSurface -n "pose38Shape" -p "pose38";
	rename -uid "0FB8BE56-44D0-F7D9-38A3-CDB7E21E9A78";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose39" -p "poses";
	rename -uid "9E371A14-4E2B-9746-92E0-508BCC382CD7";
	setAttr ".t" -type "double3" 0.42172292360880237 -0.49222216860548107 -0.7600759110153934 ;
createNode nurbsSurface -n "pose39Shape" -p "pose39";
	rename -uid "FC9B25B2-4950-FBB9-D54E-4B9B7B1AD63A";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose40" -p "poses";
	rename -uid "F2B3E8EA-4891-E553-9976-4BAD383440CC";
	setAttr ".t" -type "double3" -0.57931394945721326 -0.60919670898227207 -0.54154844448992201 ;
createNode nurbsSurface -n "pose40Shape" -p "pose40";
	rename -uid "4CE81217-453D-0429-AEED-4B93CCCE5DFF";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose41" -p "poses";
	rename -uid "D980C456-496B-DAE8-D1B0-158B5BBE0203";
	setAttr ".t" -type "double3" 0.050258559779704115 0.94683451176012179 -0.31110578507889031 ;
createNode nurbsSurface -n "pose41Shape" -p "pose41";
	rename -uid "DD17CA94-472A-9BDE-0EED-76891880B18E";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose42" -p "poses";
	rename -uid "0E4766D8-4352-AA90-7ED7-139D6F75F874";
	setAttr ".t" -type "double3" 0.92380475383633287 -0.37144692844486993 -0.08377489642363542 ;
createNode nurbsSurface -n "pose42Shape" -p "pose42";
	rename -uid "D10DF635-4170-AD1F-42BE-E5B65AECDAC3";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose43" -p "poses";
	rename -uid "627E61F9-4DD6-2368-2ECD-388C9035BFDD";
	setAttr ".t" -type "double3" 0.27943076370170922 0.85745786508136401 0.42740606874310494 ;
createNode nurbsSurface -n "pose43Shape" -p "pose43";
	rename -uid "B08BCC29-461B-E010-B170-F4A653853FAC";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose44" -p "poses";
	rename -uid "4A1F2ADC-46DE-405B-1CE1-058EBA6BF752";
	setAttr ".t" -type "double3" -0.18864632934819769 -0.83988966976092905 0.50511840565824162 ;
createNode nurbsSurface -n "pose44Shape" -p "pose44";
	rename -uid "60A64489-454C-0201-D89A-12BFCF641EB1";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose45" -p "poses";
	rename -uid "DDA5FC3E-4808-1354-6087-D6B8DF952D42";
	setAttr ".t" -type "double3" -0.53412949600668924 -0.82569056099337512 0.18149594756381127 ;
createNode nurbsSurface -n "pose45Shape" -p "pose45";
	rename -uid "69A978C9-4C41-10B8-AC16-B18171459CFB";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose46" -p "poses";
	rename -uid "6C3564E2-4616-C2DC-4750-A6BC8D7950FC";
	setAttr ".t" -type "double3" 0.7978665835584261 0.24529459457961766 0.55067184121836676 ;
createNode nurbsSurface -n "pose46Shape" -p "pose46";
	rename -uid "E5E56518-407A-D8B7-452C-88BE47A5AED6";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose47" -p "poses";
	rename -uid "DF9F3653-4E35-4EBD-AA69-7DB6FDC97228";
	setAttr ".t" -type "double3" -0.45339335800200525 -0.76119173505020754 -0.46370422190327321 ;
createNode nurbsSurface -n "pose47Shape" -p "pose47";
	rename -uid "CCF22DAC-436A-48DC-D326-1EB1AECA8D25";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose48" -p "poses";
	rename -uid "60D9930B-4C13-A943-F6F9-4C8FDF81771F";
	setAttr ".t" -type "double3" -0.63172174882815202 -0.3615131638755279 -0.68573746025881288 ;
createNode nurbsSurface -n "pose48Shape" -p "pose48";
	rename -uid "3B484C42-4F84-9B23-C65F-77BD3426A94A";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose49" -p "poses";
	rename -uid "DFA2308E-4128-7AD1-ECB6-8B9AB977A027";
	setAttr ".t" -type "double3" -0.80415263521138891 -0.44777483843046473 -0.38741751046529116 ;
createNode nurbsSurface -n "pose49Shape" -p "pose49";
	rename -uid "4DBE9A7B-424F-5656-F2FA-24AD87F8CE1F";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "pose50" -p "poses";
	rename -uid "84713D09-4749-C469-1E1E-36990E17C75A";
	setAttr ".t" -type "double3" -0.47702810515641347 0.86351153072137488 -0.16368269060016583 ;
createNode nurbsSurface -n "pose50Shape" -p "pose50";
	rename -uid "A61867A8-42B2-5AEE-E033-9B8C11F9B3BA";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 9.5964746819769487e-018 -7.8598543388568475e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.050000000000000003 -0.014136251847345181 -8.8196237260076083e-018
		-0.050000000000000003 -0.0099958395418186397 0.0099958395418186276
		-0.050000000000000003 -5.9212031702453714e-018 0.014136251847345179
		-0.050000000000000003 0.0099958395418186276 0.0099958395418186345
		-0.050000000000000003 0.014136251847345181 6.1926660492906577e-018
		-0.050000000000000003 0.0099958395418186467 -0.009995839541818631
		-0.050000000000000003 4.8897295815728335e-020 -0.014136251847345184
		-0.050000000000000003 -0.0099958395418186328 -0.0099958395418186397
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		-0.039180581244561218 -0.043588181876590165 -1.2350559912432997e-017
		-0.039180581244561218 -0.030821498984529478 0.030821498984529457
		-0.039180581244561218 -1.0454646495845655e-017 0.043588181876590165
		-0.039180581244561218 0.03082149898452945 0.030821498984529471
		-0.039180581244561218 0.043588181876590165 1.833285546870408e-017
		-0.039180581244561218 0.030821498984529502 -0.030821498984529454
		-0.039180581244561218 -7.6522137421939308e-018 -0.043588181876590165
		-0.039180581244561218 -0.030821498984529468 -0.030821498984529471
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		6.1265372767330888e-019 -0.061320473128284016 -1.0259546881590935e-017
		-2.0423880261598599e-018 -0.043360122374577093 0.043360122374577086
		-3.1421423292644077e-018 -1.0967463177287157e-017 0.06132047312828403
		-2.0423880261598603e-018 0.043360122374577065 0.043360122374577093
		6.1265372767330667e-019 0.061320473128284016 2.5425753623286322e-017
		3.2676954815064748e-018 0.043360122374577127 -0.043360122374577065
		4.3674497846110229e-018 -1.450552488649394e-017 -0.061320473128284016
		3.2676954815064763e-018 -0.043360122374577093 -0.043360122374577086
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.039180581244561224 -0.043588181876590172 -2.2349438396546818e-018
		0.039180581244561224 -0.030821498984529485 0.030821498984529478
		0.039180581244561224 -5.1372677640558092e-018 0.043588181876590179
		0.039180581244561224 0.030821498984529468 0.030821498984529482
		0.039180581244561224 0.043588181876590172 1.7813714077902713e-017
		0.039180581244561224 0.030821498984529502 -0.030821498984529464
		0.039180581244561224 -1.2969592473983781e-017 -0.043588181876590172
		0.039180581244561224 -0.030821498984529485 -0.030821498984529471
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.049999999999999996 -0.014136251847345186 4.0893425928400704e-018
		0.049999999999999996 -0.009995839541818638 0.0099958395418186449
		0.049999999999999996 8.6452915286554267e-019 0.014136251847345193
		0.049999999999999996 0.009995839541818638 0.0099958395418186415
		0.049999999999999996 0.014136251847345186 5.5301677219165117e-018
		0.049999999999999996 0.0099958395418186449 -0.0099958395418186345
		0.049999999999999996 -6.7368350272951868e-018 -0.014136251847345183
		0.049999999999999996 -0.0099958395418186449 -0.0099958395418186328
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		0.050000000000000003 3.9015993421932211e-018 -5.6382196853133023e-018
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode transform -n "output_color";
	rename -uid "23EF173A-40D0-324B-F008-588D6F675D24";
	setAttr ".t" -type "double3" 1.4764693472124044 0.38285879074688656 -0.84547011402467409 ;
createNode nurbsSurface -n "output_colorShape" -p "output_color";
	rename -uid "ED423BE9-4037-64CE-2D40-699BE20202B4";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		-2.2062493594640584e-016 -0.25433066102787366 -4.9225994643753615e-017
		0.050844969563985536 -0.25433066102787366 -0.050844969563985903
		0.07190564553583581 -0.25433066102787366 -6.6116128701045942e-019
		0.05084496956398557 -0.25433066102787366 0.050844969563985778
		-2.1574296029303845e-016 -0.25433066102787366 0.071905645535836005
		-0.050844969563986028 -0.25433066102787366 0.050844969563985841
		-0.071905645535836227 -0.25433066102787366 2.9706430671712308e-017
		-0.050844969563986084 -0.25433066102787366 -0.050844969563985827
		-2.9210467193491034e-016 -0.25433066102787366 -0.071905645535836032
		0.050844969563985536 -0.25433066102787366 -0.050844969563985903
		0.07190564553583581 -0.25433066102787366 -6.6116128701045942e-019
		0.05084496956398557 -0.25433066102787366 0.050844969563985778
		0.15677704421210598 -0.19929646254771133 -0.15677704421210664
		0.22171622219352702 -0.19929646254771133 4.1881284682529146e-017
		0.15677704421210611 -0.19929646254771133 0.15677704421210625
		-1.9441258085560366e-016 -0.19929646254771133 0.2217162221935271
		-0.15677704421210659 -0.19929646254771133 0.15677704421210631
		-0.22171622219352743 -0.19929646254771133 5.6136176176977275e-017
		-0.15677704421210659 -0.19929646254771133 -0.15677704421210642
		-3.5048724718515206e-016 -0.19929646254771133 -0.2217162221935273
		0.15677704421210598 -0.19929646254771133 -0.15677704421210664
		0.22171622219352702 -0.19929646254771133 4.1881284682529146e-017
		0.15677704421210611 -0.19929646254771133 0.15677704421210625
		0.22055617171551337 1.6621503036986776e-017 -0.22055617171551409
		0.31191352930516847 3.1163325508068644e-018 8.8944816500741687e-017
		0.22055617171551345 -1.0388837935373032e-017 0.22055617171551367
		-1.9284536663562071e-016 -1.5982862712909591e-017 0.31191352930516858
		-0.22055617171551395 -1.0388837935373032e-017 0.22055617171551367
		-0.31191352930516897 3.1163325508068655e-018 7.0948065035542278e-017
		-0.22055617171551398 1.6621503036986764e-017 -0.22055617171551375
		-3.7436268796329549e-016 2.2215527814523319e-017 -0.31191352930516875
		0.22055617171551337 1.6621503036986776e-017 -0.22055617171551409
		0.31191352930516847 3.1163325508068644e-018 8.8944816500741687e-017
		0.22055617171551345 -1.0388837935373032e-017 0.22055617171551367
		0.15677704421210611 0.19929646254771138 -0.15677704421210664
		0.22171622219352705 0.19929646254771138 9.3335511132407006e-017
		0.15677704421210617 0.19929646254771138 0.15677704421210636
		-2.2146002981143717e-016 0.19929646254771138 0.22171622219352713
		-0.15677704421210659 0.19929646254771138 0.15677704421210636
		-0.22171622219352752 0.19929646254771138 5.3495504715188428e-017
		-0.15677704421210664 0.19929646254771138 -0.15677704421210648
		-3.2343979822931879e-016 0.19929646254771138 -0.22171622219352735
		0.15677704421210611 0.19929646254771138 -0.15677704421210664
		0.22171622219352705 0.19929646254771138 9.3335511132407006e-017
		0.15677704421210617 0.19929646254771138 0.15677704421210636
		0.050844969563985584 0.25433066102787366 -0.050844969563985883
		0.071905645535835824 0.25433066102787366 6.5001757454171311e-017
		0.05084496956398557 0.25433066102787366 0.050844969563985896
		-2.5025935603893855e-016 0.25433066102787366 0.071905645535836046
		-0.050844969563986098 0.25433066102787366 0.050844969563985883
		-0.071905645535836241 0.25433066102787366 2.6336557921093758e-017
		-0.050844969563986077 0.25433066102787366 -0.050844969563985848
		-2.5758827618901013e-016 0.25433066102787366 -0.071905645535836032
		0.050844969563985584 0.25433066102787366 -0.050844969563985883
		0.071905645535835824 0.25433066102787366 6.5001757454171311e-017
		0.05084496956398557 0.25433066102787366 0.050844969563985896
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		-2.0077900915108749e-016 0.25433066102787366 1.0888156544298531e-017
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
	setAttr ".qdGuid" -type "string" "0284e906-7a0a-4cae-a13a-762b3dcef633";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "F2A0E1BC-4217-EB21-739F-87BB448A198B";
	setAttr -s 54 ".lnk";
	setAttr -s 54 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "65CB6384-4620-D5F1-C07B-F5A4433C2F86";
createNode displayLayer -n "defaultLayer";
	rename -uid "6CCCF341-482D-D3F0-0D25-60827270F4DD";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "408B9DA2-449F-610B-BA38-778E8E978A26";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "C1B8AE12-4755-99CC-7753-009483EB82EF";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "60564B69-4854-98BA-7E07-21BDF0225499";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                -pluginObjects \"AtgiLocatorNode\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n"
		+ "            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n"
		+ "            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"AtgiLocatorNode\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n"
		+ "                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n"
		+ "                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                -pluginObjects \"AtgiLocatorNode\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n"
		+ "            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n"
		+ "            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"AtgiLocatorNode\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n"
		+ "                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n"
		+ "                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n"
		+ "                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                -pluginObjects \"AtgiLocatorNode\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n"
		+ "            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"AtgiLocatorNode\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n"
		+ "                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 0\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n"
		+ "                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n"
		+ "                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "                -pluginObjects \"AtgiLocatorNode\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 0\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n"
		+ "            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n"
		+ "            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"AtgiLocatorNode\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n"
		+ "                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n"
		+ "            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n"
		+ "            -ignoreHiddenAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n"
		+ "                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n"
		+ "                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n"
		+ "                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n"
		+ "                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n"
		+ "                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n"
		+ "                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n"
		+ "                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range -1 -1 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n"
		+ "                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range -1 -1 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n"
		+ "\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n"
		+ "\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n"
		+ "                -extendToShapes 1\n                $editorName;\n\t\t\tif (`objExists nodeEditorPanel1Info`) nodeEditor -e -restoreInfo nodeEditorPanel1Info $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;\n\t\t\tif (`objExists nodeEditorPanel1Info`) nodeEditor -e -restoreInfo nodeEditorPanel1Info $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Texture Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n"
		+ "        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"right3\\\" -ps 1 26 100 -ps 2 74 100 -ps 3 74 0 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 0\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    -pluginObjects \\\"AtgiLocatorNode\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 0\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    -pluginObjects \\\"AtgiLocatorNode\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Hypershade\")) \n\t\t\t\t\t\"scriptedPanel\"\n\t\t\t\t\t\"$panelName = `scriptedPanel -unParent  -type \\\"hyperShadePanel\\\" -l (localizedPanelLabel(\\\"Hypershade\\\")) -mbv $menusOkayInPanels `\"\n\t\t\t\t\t\"scriptedPanel -edit -l (localizedPanelLabel(\\\"Hypershade\\\")) -mbv $menusOkayInPanels  $panelName\"\n\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "A15F623D-4381-CD3A-4840-0FA2D244006B";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 30 -ast 1 -aet 60 ";
	setAttr ".st" 6;
createNode surfaceShader -n "outShader";
	rename -uid "E7648804-490E-79BF-4541-AEBE3E43D7CE";
createNode shadingEngine -n "surfaceShader1SG";
	rename -uid "EAFFFAC8-47DC-21E4-2D75-7DA38B044AD9";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo1";
	rename -uid "65F738AA-43D3-BC54-66CE-DA85F2026BB6";
createNode surfaceShader -n "sp_shader1";
	rename -uid "5CE32E22-48CD-F8B7-9B29-47A452B17FF3";
	setAttr ".oc" -type "float3" 0.4400759 0.38035494 0.51820427 ;
createNode shadingEngine -n "sp_shader1SG";
	rename -uid "B00261AB-4ADB-8CA0-4688-E58D4F4A3C37";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo2";
	rename -uid "87627F93-429B-A282-E380-52B36378DBB4";
createNode surfaceShader -n "sp_shader2";
	rename -uid "738017A4-459A-5079-6833-89A0F354C389";
	setAttr ".oc" -type "float3" 0.78521395 0.12909374 0.87687892 ;
createNode shadingEngine -n "sp_shader2SG";
	rename -uid "0D6B69BD-4A24-258B-F8F2-1084DF88F6AD";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo3";
	rename -uid "D9F0411D-4880-4B32-D281-03ADCD157282";
createNode surfaceShader -n "sp_shader3";
	rename -uid "89D17BF8-4DF3-DF07-7BE8-CF8AFEC6B22B";
	setAttr ".oc" -type "float3" 0.62065887 0.83697164 0.75633037 ;
createNode shadingEngine -n "sp_shader3SG";
	rename -uid "0585AC98-4C39-9B7F-FF5F-02B5A4A2516F";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo4";
	rename -uid "44BA1AF3-48E1-8205-6E5B-9F8BE7B079C7";
createNode surfaceShader -n "sp_shader4";
	rename -uid "C428D2E2-4E3C-A1F5-A5F0-A58C1E13AC8D";
	setAttr ".oc" -type "float3" 0.6488601 0.81278455 0.93044728 ;
createNode shadingEngine -n "sp_shader4SG";
	rename -uid "16420293-487B-EDDD-B9B8-CE9E0E9DB7C5";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo5";
	rename -uid "5C9DE4A9-49E4-A088-8AED-979EE815CE83";
createNode surfaceShader -n "sp_shader5";
	rename -uid "1AFF623D-4407-D935-59E7-4EB4E3605D6B";
	setAttr ".oc" -type "float3" 0.48086238 0.064664751 0.1673658 ;
createNode shadingEngine -n "sp_shader5SG";
	rename -uid "3F57D899-4645-B598-8851-7EA4CD3662A2";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo6";
	rename -uid "EE03DB0A-47E5-B6CA-DFC7-208A5FF5E3A0";
createNode surfaceShader -n "sp_shader6";
	rename -uid "BEF0E113-4C83-0522-1D25-8991BC83DDDE";
	setAttr ".oc" -type "float3" 0.95209736 0.10421081 0.29202747 ;
createNode shadingEngine -n "sp_shader6SG";
	rename -uid "111357CE-459A-0621-3CD2-78B02DF34FD8";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo7";
	rename -uid "740089CF-4E41-B488-911A-EDB3775DDFD5";
createNode surfaceShader -n "sp_shader7";
	rename -uid "3F52E2E6-4D38-B15B-0643-53A31706FAB3";
	setAttr ".oc" -type "float3" 0.52998793 0.79562187 0.17601284 ;
createNode shadingEngine -n "sp_shader7SG";
	rename -uid "DD7380D9-423B-2777-B54E-05AE680F81C5";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo8";
	rename -uid "6DC01EDE-4756-8F31-AA73-6E8EB5D6165F";
createNode surfaceShader -n "sp_shader8";
	rename -uid "27FEE976-48B5-B6C3-838E-FBA7A4570B58";
	setAttr ".oc" -type "float3" 0.81115448 0.11208478 0.29400402 ;
createNode shadingEngine -n "sp_shader8SG";
	rename -uid "2C55ACAA-45BA-0655-FD37-07AB0EE98506";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo9";
	rename -uid "F88678CB-4DE6-528D-E3A8-319D837C462A";
createNode surfaceShader -n "sp_shader9";
	rename -uid "C5F65A6C-42D7-EE89-3355-2AA799F6D0B6";
	setAttr ".oc" -type "float3" 0.12179035 0.40219721 0.4365198 ;
createNode shadingEngine -n "sp_shader9SG";
	rename -uid "0280CBBD-4ED0-36B1-0B58-2096CFE40EBC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo10";
	rename -uid "3902D3F0-49B8-EBE2-6C0B-D1B087E14FF5";
createNode surfaceShader -n "sp_shader10";
	rename -uid "BF6E0097-4488-013B-9E66-D58121380C3B";
	setAttr ".oc" -type "float3" 0.10891694 0.18788576 0.08459501 ;
createNode shadingEngine -n "sp_shader10SG";
	rename -uid "C04E37F6-4F03-B150-7D7E-B2819A27E549";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo11";
	rename -uid "FA6EA690-4247-634E-6547-879031A682F8";
createNode surfaceShader -n "sp_shader11";
	rename -uid "743A5483-40E6-6BA8-2F9F-06B00FC8F9E3";
	setAttr ".oc" -type "float3" 0.40164715 0.2080584 0.89789367 ;
createNode shadingEngine -n "sp_shader11SG";
	rename -uid "DA8A06B6-4FBB-4939-6D63-FEA8C8A74CC5";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo12";
	rename -uid "8D48B01A-4FEF-6A04-33E0-D581BF5E00E1";
createNode surfaceShader -n "sp_shader12";
	rename -uid "600FF70B-4486-E1C1-088D-22A9ED376C54";
	setAttr ".oc" -type "float3" 0.64966387 0.8430351 0.47709867 ;
createNode shadingEngine -n "sp_shader12SG";
	rename -uid "895A6FC3-4F01-8795-0C45-D4816D28B606";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo13";
	rename -uid "9C944EE7-4857-786C-BC4C-2AB03B485797";
createNode surfaceShader -n "sp_shader13";
	rename -uid "17F9A2BE-4114-E77B-988B-F1924747D62D";
	setAttr ".oc" -type "float3" 0.51827395 0.44288713 0.42753452 ;
createNode shadingEngine -n "sp_shader13SG";
	rename -uid "419EC6D4-4915-8852-20B9-1C837F22B023";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo14";
	rename -uid "89104AC5-4C88-015D-9367-CC96FD6FB27D";
createNode surfaceShader -n "sp_shader14";
	rename -uid "9EF41A98-4DAE-6DDC-EEE1-E99D9A5E7E0D";
	setAttr ".oc" -type "float3" 0.84260905 0.78155756 0.046895072 ;
createNode shadingEngine -n "sp_shader14SG";
	rename -uid "1FD3BE1A-4B47-FCDC-A1DD-39B80BF42F7B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo15";
	rename -uid "65670948-46B7-1FB4-FD69-119A0078276B";
createNode surfaceShader -n "sp_shader15";
	rename -uid "072997CF-4009-F335-87A5-14A73A6A78C8";
	setAttr ".oc" -type "float3" 0.48242217 0.18989635 0.20450859 ;
createNode shadingEngine -n "sp_shader15SG";
	rename -uid "9A32580B-444E-94FF-47C2-3FBC185EDAB3";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo16";
	rename -uid "E62FD400-45F4-FEC9-1C35-D2A9EECCEE66";
createNode surfaceShader -n "sp_shader16";
	rename -uid "E0C7C33F-4275-C923-559F-DA85AA756442";
	setAttr ".oc" -type "float3" 0.88999999 0.88999999 0.88999999 ;
createNode shadingEngine -n "sp_shader16SG";
	rename -uid "02986B47-4478-1DD1-732B-CC8FA21A4061";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo17";
	rename -uid "60B66675-4810-8EC6-E893-80988C7473F5";
createNode surfaceShader -n "sp_shader17";
	rename -uid "030349B7-40BA-AF28-688F-69A5015CF21C";
	setAttr ".oc" -type "float3" 0.71431851 0.8200767 0.7884537 ;
createNode shadingEngine -n "sp_shader17SG";
	rename -uid "D54BAAE9-403E-A350-7022-42998044405E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo18";
	rename -uid "DE7E6EF2-4003-785D-FC27-739BB7D65A8F";
createNode surfaceShader -n "sp_shader18";
	rename -uid "3180B451-4A69-B970-7EE0-EB9601BD199D";
	setAttr ".oc" -type "float3" 0.58346057 0.71509695 0.41887093 ;
createNode shadingEngine -n "sp_shader18SG";
	rename -uid "3E0BA3BE-4EFA-4C81-F2DE-BC8F64C636FA";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo19";
	rename -uid "1660C537-4613-634D-8E83-2A911B4AC86D";
createNode surfaceShader -n "sp_shader19";
	rename -uid "9C0AA57E-41C4-4C43-A71D-72A80AF24E6C";
	setAttr ".oc" -type "float3" 0 1 0 ;
createNode shadingEngine -n "sp_shader19SG";
	rename -uid "E56DBCA9-44FB-E65D-DB7F-DB9E0EAF7B13";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo20";
	rename -uid "633F7A77-4DA4-BD5B-EFF3-69AEF72EEE5F";
createNode surfaceShader -n "sp_shader20";
	rename -uid "ACC3CBAC-408D-5BAD-4198-5B89A7A2623C";
	setAttr ".oc" -type "float3" 0.10043967 0.4039551 0.40237793 ;
createNode shadingEngine -n "sp_shader20SG";
	rename -uid "3649A752-4AC2-59CB-67B0-0FB928A9F19A";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo21";
	rename -uid "15C3E1CA-45DC-3560-6882-93B1BCBF8916";
createNode surfaceShader -n "sp_shader21";
	rename -uid "227B526F-4897-0175-CE2F-8C92BF0282E4";
	setAttr ".oc" -type "float3" 0.68108994 0.0043318141 0.77759004 ;
createNode shadingEngine -n "sp_shader21SG";
	rename -uid "49712A44-447F-126D-901E-829AC898C092";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo22";
	rename -uid "F9C031E9-4A2B-AECF-6555-C0993983B2E3";
createNode surfaceShader -n "sp_shader22";
	rename -uid "5E41A7C9-49D4-3B48-2C00-FD9282E7D165";
	setAttr ".oc" -type "float3" 1 1 1 ;
createNode shadingEngine -n "sp_shader22SG";
	rename -uid "14DA7AE1-4FED-C517-C8F4-C7AB48CD83A3";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo23";
	rename -uid "CDC5D7F4-44EB-20E3-416F-0A9063E2A361";
createNode surfaceShader -n "sp_shader23";
	rename -uid "CDCABC6B-440B-B5DB-D0AB-69A6B07C8F59";
	setAttr ".oc" -type "float3" 0.32635489 0.61733103 0.010202581 ;
createNode shadingEngine -n "sp_shader23SG";
	rename -uid "6FA1DFF4-4B74-475D-4DA6-F4BBC34361CC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo24";
	rename -uid "525DF563-4622-0E17-2593-6F9ABC093C66";
createNode surfaceShader -n "sp_shader24";
	rename -uid "6D11A47B-4907-59A9-9974-C382306FC75A";
	setAttr ".oc" -type "float3" 0.89956909 0.8298099 0.15488137 ;
createNode shadingEngine -n "sp_shader24SG";
	rename -uid "F7EB9BAD-43D2-42D9-03EB-189E19994472";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo25";
	rename -uid "2F62CC89-4AA3-8B73-B147-F59489C781BE";
createNode surfaceShader -n "sp_shader25";
	rename -uid "6330E8AA-4915-285F-D3BB-42ACBED0CE10";
	setAttr ".oc" -type "float3" 0.56525755 0.22210982 0.85496438 ;
createNode shadingEngine -n "sp_shader25SG";
	rename -uid "71EDF83A-4118-F053-21FD-75A33B62B1D9";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo26";
	rename -uid "4882EAD2-4E02-F88D-5786-859733C63653";
createNode surfaceShader -n "sp_shader26";
	rename -uid "3F53D873-4C1B-ABDE-FF7C-A5930EFC6725";
	setAttr ".oc" -type "float3" 0.035999998 0.28 1 ;
createNode shadingEngine -n "sp_shader26SG";
	rename -uid "9385DBEA-4C06-937A-2F42-66AD45DA4B75";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo27";
	rename -uid "745DEB3E-48C6-7400-EE9E-6BB1E0A884A9";
createNode surfaceShader -n "sp_shader27";
	rename -uid "9904A0D3-44EC-B86B-AF03-52B7073D5D12";
	setAttr ".oc" -type "float3" 0.33873066 0.016086558 0.69875497 ;
createNode shadingEngine -n "sp_shader27SG";
	rename -uid "0E1EE8FC-4E39-4ACA-FC73-FD985553C241";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo28";
	rename -uid "BC9D1B3E-4481-F87A-BCD2-D5A2CC948771";
createNode surfaceShader -n "sp_shader28";
	rename -uid "A5A46B8C-4032-E8AC-F654-5C8882BDAAA6";
	setAttr ".oc" -type "float3" 0.050614137 0.18599968 0.13865262 ;
createNode shadingEngine -n "sp_shader28SG";
	rename -uid "8154B40C-48E5-364C-FBF6-37A0BC773519";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo29";
	rename -uid "7DD5E73F-439C-4204-4981-1194E512B30D";
createNode surfaceShader -n "sp_shader29";
	rename -uid "ED7568AE-49EB-33E5-99B0-84BF9FE01357";
	setAttr ".oc" -type "float3" 0.69236839 0.47139713 0.70029259 ;
createNode shadingEngine -n "sp_shader29SG";
	rename -uid "FDD34C4E-4286-EF1B-81D0-9CA6BD067B95";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo30";
	rename -uid "9707E929-4719-813C-AB61-BCA12EC0D124";
createNode surfaceShader -n "sp_shader30";
	rename -uid "8F2572A8-4BE8-A5AA-1649-06AB087EBA54";
	setAttr ".oc" -type "float3" 0.33772039 0.89582098 0.28660861 ;
createNode shadingEngine -n "sp_shader30SG";
	rename -uid "039833AB-4B31-D9B7-9E38-5C866D06C1D6";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo31";
	rename -uid "44571B08-4505-E8AA-838F-C4BE8158750B";
createNode surfaceShader -n "sp_shader31";
	rename -uid "C9140EE1-4867-D788-37D9-978659AF27AD";
	setAttr ".oc" -type "float3" 0.40673137 0.62870234 0.41522437 ;
createNode shadingEngine -n "sp_shader31SG";
	rename -uid "74AAC595-457F-CE89-022F-36AC56400F0E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo32";
	rename -uid "7E1CA713-40DF-4D7C-8D44-438957B58E04";
createNode surfaceShader -n "sp_shader32";
	rename -uid "25CA331E-48BE-0C87-E3FB-1F92D75CA493";
	setAttr ".oc" -type "float3" 1 0.419 0 ;
createNode shadingEngine -n "sp_shader32SG";
	rename -uid "714D2AE4-467B-25A1-77A0-0894038BE96E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo33";
	rename -uid "B43CC425-40F8-0831-ABA4-1D8FB8B98A4B";
createNode surfaceShader -n "sp_shader33";
	rename -uid "C9D0E98C-4F2E-7BCA-1B15-419EC46D5034";
	setAttr ".oc" -type "float3" 0.81957442 0.83366925 0.92934912 ;
createNode shadingEngine -n "sp_shader33SG";
	rename -uid "E8E9D477-44F0-1E2E-A1CD-2DB6ACFA6229";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo34";
	rename -uid "BD881A85-47A9-C486-4455-18B168B4FF1B";
createNode surfaceShader -n "sp_shader34";
	rename -uid "305835BE-4B03-50DB-6880-8CADE0086261";
	setAttr ".oc" -type "float3" 0.77174628 0.75592685 0.69826281 ;
createNode shadingEngine -n "sp_shader34SG";
	rename -uid "F1794785-4EB2-54E6-7249-9A9455A70ED5";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo35";
	rename -uid "271838C0-4DC9-121F-B24B-8BAB1973E688";
createNode surfaceShader -n "sp_shader35";
	rename -uid "13BEA7C3-4251-1761-9DC0-56A85691C7A4";
	setAttr ".oc" -type "float3" 0.90294892 0.95365 0.071001731 ;
createNode shadingEngine -n "sp_shader35SG";
	rename -uid "10217BD6-42F1-C0CC-6EAD-7CBAC2F6EEAC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo36";
	rename -uid "E807DC9C-4B18-DB08-8BD8-9E8487516944";
createNode surfaceShader -n "sp_shader36";
	rename -uid "4A110293-4708-E75A-D269-7282CE10D911";
	setAttr ".oc" -type "float3" 0.72213197 0.01014102 0.78118932 ;
createNode shadingEngine -n "sp_shader36SG";
	rename -uid "56C07C40-4909-B56F-8C14-A9896DFB62D6";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo37";
	rename -uid "0B854C36-411E-C07F-F9F2-4986A3DC340A";
createNode surfaceShader -n "sp_shader37";
	rename -uid "1A00A43E-4E11-9279-B269-70A7B88C6245";
	setAttr ".oc" -type "float3" 0.16234653 0.79509085 0.19253328 ;
createNode shadingEngine -n "sp_shader37SG";
	rename -uid "58CC4D97-4198-45A2-5300-C0BF3B9E4486";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo38";
	rename -uid "21F3E3C1-4501-360E-46BC-80BADF4C50E7";
createNode surfaceShader -n "sp_shader38";
	rename -uid "B662D306-4508-8E75-06EC-4E94E5414C83";
	setAttr ".oc" -type "float3" 0.57880932 0.52092558 0.25550014 ;
createNode shadingEngine -n "sp_shader38SG";
	rename -uid "71AA7953-4421-7531-F8B6-038ABA698B2A";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo39";
	rename -uid "C749743E-4144-5EB2-ED56-0994A13EFDFF";
createNode surfaceShader -n "sp_shader39";
	rename -uid "3DE3205A-45EA-CACA-5125-909B24073F58";
	setAttr ".oc" -type "float3" 0.22591576 0.83178043 0.86628526 ;
createNode shadingEngine -n "sp_shader39SG";
	rename -uid "91D0A3B2-4452-A5E8-CA59-AEA2F2FF6570";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo40";
	rename -uid "B6F838C4-4230-2A5F-A8EC-33B45ABC6C70";
createNode surfaceShader -n "sp_shader40";
	rename -uid "222DB367-49CB-9F49-9780-DA835CEA6E1B";
	setAttr ".oc" -type "float3" 0.036405306 0.91733956 0.82625091 ;
createNode shadingEngine -n "sp_shader40SG";
	rename -uid "BB31D2F3-49EC-5D9B-0A3A-398D51C0E00E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo41";
	rename -uid "7AEB34F2-480B-7BE7-0403-AEA9EBB377D4";
createNode surfaceShader -n "sp_shader41";
	rename -uid "1D80B3FD-4639-0743-9716-A6AB702BBC9F";
	setAttr ".oc" -type "float3" 0.12580563 0.15725113 0.77560848 ;
createNode shadingEngine -n "sp_shader41SG";
	rename -uid "5982BF1A-4D40-1E95-98C0-12B35D9F087B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo42";
	rename -uid "B16FA45D-45FC-5BD9-ABFF-6FABBA0F4729";
createNode surfaceShader -n "sp_shader42";
	rename -uid "6C6EA191-46AE-747F-C666-F89974A5C4CF";
	setAttr ".oc" -type "float3" 1 0 0 ;
createNode shadingEngine -n "sp_shader42SG";
	rename -uid "1FED96DE-442E-E942-3F4D-8097579C64AB";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo43";
	rename -uid "F45C6FE9-4F7E-3A46-AD9C-AA870BA5D204";
createNode surfaceShader -n "sp_shader43";
	rename -uid "304AAC8D-4578-F10A-0DFA-85AF73AEFCB6";
	setAttr ".oc" -type "float3" 0.19956511 0.3722865 0.45298991 ;
createNode shadingEngine -n "sp_shader43SG";
	rename -uid "E48D8D87-4BFC-54E6-54AF-C78D7AFA7CE1";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo44";
	rename -uid "34ED2E49-4DCB-7707-4FF3-EE8153467249";
createNode surfaceShader -n "sp_shader44";
	rename -uid "064D09B0-46FD-0DB7-1023-A3AF54491036";
	setAttr ".oc" -type "float3" 1 0.546 0.003 ;
createNode shadingEngine -n "sp_shader44SG";
	rename -uid "AB625901-4A69-4CD0-72CE-08BD50432C49";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo45";
	rename -uid "D9E8935A-4D7C-9AB7-DACB-5DAFBD55455A";
createNode surfaceShader -n "sp_shader45";
	rename -uid "84D5429D-4CAF-0E08-A017-868FF72675A4";
	setAttr ".oc" -type "float3" 0.11652204 0.26700506 0.63347065 ;
createNode shadingEngine -n "sp_shader45SG";
	rename -uid "1E75BA2A-4C55-05DD-E8C5-4D89197C82EC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo46";
	rename -uid "411D6D33-4049-6E8D-3AAB-DE805D6D421B";
createNode surfaceShader -n "sp_shader46";
	rename -uid "3320A8C0-4598-A603-6522-20A6B201F468";
	setAttr ".oc" -type "float3" 0.58576757 0.82126909 0.030367361 ;
createNode shadingEngine -n "sp_shader46SG";
	rename -uid "CE85911C-455E-70C1-6463-21B4582326EB";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo47";
	rename -uid "BE7E27FA-4D72-36F3-4E5F-E19F0E749AA4";
createNode surfaceShader -n "sp_shader47";
	rename -uid "78CBEF3D-49F4-615C-B702-8FBD8D6AB054";
	setAttr ".oc" -type "float3" 0.2945669 0.15642312 0.82146001 ;
createNode shadingEngine -n "sp_shader47SG";
	rename -uid "02C67289-4B12-9A7E-2C5D-DCB75CC4F70B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo48";
	rename -uid "9B575C95-45EF-13CA-D224-679E9604C7C7";
createNode surfaceShader -n "sp_shader48";
	rename -uid "AB4FB2C5-4E10-BFCB-A7C3-A2BB15748367";
	setAttr ".oc" -type "float3" 0.035456784 0.89962018 0.52763039 ;
createNode shadingEngine -n "sp_shader48SG";
	rename -uid "291E33FF-4ACB-D9F5-651F-5B814E088BFC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo49";
	rename -uid "EA8E71C7-4718-D137-89C6-A79C53F9638F";
createNode surfaceShader -n "sp_shader49";
	rename -uid "8EE4837F-4038-AB4E-6035-378CAF2E631C";
	setAttr ".oc" -type "float3" 0.70284599 0.93202996 0.037991162 ;
createNode shadingEngine -n "sp_shader49SG";
	rename -uid "9FD3336F-4C79-5EA8-A372-8A8E9FFD4ECA";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo50";
	rename -uid "B36B63A0-48E1-1534-933B-8A85EC11B6CC";
createNode surfaceShader -n "sp_shader50";
	rename -uid "3DAB5E97-4586-CEFC-433B-31ADF0E83B96";
	setAttr ".oc" -type "float3" 0.53810251 0.32126629 0.9067744 ;
createNode shadingEngine -n "sp_shader50SG";
	rename -uid "EB2CF912-462B-91FA-C638-2FAE44396E55";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo51";
	rename -uid "AC216744-4A71-B003-7BA7-A8B30BEEFE95";
createNode blinn -n "blinn1";
	rename -uid "C9A15811-4333-0AC2-75BF-D3841F9737C0";
	setAttr ".dc" 0.43902438879013062;
	setAttr ".c" -type "float3" 0 0 0 ;
	setAttr ".it" -type "float3" 0.024383917 0.024383917 0.024383917 ;
	setAttr ".sc" -type "float3" 0.30894941 0.30894941 0.30894941 ;
createNode shadingEngine -n "blinn1SG";
	rename -uid "7421AC22-431C-E3BC-F3A2-F6B7B9BB90D6";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo52";
	rename -uid "0F680531-4448-D25D-EBF2-5FBB9E4B3C07";
createNode makeNurbSphere -n "makeNurbSphere3";
	rename -uid "59F73A1E-47B4-09C3-A58E-1FA1F29081B9";
	setAttr ".ax" -type "double3" 0 1 0 ;
createNode rbfSolver -n "rbfSolver1";
	rename -uid "16092A95-4C77-88FA-7E36-3597D8DC4479";
	setAttr ".nd" 3;
	setAttr ".md" 3;
	setAttr ".sc" 2;
	setAttr ".nz" no;
	setAttr -s 3 ".ni";
	setAttr -s 3 ".ni";
	setAttr ".dist" 1;
	setAttr -s 50 ".ps";
	setAttr -s 3 ".ps[0].nk";
	setAttr -s 3 ".ps[0].nk";
	setAttr -s 3 ".ps[0].mv";
	setAttr -s 3 ".ps[0].mv";
	setAttr -s 3 ".ps[1].nk";
	setAttr -s 3 ".ps[1].nk";
	setAttr -s 3 ".ps[1].mv";
	setAttr -s 3 ".ps[1].mv";
	setAttr -s 3 ".ps[2].nk";
	setAttr -s 3 ".ps[2].nk";
	setAttr -s 3 ".ps[2].mv";
	setAttr -s 3 ".ps[2].mv";
	setAttr -s 3 ".ps[3].nk";
	setAttr -s 3 ".ps[3].nk";
	setAttr -s 3 ".ps[3].mv";
	setAttr -s 3 ".ps[3].mv";
	setAttr -s 3 ".ps[4].nk";
	setAttr -s 3 ".ps[4].nk";
	setAttr -s 3 ".ps[4].mv";
	setAttr -s 3 ".ps[4].mv";
	setAttr -s 3 ".ps[5].nk";
	setAttr -s 3 ".ps[5].nk";
	setAttr -s 3 ".ps[5].mv";
	setAttr -s 3 ".ps[5].mv";
	setAttr -s 3 ".ps[6].nk";
	setAttr -s 3 ".ps[6].nk";
	setAttr -s 3 ".ps[6].mv";
	setAttr -s 3 ".ps[6].mv";
	setAttr -s 3 ".ps[7].nk";
	setAttr -s 3 ".ps[7].nk";
	setAttr -s 3 ".ps[7].mv";
	setAttr -s 3 ".ps[7].mv";
	setAttr -s 3 ".ps[8].nk";
	setAttr -s 3 ".ps[8].nk";
	setAttr -s 3 ".ps[8].mv";
	setAttr -s 3 ".ps[8].mv";
	setAttr -s 3 ".ps[9].nk";
	setAttr -s 3 ".ps[9].nk";
	setAttr -s 3 ".ps[9].mv";
	setAttr -s 3 ".ps[9].mv";
	setAttr -s 3 ".ps[10].nk";
	setAttr -s 3 ".ps[10].nk";
	setAttr -s 3 ".ps[10].mv";
	setAttr -s 3 ".ps[10].mv";
	setAttr -s 3 ".ps[11].nk";
	setAttr -s 3 ".ps[11].nk";
	setAttr -s 3 ".ps[11].mv";
	setAttr -s 3 ".ps[11].mv";
	setAttr -s 3 ".ps[12].nk";
	setAttr -s 3 ".ps[12].nk";
	setAttr -s 3 ".ps[12].mv";
	setAttr -s 3 ".ps[12].mv";
	setAttr -s 3 ".ps[13].nk";
	setAttr -s 3 ".ps[13].nk";
	setAttr -s 3 ".ps[13].mv";
	setAttr -s 3 ".ps[13].mv";
	setAttr -s 3 ".ps[14].nk";
	setAttr -s 3 ".ps[14].nk";
	setAttr -s 3 ".ps[14].mv";
	setAttr -s 3 ".ps[14].mv";
	setAttr -s 3 ".ps[15].nk";
	setAttr -s 3 ".ps[15].nk";
	setAttr -s 3 ".ps[15].mv";
	setAttr -s 3 ".ps[15].mv";
	setAttr -s 3 ".ps[16].nk";
	setAttr -s 3 ".ps[16].nk";
	setAttr -s 3 ".ps[16].mv";
	setAttr -s 3 ".ps[16].mv";
	setAttr -s 3 ".ps[17].nk";
	setAttr -s 3 ".ps[17].nk";
	setAttr -s 3 ".ps[17].mv";
	setAttr -s 3 ".ps[17].mv";
	setAttr -s 3 ".ps[18].nk";
	setAttr -s 3 ".ps[18].nk";
	setAttr -s 3 ".ps[18].mv";
	setAttr -s 3 ".ps[18].mv";
	setAttr -s 3 ".ps[19].nk";
	setAttr -s 3 ".ps[19].nk";
	setAttr -s 3 ".ps[19].mv";
	setAttr -s 3 ".ps[19].mv";
	setAttr -s 3 ".ps[20].nk";
	setAttr -s 3 ".ps[20].nk";
	setAttr -s 3 ".ps[20].mv";
	setAttr -s 3 ".ps[20].mv";
	setAttr -s 3 ".ps[21].nk";
	setAttr -s 3 ".ps[21].nk";
	setAttr -s 3 ".ps[21].mv";
	setAttr -s 3 ".ps[21].mv";
	setAttr -s 3 ".ps[22].nk";
	setAttr -s 3 ".ps[22].nk";
	setAttr -s 3 ".ps[22].mv";
	setAttr -s 3 ".ps[22].mv";
	setAttr -s 3 ".ps[23].nk";
	setAttr -s 3 ".ps[23].nk";
	setAttr -s 3 ".ps[23].mv";
	setAttr -s 3 ".ps[23].mv";
	setAttr -s 3 ".ps[24].nk";
	setAttr -s 3 ".ps[24].nk";
	setAttr -s 3 ".ps[24].mv";
	setAttr -s 3 ".ps[24].mv";
	setAttr -s 3 ".ps[25].nk";
	setAttr -s 3 ".ps[25].nk";
	setAttr -s 3 ".ps[25].mv";
	setAttr -s 3 ".ps[25].mv";
	setAttr -s 3 ".ps[26].nk";
	setAttr -s 3 ".ps[26].nk";
	setAttr -s 3 ".ps[26].mv";
	setAttr -s 3 ".ps[26].mv";
	setAttr -s 3 ".ps[27].nk";
	setAttr -s 3 ".ps[27].nk";
	setAttr -s 3 ".ps[27].mv";
	setAttr -s 3 ".ps[27].mv";
	setAttr -s 3 ".ps[28].nk";
	setAttr -s 3 ".ps[28].nk";
	setAttr -s 3 ".ps[28].mv";
	setAttr -s 3 ".ps[28].mv";
	setAttr -s 3 ".ps[29].nk";
	setAttr -s 3 ".ps[29].nk";
	setAttr -s 3 ".ps[29].mv";
	setAttr -s 3 ".ps[29].mv";
	setAttr -s 3 ".ps[30].nk";
	setAttr -s 3 ".ps[30].nk";
	setAttr -s 3 ".ps[30].mv";
	setAttr -s 3 ".ps[30].mv";
	setAttr -s 3 ".ps[31].nk";
	setAttr -s 3 ".ps[31].nk";
	setAttr -s 3 ".ps[31].mv";
	setAttr -s 3 ".ps[31].mv";
	setAttr -s 3 ".ps[32].nk";
	setAttr -s 3 ".ps[32].nk";
	setAttr -s 3 ".ps[32].mv";
	setAttr -s 3 ".ps[32].mv";
	setAttr -s 3 ".ps[33].nk";
	setAttr -s 3 ".ps[33].nk";
	setAttr -s 3 ".ps[33].mv";
	setAttr -s 3 ".ps[33].mv";
	setAttr -s 3 ".ps[34].nk";
	setAttr -s 3 ".ps[34].nk";
	setAttr -s 3 ".ps[34].mv";
	setAttr -s 3 ".ps[34].mv";
	setAttr -s 3 ".ps[35].nk";
	setAttr -s 3 ".ps[35].nk";
	setAttr -s 3 ".ps[35].mv";
	setAttr -s 3 ".ps[35].mv";
	setAttr -s 3 ".ps[36].nk";
	setAttr -s 3 ".ps[36].nk";
	setAttr -s 3 ".ps[36].mv";
	setAttr -s 3 ".ps[36].mv";
	setAttr -s 3 ".ps[37].nk";
	setAttr -s 3 ".ps[37].nk";
	setAttr -s 3 ".ps[37].mv";
	setAttr -s 3 ".ps[37].mv";
	setAttr -s 3 ".ps[38].nk";
	setAttr -s 3 ".ps[38].nk";
	setAttr -s 3 ".ps[38].mv";
	setAttr -s 3 ".ps[38].mv";
	setAttr -s 3 ".ps[39].nk";
	setAttr -s 3 ".ps[39].nk";
	setAttr -s 3 ".ps[39].mv";
	setAttr -s 3 ".ps[39].mv";
	setAttr -s 3 ".ps[40].nk";
	setAttr -s 3 ".ps[40].nk";
	setAttr -s 3 ".ps[40].mv";
	setAttr -s 3 ".ps[40].mv";
	setAttr -s 3 ".ps[41].nk";
	setAttr -s 3 ".ps[41].nk";
	setAttr -s 3 ".ps[41].mv";
	setAttr -s 3 ".ps[41].mv";
	setAttr -s 3 ".ps[42].nk";
	setAttr -s 3 ".ps[42].nk";
	setAttr -s 3 ".ps[42].mv";
	setAttr -s 3 ".ps[42].mv";
	setAttr -s 3 ".ps[43].nk";
	setAttr -s 3 ".ps[43].nk";
	setAttr -s 3 ".ps[43].mv";
	setAttr -s 3 ".ps[43].mv";
	setAttr -s 3 ".ps[44].nk";
	setAttr -s 3 ".ps[44].nk";
	setAttr -s 3 ".ps[44].mv";
	setAttr -s 3 ".ps[44].mv";
	setAttr -s 3 ".ps[45].nk";
	setAttr -s 3 ".ps[45].nk";
	setAttr -s 3 ".ps[45].mv";
	setAttr -s 3 ".ps[45].mv";
	setAttr -s 3 ".ps[46].nk";
	setAttr -s 3 ".ps[46].nk";
	setAttr -s 3 ".ps[46].mv";
	setAttr -s 3 ".ps[46].mv";
	setAttr -s 3 ".ps[47].nk";
	setAttr -s 3 ".ps[47].nk";
	setAttr -s 3 ".ps[47].mv";
	setAttr -s 3 ".ps[47].mv";
	setAttr -s 3 ".ps[48].nk";
	setAttr -s 3 ".ps[48].nk";
	setAttr -s 3 ".ps[48].mv";
	setAttr -s 3 ".ps[48].mv";
	setAttr -s 3 ".ps[49].nk";
	setAttr -s 3 ".ps[49].nk";
	setAttr -s 3 ".ps[49].mv";
	setAttr -s 3 ".ps[49].mv";
	setAttr -s 3 ".mo";
createNode vectorProduct -n "vectorProduct1";
	rename -uid "AF17E1C7-4FB7-4970-19F8-A9AFB8770C4D";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 1 0 0 ;
createNode hyperGraphInfo -n "nodeEditorPanel1Info";
	rename -uid "DE0933E1-4F75-349F-5EBF-0B8438457976";
createNode hyperView -n "hyperView1";
	rename -uid "53F6987F-41D5-01BB-640E-F890B6C15D03";
	setAttr ".dag" no;
createNode hyperLayout -n "hyperLayout1";
	rename -uid "39377A47-4D24-3A23-98E1-97A1B8FB9002";
	setAttr ".ihi" 0;
	setAttr ".hyp[0].nvs" 1920;
	setAttr ".anf" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 54 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 54 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultRenderGlobals;
	setAttr ".ep" 1;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w" 640;
	setAttr -av -k on ".h" 480;
	setAttr -av -k on ".pa";
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar" 1.3333332538604736;
	setAttr -av -k on ".ldar";
	setAttr -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -k on ".isu";
	setAttr -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :hardwareRenderingGlobals;
	setAttr ".vac" 2;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -av -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -av -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".fn";
	setAttr -k on ".if";
	setAttr -k on ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -av -k on ".fir";
	setAttr -k on ".aap";
	setAttr -av -k on ".gh";
	setAttr -cb on ".sd";
connectAttr "makeNurbSphere3.os" "unusedShape.cr";
relationship "link" ":lightLinker1" "surfaceShader1SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader1SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader3SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader4SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader5SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader6SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader7SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader8SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader9SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader10SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader11SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader12SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader13SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader14SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader15SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader16SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader17SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader18SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader19SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader20SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader21SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader22SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader23SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader24SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader25SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader26SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader27SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader28SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader29SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader30SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader31SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader32SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader33SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader34SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader35SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader36SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader37SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader38SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader39SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader40SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader41SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader42SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader43SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader44SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader45SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader46SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader47SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader48SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader49SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "sp_shader50SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "blinn1SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "surfaceShader1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader3SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader4SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader5SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader6SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader7SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader8SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader9SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader10SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader11SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader12SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader13SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader14SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader15SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader16SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader17SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader18SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader19SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader20SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader21SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader22SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader23SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader24SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader25SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader26SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader27SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader28SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader29SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader30SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader31SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader32SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader33SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader34SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader35SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader36SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader37SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader38SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader39SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader40SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader41SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader42SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader43SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader44SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader45SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader46SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader47SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader48SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader49SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "sp_shader50SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "blinn1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "rbfSolver1.mo[0]" "outShader.ocr";
connectAttr "rbfSolver1.mo[1]" "outShader.ocg";
connectAttr "rbfSolver1.mo[2]" "outShader.ocb";
connectAttr "outShader.oc" "surfaceShader1SG.ss";
connectAttr "output_colorShape.iog" "surfaceShader1SG.dsm" -na;
connectAttr "surfaceShader1SG.msg" "materialInfo1.sg";
connectAttr "outShader.msg" "materialInfo1.m";
connectAttr "outShader.msg" "materialInfo1.t" -na;
connectAttr "sp_shader1.oc" "sp_shader1SG.ss";
connectAttr "pose1Shape.iog" "sp_shader1SG.dsm" -na;
connectAttr "sp_shader1SG.msg" "materialInfo2.sg";
connectAttr "sp_shader1.msg" "materialInfo2.m";
connectAttr "sp_shader1.msg" "materialInfo2.t" -na;
connectAttr "sp_shader2.oc" "sp_shader2SG.ss";
connectAttr "pose2Shape.iog" "sp_shader2SG.dsm" -na;
connectAttr "sp_shader2SG.msg" "materialInfo3.sg";
connectAttr "sp_shader2.msg" "materialInfo3.m";
connectAttr "sp_shader2.msg" "materialInfo3.t" -na;
connectAttr "sp_shader3.oc" "sp_shader3SG.ss";
connectAttr "pose3Shape.iog" "sp_shader3SG.dsm" -na;
connectAttr "sp_shader3SG.msg" "materialInfo4.sg";
connectAttr "sp_shader3.msg" "materialInfo4.m";
connectAttr "sp_shader3.msg" "materialInfo4.t" -na;
connectAttr "sp_shader4.oc" "sp_shader4SG.ss";
connectAttr "pose4Shape.iog" "sp_shader4SG.dsm" -na;
connectAttr "sp_shader4SG.msg" "materialInfo5.sg";
connectAttr "sp_shader4.msg" "materialInfo5.m";
connectAttr "sp_shader4.msg" "materialInfo5.t" -na;
connectAttr "sp_shader5.oc" "sp_shader5SG.ss";
connectAttr "pose5Shape.iog" "sp_shader5SG.dsm" -na;
connectAttr "sp_shader5SG.msg" "materialInfo6.sg";
connectAttr "sp_shader5.msg" "materialInfo6.m";
connectAttr "sp_shader5.msg" "materialInfo6.t" -na;
connectAttr "sp_shader6.oc" "sp_shader6SG.ss";
connectAttr "pose6Shape.iog" "sp_shader6SG.dsm" -na;
connectAttr "sp_shader6SG.msg" "materialInfo7.sg";
connectAttr "sp_shader6.msg" "materialInfo7.m";
connectAttr "sp_shader6.msg" "materialInfo7.t" -na;
connectAttr "sp_shader7.oc" "sp_shader7SG.ss";
connectAttr "pose7Shape.iog" "sp_shader7SG.dsm" -na;
connectAttr "sp_shader7SG.msg" "materialInfo8.sg";
connectAttr "sp_shader7.msg" "materialInfo8.m";
connectAttr "sp_shader7.msg" "materialInfo8.t" -na;
connectAttr "sp_shader8.oc" "sp_shader8SG.ss";
connectAttr "pose8Shape.iog" "sp_shader8SG.dsm" -na;
connectAttr "sp_shader8SG.msg" "materialInfo9.sg";
connectAttr "sp_shader8.msg" "materialInfo9.m";
connectAttr "sp_shader8.msg" "materialInfo9.t" -na;
connectAttr "sp_shader9.oc" "sp_shader9SG.ss";
connectAttr "pose9Shape.iog" "sp_shader9SG.dsm" -na;
connectAttr "sp_shader9SG.msg" "materialInfo10.sg";
connectAttr "sp_shader9.msg" "materialInfo10.m";
connectAttr "sp_shader9.msg" "materialInfo10.t" -na;
connectAttr "sp_shader10.oc" "sp_shader10SG.ss";
connectAttr "pose10Shape.iog" "sp_shader10SG.dsm" -na;
connectAttr "sp_shader10SG.msg" "materialInfo11.sg";
connectAttr "sp_shader10.msg" "materialInfo11.m";
connectAttr "sp_shader10.msg" "materialInfo11.t" -na;
connectAttr "sp_shader11.oc" "sp_shader11SG.ss";
connectAttr "pose11Shape.iog" "sp_shader11SG.dsm" -na;
connectAttr "sp_shader11SG.msg" "materialInfo12.sg";
connectAttr "sp_shader11.msg" "materialInfo12.m";
connectAttr "sp_shader11.msg" "materialInfo12.t" -na;
connectAttr "sp_shader12.oc" "sp_shader12SG.ss";
connectAttr "pose12Shape.iog" "sp_shader12SG.dsm" -na;
connectAttr "sp_shader12SG.msg" "materialInfo13.sg";
connectAttr "sp_shader12.msg" "materialInfo13.m";
connectAttr "sp_shader12.msg" "materialInfo13.t" -na;
connectAttr "sp_shader13.oc" "sp_shader13SG.ss";
connectAttr "pose13Shape.iog" "sp_shader13SG.dsm" -na;
connectAttr "sp_shader13SG.msg" "materialInfo14.sg";
connectAttr "sp_shader13.msg" "materialInfo14.m";
connectAttr "sp_shader13.msg" "materialInfo14.t" -na;
connectAttr "sp_shader14.oc" "sp_shader14SG.ss";
connectAttr "pose14Shape.iog" "sp_shader14SG.dsm" -na;
connectAttr "sp_shader14SG.msg" "materialInfo15.sg";
connectAttr "sp_shader14.msg" "materialInfo15.m";
connectAttr "sp_shader14.msg" "materialInfo15.t" -na;
connectAttr "sp_shader15.oc" "sp_shader15SG.ss";
connectAttr "pose15Shape.iog" "sp_shader15SG.dsm" -na;
connectAttr "sp_shader15SG.msg" "materialInfo16.sg";
connectAttr "sp_shader15.msg" "materialInfo16.m";
connectAttr "sp_shader15.msg" "materialInfo16.t" -na;
connectAttr "sp_shader16.oc" "sp_shader16SG.ss";
connectAttr "pose16Shape.iog" "sp_shader16SG.dsm" -na;
connectAttr "sp_shader16SG.msg" "materialInfo17.sg";
connectAttr "sp_shader16.msg" "materialInfo17.m";
connectAttr "sp_shader16.msg" "materialInfo17.t" -na;
connectAttr "sp_shader17.oc" "sp_shader17SG.ss";
connectAttr "pose17Shape.iog" "sp_shader17SG.dsm" -na;
connectAttr "sp_shader17SG.msg" "materialInfo18.sg";
connectAttr "sp_shader17.msg" "materialInfo18.m";
connectAttr "sp_shader17.msg" "materialInfo18.t" -na;
connectAttr "sp_shader18.oc" "sp_shader18SG.ss";
connectAttr "pose18Shape.iog" "sp_shader18SG.dsm" -na;
connectAttr "sp_shader18SG.msg" "materialInfo19.sg";
connectAttr "sp_shader18.msg" "materialInfo19.m";
connectAttr "sp_shader18.msg" "materialInfo19.t" -na;
connectAttr "sp_shader19.oc" "sp_shader19SG.ss";
connectAttr "pose19Shape.iog" "sp_shader19SG.dsm" -na;
connectAttr "sp_shader19SG.msg" "materialInfo20.sg";
connectAttr "sp_shader19.msg" "materialInfo20.m";
connectAttr "sp_shader19.msg" "materialInfo20.t" -na;
connectAttr "sp_shader20.oc" "sp_shader20SG.ss";
connectAttr "pose20Shape.iog" "sp_shader20SG.dsm" -na;
connectAttr "sp_shader20SG.msg" "materialInfo21.sg";
connectAttr "sp_shader20.msg" "materialInfo21.m";
connectAttr "sp_shader20.msg" "materialInfo21.t" -na;
connectAttr "sp_shader21.oc" "sp_shader21SG.ss";
connectAttr "pose21Shape.iog" "sp_shader21SG.dsm" -na;
connectAttr "sp_shader21SG.msg" "materialInfo22.sg";
connectAttr "sp_shader21.msg" "materialInfo22.m";
connectAttr "sp_shader21.msg" "materialInfo22.t" -na;
connectAttr "sp_shader22.oc" "sp_shader22SG.ss";
connectAttr "pose22Shape.iog" "sp_shader22SG.dsm" -na;
connectAttr "sp_shader22SG.msg" "materialInfo23.sg";
connectAttr "sp_shader22.msg" "materialInfo23.m";
connectAttr "sp_shader22.msg" "materialInfo23.t" -na;
connectAttr "sp_shader23.oc" "sp_shader23SG.ss";
connectAttr "pose23Shape.iog" "sp_shader23SG.dsm" -na;
connectAttr "sp_shader23SG.msg" "materialInfo24.sg";
connectAttr "sp_shader23.msg" "materialInfo24.m";
connectAttr "sp_shader23.msg" "materialInfo24.t" -na;
connectAttr "sp_shader24.oc" "sp_shader24SG.ss";
connectAttr "pose24Shape.iog" "sp_shader24SG.dsm" -na;
connectAttr "sp_shader24SG.msg" "materialInfo25.sg";
connectAttr "sp_shader24.msg" "materialInfo25.m";
connectAttr "sp_shader24.msg" "materialInfo25.t" -na;
connectAttr "sp_shader25.oc" "sp_shader25SG.ss";
connectAttr "pose25Shape.iog" "sp_shader25SG.dsm" -na;
connectAttr "sp_shader25SG.msg" "materialInfo26.sg";
connectAttr "sp_shader25.msg" "materialInfo26.m";
connectAttr "sp_shader25.msg" "materialInfo26.t" -na;
connectAttr "sp_shader26.oc" "sp_shader26SG.ss";
connectAttr "pose26Shape.iog" "sp_shader26SG.dsm" -na;
connectAttr "sp_shader26SG.msg" "materialInfo27.sg";
connectAttr "sp_shader26.msg" "materialInfo27.m";
connectAttr "sp_shader26.msg" "materialInfo27.t" -na;
connectAttr "sp_shader27.oc" "sp_shader27SG.ss";
connectAttr "pose27Shape.iog" "sp_shader27SG.dsm" -na;
connectAttr "sp_shader27SG.msg" "materialInfo28.sg";
connectAttr "sp_shader27.msg" "materialInfo28.m";
connectAttr "sp_shader27.msg" "materialInfo28.t" -na;
connectAttr "sp_shader28.oc" "sp_shader28SG.ss";
connectAttr "pose28Shape.iog" "sp_shader28SG.dsm" -na;
connectAttr "sp_shader28SG.msg" "materialInfo29.sg";
connectAttr "sp_shader28.msg" "materialInfo29.m";
connectAttr "sp_shader28.msg" "materialInfo29.t" -na;
connectAttr "sp_shader29.oc" "sp_shader29SG.ss";
connectAttr "pose29Shape.iog" "sp_shader29SG.dsm" -na;
connectAttr "sp_shader29SG.msg" "materialInfo30.sg";
connectAttr "sp_shader29.msg" "materialInfo30.m";
connectAttr "sp_shader29.msg" "materialInfo30.t" -na;
connectAttr "sp_shader30.oc" "sp_shader30SG.ss";
connectAttr "pose30Shape.iog" "sp_shader30SG.dsm" -na;
connectAttr "sp_shader30SG.msg" "materialInfo31.sg";
connectAttr "sp_shader30.msg" "materialInfo31.m";
connectAttr "sp_shader30.msg" "materialInfo31.t" -na;
connectAttr "sp_shader31.oc" "sp_shader31SG.ss";
connectAttr "pose31Shape.iog" "sp_shader31SG.dsm" -na;
connectAttr "sp_shader31SG.msg" "materialInfo32.sg";
connectAttr "sp_shader31.msg" "materialInfo32.m";
connectAttr "sp_shader31.msg" "materialInfo32.t" -na;
connectAttr "sp_shader32.oc" "sp_shader32SG.ss";
connectAttr "pose32Shape.iog" "sp_shader32SG.dsm" -na;
connectAttr "sp_shader32SG.msg" "materialInfo33.sg";
connectAttr "sp_shader32.msg" "materialInfo33.m";
connectAttr "sp_shader32.msg" "materialInfo33.t" -na;
connectAttr "sp_shader33.oc" "sp_shader33SG.ss";
connectAttr "pose33Shape.iog" "sp_shader33SG.dsm" -na;
connectAttr "sp_shader33SG.msg" "materialInfo34.sg";
connectAttr "sp_shader33.msg" "materialInfo34.m";
connectAttr "sp_shader33.msg" "materialInfo34.t" -na;
connectAttr "sp_shader34.oc" "sp_shader34SG.ss";
connectAttr "pose34Shape.iog" "sp_shader34SG.dsm" -na;
connectAttr "sp_shader34SG.msg" "materialInfo35.sg";
connectAttr "sp_shader34.msg" "materialInfo35.m";
connectAttr "sp_shader34.msg" "materialInfo35.t" -na;
connectAttr "sp_shader35.oc" "sp_shader35SG.ss";
connectAttr "pose35Shape.iog" "sp_shader35SG.dsm" -na;
connectAttr "sp_shader35SG.msg" "materialInfo36.sg";
connectAttr "sp_shader35.msg" "materialInfo36.m";
connectAttr "sp_shader35.msg" "materialInfo36.t" -na;
connectAttr "sp_shader36.oc" "sp_shader36SG.ss";
connectAttr "pose36Shape.iog" "sp_shader36SG.dsm" -na;
connectAttr "sp_shader36SG.msg" "materialInfo37.sg";
connectAttr "sp_shader36.msg" "materialInfo37.m";
connectAttr "sp_shader36.msg" "materialInfo37.t" -na;
connectAttr "sp_shader37.oc" "sp_shader37SG.ss";
connectAttr "pose37Shape.iog" "sp_shader37SG.dsm" -na;
connectAttr "sp_shader37SG.msg" "materialInfo38.sg";
connectAttr "sp_shader37.msg" "materialInfo38.m";
connectAttr "sp_shader37.msg" "materialInfo38.t" -na;
connectAttr "sp_shader38.oc" "sp_shader38SG.ss";
connectAttr "pose38Shape.iog" "sp_shader38SG.dsm" -na;
connectAttr "sp_shader38SG.msg" "materialInfo39.sg";
connectAttr "sp_shader38.msg" "materialInfo39.m";
connectAttr "sp_shader38.msg" "materialInfo39.t" -na;
connectAttr "sp_shader39.oc" "sp_shader39SG.ss";
connectAttr "pose39Shape.iog" "sp_shader39SG.dsm" -na;
connectAttr "sp_shader39SG.msg" "materialInfo40.sg";
connectAttr "sp_shader39.msg" "materialInfo40.m";
connectAttr "sp_shader39.msg" "materialInfo40.t" -na;
connectAttr "sp_shader40.oc" "sp_shader40SG.ss";
connectAttr "pose40Shape.iog" "sp_shader40SG.dsm" -na;
connectAttr "sp_shader40SG.msg" "materialInfo41.sg";
connectAttr "sp_shader40.msg" "materialInfo41.m";
connectAttr "sp_shader40.msg" "materialInfo41.t" -na;
connectAttr "sp_shader41.oc" "sp_shader41SG.ss";
connectAttr "pose41Shape.iog" "sp_shader41SG.dsm" -na;
connectAttr "sp_shader41SG.msg" "materialInfo42.sg";
connectAttr "sp_shader41.msg" "materialInfo42.m";
connectAttr "sp_shader41.msg" "materialInfo42.t" -na;
connectAttr "sp_shader42.oc" "sp_shader42SG.ss";
connectAttr "pose42Shape.iog" "sp_shader42SG.dsm" -na;
connectAttr "sp_shader42SG.msg" "materialInfo43.sg";
connectAttr "sp_shader42.msg" "materialInfo43.m";
connectAttr "sp_shader42.msg" "materialInfo43.t" -na;
connectAttr "sp_shader43.oc" "sp_shader43SG.ss";
connectAttr "pose43Shape.iog" "sp_shader43SG.dsm" -na;
connectAttr "sp_shader43SG.msg" "materialInfo44.sg";
connectAttr "sp_shader43.msg" "materialInfo44.m";
connectAttr "sp_shader43.msg" "materialInfo44.t" -na;
connectAttr "sp_shader44.oc" "sp_shader44SG.ss";
connectAttr "pose44Shape.iog" "sp_shader44SG.dsm" -na;
connectAttr "sp_shader44SG.msg" "materialInfo45.sg";
connectAttr "sp_shader44.msg" "materialInfo45.m";
connectAttr "sp_shader44.msg" "materialInfo45.t" -na;
connectAttr "sp_shader45.oc" "sp_shader45SG.ss";
connectAttr "pose45Shape.iog" "sp_shader45SG.dsm" -na;
connectAttr "sp_shader45SG.msg" "materialInfo46.sg";
connectAttr "sp_shader45.msg" "materialInfo46.m";
connectAttr "sp_shader45.msg" "materialInfo46.t" -na;
connectAttr "sp_shader46.oc" "sp_shader46SG.ss";
connectAttr "pose46Shape.iog" "sp_shader46SG.dsm" -na;
connectAttr "sp_shader46SG.msg" "materialInfo47.sg";
connectAttr "sp_shader46.msg" "materialInfo47.m";
connectAttr "sp_shader46.msg" "materialInfo47.t" -na;
connectAttr "sp_shader47.oc" "sp_shader47SG.ss";
connectAttr "pose47Shape.iog" "sp_shader47SG.dsm" -na;
connectAttr "sp_shader47SG.msg" "materialInfo48.sg";
connectAttr "sp_shader47.msg" "materialInfo48.m";
connectAttr "sp_shader47.msg" "materialInfo48.t" -na;
connectAttr "sp_shader48.oc" "sp_shader48SG.ss";
connectAttr "pose48Shape.iog" "sp_shader48SG.dsm" -na;
connectAttr "sp_shader48SG.msg" "materialInfo49.sg";
connectAttr "sp_shader48.msg" "materialInfo49.m";
connectAttr "sp_shader48.msg" "materialInfo49.t" -na;
connectAttr "sp_shader49.oc" "sp_shader49SG.ss";
connectAttr "pose49Shape.iog" "sp_shader49SG.dsm" -na;
connectAttr "sp_shader49SG.msg" "materialInfo50.sg";
connectAttr "sp_shader49.msg" "materialInfo50.m";
connectAttr "sp_shader49.msg" "materialInfo50.t" -na;
connectAttr "sp_shader50.oc" "sp_shader50SG.ss";
connectAttr "pose50Shape.iog" "sp_shader50SG.dsm" -na;
connectAttr "sp_shader50SG.msg" "materialInfo51.sg";
connectAttr "sp_shader50.msg" "materialInfo51.m";
connectAttr "sp_shader50.msg" "materialInfo51.t" -na;
connectAttr "blinn1.oc" "blinn1SG.ss";
connectAttr "unusedShape.iog" "blinn1SG.dsm" -na;
connectAttr "blinn1SG.msg" "materialInfo52.sg";
connectAttr "blinn1.msg" "materialInfo52.m";
connectAttr "vectorProduct1.ox" "rbfSolver1.ni[0]";
connectAttr "vectorProduct1.oy" "rbfSolver1.ni[1]";
connectAttr "vectorProduct1.oz" "rbfSolver1.ni[2]";
connectAttr "pose1.tx" "rbfSolver1.ps[0].nk[0]";
connectAttr "pose1.ty" "rbfSolver1.ps[0].nk[1]";
connectAttr "pose1.tz" "rbfSolver1.ps[0].nk[2]";
connectAttr "sp_shader1.ocr" "rbfSolver1.ps[0].mv[0]";
connectAttr "sp_shader1.ocg" "rbfSolver1.ps[0].mv[1]";
connectAttr "sp_shader1.ocb" "rbfSolver1.ps[0].mv[2]";
connectAttr "pose2.tx" "rbfSolver1.ps[1].nk[0]";
connectAttr "pose2.ty" "rbfSolver1.ps[1].nk[1]";
connectAttr "pose2.tz" "rbfSolver1.ps[1].nk[2]";
connectAttr "sp_shader2.ocr" "rbfSolver1.ps[1].mv[0]";
connectAttr "sp_shader2.ocg" "rbfSolver1.ps[1].mv[1]";
connectAttr "sp_shader2.ocb" "rbfSolver1.ps[1].mv[2]";
connectAttr "pose3.tx" "rbfSolver1.ps[2].nk[0]";
connectAttr "pose3.ty" "rbfSolver1.ps[2].nk[1]";
connectAttr "pose3.tz" "rbfSolver1.ps[2].nk[2]";
connectAttr "sp_shader3.ocr" "rbfSolver1.ps[2].mv[0]";
connectAttr "sp_shader3.ocg" "rbfSolver1.ps[2].mv[1]";
connectAttr "sp_shader3.ocb" "rbfSolver1.ps[2].mv[2]";
connectAttr "pose4.tx" "rbfSolver1.ps[3].nk[0]";
connectAttr "pose4.ty" "rbfSolver1.ps[3].nk[1]";
connectAttr "pose4.tz" "rbfSolver1.ps[3].nk[2]";
connectAttr "sp_shader4.ocr" "rbfSolver1.ps[3].mv[0]";
connectAttr "sp_shader4.ocg" "rbfSolver1.ps[3].mv[1]";
connectAttr "sp_shader4.ocb" "rbfSolver1.ps[3].mv[2]";
connectAttr "pose5.tx" "rbfSolver1.ps[4].nk[0]";
connectAttr "pose5.ty" "rbfSolver1.ps[4].nk[1]";
connectAttr "pose5.tz" "rbfSolver1.ps[4].nk[2]";
connectAttr "sp_shader5.ocr" "rbfSolver1.ps[4].mv[0]";
connectAttr "sp_shader5.ocg" "rbfSolver1.ps[4].mv[1]";
connectAttr "sp_shader5.ocb" "rbfSolver1.ps[4].mv[2]";
connectAttr "pose6.tx" "rbfSolver1.ps[5].nk[0]";
connectAttr "pose6.ty" "rbfSolver1.ps[5].nk[1]";
connectAttr "pose6.tz" "rbfSolver1.ps[5].nk[2]";
connectAttr "sp_shader6.ocr" "rbfSolver1.ps[5].mv[0]";
connectAttr "sp_shader6.ocg" "rbfSolver1.ps[5].mv[1]";
connectAttr "sp_shader6.ocb" "rbfSolver1.ps[5].mv[2]";
connectAttr "pose7.tx" "rbfSolver1.ps[6].nk[0]";
connectAttr "pose7.ty" "rbfSolver1.ps[6].nk[1]";
connectAttr "pose7.tz" "rbfSolver1.ps[6].nk[2]";
connectAttr "sp_shader7.ocr" "rbfSolver1.ps[6].mv[0]";
connectAttr "sp_shader7.ocg" "rbfSolver1.ps[6].mv[1]";
connectAttr "sp_shader7.ocb" "rbfSolver1.ps[6].mv[2]";
connectAttr "pose8.tx" "rbfSolver1.ps[7].nk[0]";
connectAttr "pose8.ty" "rbfSolver1.ps[7].nk[1]";
connectAttr "pose8.tz" "rbfSolver1.ps[7].nk[2]";
connectAttr "sp_shader8.ocr" "rbfSolver1.ps[7].mv[0]";
connectAttr "sp_shader8.ocg" "rbfSolver1.ps[7].mv[1]";
connectAttr "sp_shader8.ocb" "rbfSolver1.ps[7].mv[2]";
connectAttr "pose9.tx" "rbfSolver1.ps[8].nk[0]";
connectAttr "pose9.ty" "rbfSolver1.ps[8].nk[1]";
connectAttr "pose9.tz" "rbfSolver1.ps[8].nk[2]";
connectAttr "sp_shader9.ocr" "rbfSolver1.ps[8].mv[0]";
connectAttr "sp_shader9.ocg" "rbfSolver1.ps[8].mv[1]";
connectAttr "sp_shader9.ocb" "rbfSolver1.ps[8].mv[2]";
connectAttr "pose10.tx" "rbfSolver1.ps[9].nk[0]";
connectAttr "pose10.ty" "rbfSolver1.ps[9].nk[1]";
connectAttr "pose10.tz" "rbfSolver1.ps[9].nk[2]";
connectAttr "sp_shader10.ocr" "rbfSolver1.ps[9].mv[0]";
connectAttr "sp_shader10.ocg" "rbfSolver1.ps[9].mv[1]";
connectAttr "sp_shader10.ocb" "rbfSolver1.ps[9].mv[2]";
connectAttr "pose11.tx" "rbfSolver1.ps[10].nk[0]";
connectAttr "pose11.ty" "rbfSolver1.ps[10].nk[1]";
connectAttr "pose11.tz" "rbfSolver1.ps[10].nk[2]";
connectAttr "sp_shader11.ocr" "rbfSolver1.ps[10].mv[0]";
connectAttr "sp_shader11.ocg" "rbfSolver1.ps[10].mv[1]";
connectAttr "sp_shader11.ocb" "rbfSolver1.ps[10].mv[2]";
connectAttr "pose12.tx" "rbfSolver1.ps[11].nk[0]";
connectAttr "pose12.ty" "rbfSolver1.ps[11].nk[1]";
connectAttr "pose12.tz" "rbfSolver1.ps[11].nk[2]";
connectAttr "sp_shader12.ocr" "rbfSolver1.ps[11].mv[0]";
connectAttr "sp_shader12.ocg" "rbfSolver1.ps[11].mv[1]";
connectAttr "sp_shader12.ocb" "rbfSolver1.ps[11].mv[2]";
connectAttr "pose13.tx" "rbfSolver1.ps[12].nk[0]";
connectAttr "pose13.ty" "rbfSolver1.ps[12].nk[1]";
connectAttr "pose13.tz" "rbfSolver1.ps[12].nk[2]";
connectAttr "sp_shader13.ocr" "rbfSolver1.ps[12].mv[0]";
connectAttr "sp_shader13.ocg" "rbfSolver1.ps[12].mv[1]";
connectAttr "sp_shader13.ocb" "rbfSolver1.ps[12].mv[2]";
connectAttr "pose14.tx" "rbfSolver1.ps[13].nk[0]";
connectAttr "pose14.ty" "rbfSolver1.ps[13].nk[1]";
connectAttr "pose14.tz" "rbfSolver1.ps[13].nk[2]";
connectAttr "sp_shader14.ocr" "rbfSolver1.ps[13].mv[0]";
connectAttr "sp_shader14.ocg" "rbfSolver1.ps[13].mv[1]";
connectAttr "sp_shader14.ocb" "rbfSolver1.ps[13].mv[2]";
connectAttr "pose15.tx" "rbfSolver1.ps[14].nk[0]";
connectAttr "pose15.ty" "rbfSolver1.ps[14].nk[1]";
connectAttr "pose15.tz" "rbfSolver1.ps[14].nk[2]";
connectAttr "sp_shader15.ocr" "rbfSolver1.ps[14].mv[0]";
connectAttr "sp_shader15.ocg" "rbfSolver1.ps[14].mv[1]";
connectAttr "sp_shader15.ocb" "rbfSolver1.ps[14].mv[2]";
connectAttr "pose16.tx" "rbfSolver1.ps[15].nk[0]";
connectAttr "pose16.ty" "rbfSolver1.ps[15].nk[1]";
connectAttr "pose16.tz" "rbfSolver1.ps[15].nk[2]";
connectAttr "sp_shader16.ocr" "rbfSolver1.ps[15].mv[0]";
connectAttr "sp_shader16.ocg" "rbfSolver1.ps[15].mv[1]";
connectAttr "sp_shader16.ocb" "rbfSolver1.ps[15].mv[2]";
connectAttr "pose17.tx" "rbfSolver1.ps[16].nk[0]";
connectAttr "pose17.ty" "rbfSolver1.ps[16].nk[1]";
connectAttr "pose17.tz" "rbfSolver1.ps[16].nk[2]";
connectAttr "sp_shader17.ocr" "rbfSolver1.ps[16].mv[0]";
connectAttr "sp_shader17.ocg" "rbfSolver1.ps[16].mv[1]";
connectAttr "sp_shader17.ocb" "rbfSolver1.ps[16].mv[2]";
connectAttr "pose18.tx" "rbfSolver1.ps[17].nk[0]";
connectAttr "pose18.ty" "rbfSolver1.ps[17].nk[1]";
connectAttr "pose18.tz" "rbfSolver1.ps[17].nk[2]";
connectAttr "sp_shader18.ocr" "rbfSolver1.ps[17].mv[0]";
connectAttr "sp_shader18.ocg" "rbfSolver1.ps[17].mv[1]";
connectAttr "sp_shader18.ocb" "rbfSolver1.ps[17].mv[2]";
connectAttr "pose19.tx" "rbfSolver1.ps[18].nk[0]";
connectAttr "pose19.ty" "rbfSolver1.ps[18].nk[1]";
connectAttr "pose19.tz" "rbfSolver1.ps[18].nk[2]";
connectAttr "sp_shader19.ocr" "rbfSolver1.ps[18].mv[0]";
connectAttr "sp_shader19.ocg" "rbfSolver1.ps[18].mv[1]";
connectAttr "sp_shader19.ocb" "rbfSolver1.ps[18].mv[2]";
connectAttr "pose20.tx" "rbfSolver1.ps[19].nk[0]";
connectAttr "pose20.ty" "rbfSolver1.ps[19].nk[1]";
connectAttr "pose20.tz" "rbfSolver1.ps[19].nk[2]";
connectAttr "sp_shader20.ocr" "rbfSolver1.ps[19].mv[0]";
connectAttr "sp_shader20.ocg" "rbfSolver1.ps[19].mv[1]";
connectAttr "sp_shader20.ocb" "rbfSolver1.ps[19].mv[2]";
connectAttr "pose21.tx" "rbfSolver1.ps[20].nk[0]";
connectAttr "pose21.ty" "rbfSolver1.ps[20].nk[1]";
connectAttr "pose21.tz" "rbfSolver1.ps[20].nk[2]";
connectAttr "sp_shader21.ocr" "rbfSolver1.ps[20].mv[0]";
connectAttr "sp_shader21.ocg" "rbfSolver1.ps[20].mv[1]";
connectAttr "sp_shader21.ocb" "rbfSolver1.ps[20].mv[2]";
connectAttr "pose22.tx" "rbfSolver1.ps[21].nk[0]";
connectAttr "pose22.ty" "rbfSolver1.ps[21].nk[1]";
connectAttr "pose22.tz" "rbfSolver1.ps[21].nk[2]";
connectAttr "sp_shader22.ocr" "rbfSolver1.ps[21].mv[0]";
connectAttr "sp_shader22.ocg" "rbfSolver1.ps[21].mv[1]";
connectAttr "sp_shader22.ocb" "rbfSolver1.ps[21].mv[2]";
connectAttr "pose23.tx" "rbfSolver1.ps[22].nk[0]";
connectAttr "pose23.ty" "rbfSolver1.ps[22].nk[1]";
connectAttr "pose23.tz" "rbfSolver1.ps[22].nk[2]";
connectAttr "sp_shader23.ocr" "rbfSolver1.ps[22].mv[0]";
connectAttr "sp_shader23.ocg" "rbfSolver1.ps[22].mv[1]";
connectAttr "sp_shader23.ocb" "rbfSolver1.ps[22].mv[2]";
connectAttr "pose24.tx" "rbfSolver1.ps[23].nk[0]";
connectAttr "pose24.ty" "rbfSolver1.ps[23].nk[1]";
connectAttr "pose24.tz" "rbfSolver1.ps[23].nk[2]";
connectAttr "sp_shader24.ocr" "rbfSolver1.ps[23].mv[0]";
connectAttr "sp_shader24.ocg" "rbfSolver1.ps[23].mv[1]";
connectAttr "sp_shader24.ocb" "rbfSolver1.ps[23].mv[2]";
connectAttr "pose25.tx" "rbfSolver1.ps[24].nk[0]";
connectAttr "pose25.ty" "rbfSolver1.ps[24].nk[1]";
connectAttr "pose25.tz" "rbfSolver1.ps[24].nk[2]";
connectAttr "sp_shader25.ocr" "rbfSolver1.ps[24].mv[0]";
connectAttr "sp_shader25.ocg" "rbfSolver1.ps[24].mv[1]";
connectAttr "sp_shader25.ocb" "rbfSolver1.ps[24].mv[2]";
connectAttr "pose26.tx" "rbfSolver1.ps[25].nk[0]";
connectAttr "pose26.ty" "rbfSolver1.ps[25].nk[1]";
connectAttr "pose26.tz" "rbfSolver1.ps[25].nk[2]";
connectAttr "sp_shader26.ocr" "rbfSolver1.ps[25].mv[0]";
connectAttr "sp_shader26.ocg" "rbfSolver1.ps[25].mv[1]";
connectAttr "sp_shader26.ocb" "rbfSolver1.ps[25].mv[2]";
connectAttr "pose27.tx" "rbfSolver1.ps[26].nk[0]";
connectAttr "pose27.ty" "rbfSolver1.ps[26].nk[1]";
connectAttr "pose27.tz" "rbfSolver1.ps[26].nk[2]";
connectAttr "sp_shader27.ocr" "rbfSolver1.ps[26].mv[0]";
connectAttr "sp_shader27.ocg" "rbfSolver1.ps[26].mv[1]";
connectAttr "sp_shader27.ocb" "rbfSolver1.ps[26].mv[2]";
connectAttr "pose28.tx" "rbfSolver1.ps[27].nk[0]";
connectAttr "pose28.ty" "rbfSolver1.ps[27].nk[1]";
connectAttr "pose28.tz" "rbfSolver1.ps[27].nk[2]";
connectAttr "sp_shader28.ocr" "rbfSolver1.ps[27].mv[0]";
connectAttr "sp_shader28.ocg" "rbfSolver1.ps[27].mv[1]";
connectAttr "sp_shader28.ocb" "rbfSolver1.ps[27].mv[2]";
connectAttr "pose29.tx" "rbfSolver1.ps[28].nk[0]";
connectAttr "pose29.ty" "rbfSolver1.ps[28].nk[1]";
connectAttr "pose29.tz" "rbfSolver1.ps[28].nk[2]";
connectAttr "sp_shader29.ocr" "rbfSolver1.ps[28].mv[0]";
connectAttr "sp_shader29.ocg" "rbfSolver1.ps[28].mv[1]";
connectAttr "sp_shader29.ocb" "rbfSolver1.ps[28].mv[2]";
connectAttr "pose30.tx" "rbfSolver1.ps[29].nk[0]";
connectAttr "pose30.ty" "rbfSolver1.ps[29].nk[1]";
connectAttr "pose30.tz" "rbfSolver1.ps[29].nk[2]";
connectAttr "sp_shader30.ocr" "rbfSolver1.ps[29].mv[0]";
connectAttr "sp_shader30.ocg" "rbfSolver1.ps[29].mv[1]";
connectAttr "sp_shader30.ocb" "rbfSolver1.ps[29].mv[2]";
connectAttr "pose31.tx" "rbfSolver1.ps[30].nk[0]";
connectAttr "pose31.ty" "rbfSolver1.ps[30].nk[1]";
connectAttr "pose31.tz" "rbfSolver1.ps[30].nk[2]";
connectAttr "sp_shader31.ocr" "rbfSolver1.ps[30].mv[0]";
connectAttr "sp_shader31.ocg" "rbfSolver1.ps[30].mv[1]";
connectAttr "sp_shader31.ocb" "rbfSolver1.ps[30].mv[2]";
connectAttr "pose32.tx" "rbfSolver1.ps[31].nk[0]";
connectAttr "pose32.ty" "rbfSolver1.ps[31].nk[1]";
connectAttr "pose32.tz" "rbfSolver1.ps[31].nk[2]";
connectAttr "sp_shader32.ocr" "rbfSolver1.ps[31].mv[0]";
connectAttr "sp_shader32.ocg" "rbfSolver1.ps[31].mv[1]";
connectAttr "sp_shader32.ocb" "rbfSolver1.ps[31].mv[2]";
connectAttr "pose33.tx" "rbfSolver1.ps[32].nk[0]";
connectAttr "pose33.ty" "rbfSolver1.ps[32].nk[1]";
connectAttr "pose33.tz" "rbfSolver1.ps[32].nk[2]";
connectAttr "sp_shader33.ocr" "rbfSolver1.ps[32].mv[0]";
connectAttr "sp_shader33.ocg" "rbfSolver1.ps[32].mv[1]";
connectAttr "sp_shader33.ocb" "rbfSolver1.ps[32].mv[2]";
connectAttr "pose34.tx" "rbfSolver1.ps[33].nk[0]";
connectAttr "pose34.ty" "rbfSolver1.ps[33].nk[1]";
connectAttr "pose34.tz" "rbfSolver1.ps[33].nk[2]";
connectAttr "sp_shader34.ocr" "rbfSolver1.ps[33].mv[0]";
connectAttr "sp_shader34.ocg" "rbfSolver1.ps[33].mv[1]";
connectAttr "sp_shader34.ocb" "rbfSolver1.ps[33].mv[2]";
connectAttr "pose35.tx" "rbfSolver1.ps[34].nk[0]";
connectAttr "pose35.ty" "rbfSolver1.ps[34].nk[1]";
connectAttr "pose35.tz" "rbfSolver1.ps[34].nk[2]";
connectAttr "sp_shader35.ocr" "rbfSolver1.ps[34].mv[0]";
connectAttr "sp_shader35.ocg" "rbfSolver1.ps[34].mv[1]";
connectAttr "sp_shader35.ocb" "rbfSolver1.ps[34].mv[2]";
connectAttr "pose36.tx" "rbfSolver1.ps[35].nk[0]";
connectAttr "pose36.ty" "rbfSolver1.ps[35].nk[1]";
connectAttr "pose36.tz" "rbfSolver1.ps[35].nk[2]";
connectAttr "sp_shader36.ocr" "rbfSolver1.ps[35].mv[0]";
connectAttr "sp_shader36.ocg" "rbfSolver1.ps[35].mv[1]";
connectAttr "sp_shader36.ocb" "rbfSolver1.ps[35].mv[2]";
connectAttr "pose37.tx" "rbfSolver1.ps[36].nk[0]";
connectAttr "pose37.ty" "rbfSolver1.ps[36].nk[1]";
connectAttr "pose37.tz" "rbfSolver1.ps[36].nk[2]";
connectAttr "sp_shader37.ocr" "rbfSolver1.ps[36].mv[0]";
connectAttr "sp_shader37.ocg" "rbfSolver1.ps[36].mv[1]";
connectAttr "sp_shader37.ocb" "rbfSolver1.ps[36].mv[2]";
connectAttr "pose38.tx" "rbfSolver1.ps[37].nk[0]";
connectAttr "pose38.ty" "rbfSolver1.ps[37].nk[1]";
connectAttr "pose38.tz" "rbfSolver1.ps[37].nk[2]";
connectAttr "sp_shader38.ocr" "rbfSolver1.ps[37].mv[0]";
connectAttr "sp_shader38.ocg" "rbfSolver1.ps[37].mv[1]";
connectAttr "sp_shader38.ocb" "rbfSolver1.ps[37].mv[2]";
connectAttr "pose39.tx" "rbfSolver1.ps[38].nk[0]";
connectAttr "pose39.ty" "rbfSolver1.ps[38].nk[1]";
connectAttr "pose39.tz" "rbfSolver1.ps[38].nk[2]";
connectAttr "sp_shader39.ocr" "rbfSolver1.ps[38].mv[0]";
connectAttr "sp_shader39.ocg" "rbfSolver1.ps[38].mv[1]";
connectAttr "sp_shader39.ocb" "rbfSolver1.ps[38].mv[2]";
connectAttr "pose40.tx" "rbfSolver1.ps[39].nk[0]";
connectAttr "pose40.ty" "rbfSolver1.ps[39].nk[1]";
connectAttr "pose40.tz" "rbfSolver1.ps[39].nk[2]";
connectAttr "sp_shader40.ocr" "rbfSolver1.ps[39].mv[0]";
connectAttr "sp_shader40.ocg" "rbfSolver1.ps[39].mv[1]";
connectAttr "sp_shader40.ocb" "rbfSolver1.ps[39].mv[2]";
connectAttr "pose41.tx" "rbfSolver1.ps[40].nk[0]";
connectAttr "pose41.ty" "rbfSolver1.ps[40].nk[1]";
connectAttr "pose41.tz" "rbfSolver1.ps[40].nk[2]";
connectAttr "sp_shader41.ocr" "rbfSolver1.ps[40].mv[0]";
connectAttr "sp_shader41.ocg" "rbfSolver1.ps[40].mv[1]";
connectAttr "sp_shader41.ocb" "rbfSolver1.ps[40].mv[2]";
connectAttr "pose42.tx" "rbfSolver1.ps[41].nk[0]";
connectAttr "pose42.ty" "rbfSolver1.ps[41].nk[1]";
connectAttr "pose42.tz" "rbfSolver1.ps[41].nk[2]";
connectAttr "sp_shader42.ocr" "rbfSolver1.ps[41].mv[0]";
connectAttr "sp_shader42.ocg" "rbfSolver1.ps[41].mv[1]";
connectAttr "sp_shader42.ocb" "rbfSolver1.ps[41].mv[2]";
connectAttr "pose43.tx" "rbfSolver1.ps[42].nk[0]";
connectAttr "pose43.ty" "rbfSolver1.ps[42].nk[1]";
connectAttr "pose43.tz" "rbfSolver1.ps[42].nk[2]";
connectAttr "sp_shader43.ocr" "rbfSolver1.ps[42].mv[0]";
connectAttr "sp_shader43.ocg" "rbfSolver1.ps[42].mv[1]";
connectAttr "sp_shader43.ocb" "rbfSolver1.ps[42].mv[2]";
connectAttr "pose44.tx" "rbfSolver1.ps[43].nk[0]";
connectAttr "pose44.ty" "rbfSolver1.ps[43].nk[1]";
connectAttr "pose44.tz" "rbfSolver1.ps[43].nk[2]";
connectAttr "sp_shader44.ocr" "rbfSolver1.ps[43].mv[0]";
connectAttr "sp_shader44.ocg" "rbfSolver1.ps[43].mv[1]";
connectAttr "sp_shader44.ocb" "rbfSolver1.ps[43].mv[2]";
connectAttr "pose45.tx" "rbfSolver1.ps[44].nk[0]";
connectAttr "pose45.ty" "rbfSolver1.ps[44].nk[1]";
connectAttr "pose45.tz" "rbfSolver1.ps[44].nk[2]";
connectAttr "sp_shader45.ocr" "rbfSolver1.ps[44].mv[0]";
connectAttr "sp_shader45.ocg" "rbfSolver1.ps[44].mv[1]";
connectAttr "sp_shader45.ocb" "rbfSolver1.ps[44].mv[2]";
connectAttr "pose46.tx" "rbfSolver1.ps[45].nk[0]";
connectAttr "pose46.ty" "rbfSolver1.ps[45].nk[1]";
connectAttr "pose46.tz" "rbfSolver1.ps[45].nk[2]";
connectAttr "sp_shader46.ocr" "rbfSolver1.ps[45].mv[0]";
connectAttr "sp_shader46.ocg" "rbfSolver1.ps[45].mv[1]";
connectAttr "sp_shader46.ocb" "rbfSolver1.ps[45].mv[2]";
connectAttr "pose47.tx" "rbfSolver1.ps[46].nk[0]";
connectAttr "pose47.ty" "rbfSolver1.ps[46].nk[1]";
connectAttr "pose47.tz" "rbfSolver1.ps[46].nk[2]";
connectAttr "sp_shader47.ocr" "rbfSolver1.ps[46].mv[0]";
connectAttr "sp_shader47.ocg" "rbfSolver1.ps[46].mv[1]";
connectAttr "sp_shader47.ocb" "rbfSolver1.ps[46].mv[2]";
connectAttr "pose48.tx" "rbfSolver1.ps[47].nk[0]";
connectAttr "pose48.ty" "rbfSolver1.ps[47].nk[1]";
connectAttr "pose48.tz" "rbfSolver1.ps[47].nk[2]";
connectAttr "sp_shader48.ocr" "rbfSolver1.ps[47].mv[0]";
connectAttr "sp_shader48.ocg" "rbfSolver1.ps[47].mv[1]";
connectAttr "sp_shader48.ocb" "rbfSolver1.ps[47].mv[2]";
connectAttr "pose49.tx" "rbfSolver1.ps[48].nk[0]";
connectAttr "pose49.ty" "rbfSolver1.ps[48].nk[1]";
connectAttr "pose49.tz" "rbfSolver1.ps[48].nk[2]";
connectAttr "sp_shader49.ocr" "rbfSolver1.ps[48].mv[0]";
connectAttr "sp_shader49.ocg" "rbfSolver1.ps[48].mv[1]";
connectAttr "sp_shader49.ocb" "rbfSolver1.ps[48].mv[2]";
connectAttr "pose50.tx" "rbfSolver1.ps[49].nk[0]";
connectAttr "pose50.ty" "rbfSolver1.ps[49].nk[1]";
connectAttr "pose50.tz" "rbfSolver1.ps[49].nk[2]";
connectAttr "sp_shader50.ocr" "rbfSolver1.ps[49].mv[0]";
connectAttr "sp_shader50.ocg" "rbfSolver1.ps[49].mv[1]";
connectAttr "sp_shader50.ocb" "rbfSolver1.ps[49].mv[2]";
connectAttr "rotate_me.m" "vectorProduct1.m";
connectAttr "hyperView1.msg" "nodeEditorPanel1Info.b[0]";
connectAttr "hyperLayout1.msg" "hyperView1.hl";
connectAttr "vectorProduct1.msg" "hyperLayout1.hyp[0].dn";
connectAttr "surfaceShader1SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader1SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader2SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader3SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader4SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader5SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader6SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader7SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader8SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader9SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader10SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader11SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader12SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader13SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader14SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader15SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader16SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader17SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader18SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader19SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader20SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader21SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader22SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader23SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader24SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader25SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader26SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader27SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader28SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader29SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader30SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader31SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader32SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader33SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader34SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader35SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader36SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader37SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader38SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader39SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader40SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader41SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader42SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader43SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader44SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader45SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader46SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader47SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader48SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader49SG.pa" ":renderPartition.st" -na;
connectAttr "sp_shader50SG.pa" ":renderPartition.st" -na;
connectAttr "blinn1SG.pa" ":renderPartition.st" -na;
connectAttr "outShader.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader1.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader2.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader3.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader4.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader5.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader6.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader7.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader8.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader9.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader10.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader11.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader12.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader13.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader14.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader15.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader16.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader17.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader18.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader19.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader20.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader21.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader22.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader23.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader24.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader25.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader26.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader27.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader28.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader29.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader30.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader31.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader32.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader33.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader34.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader35.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader36.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader37.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader38.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader39.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader40.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader41.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader42.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader43.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader44.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader45.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader46.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader47.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader48.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader49.msg" ":defaultShaderList1.s" -na;
connectAttr "sp_shader50.msg" ":defaultShaderList1.s" -na;
connectAttr "blinn1.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of sample_scene.ma
