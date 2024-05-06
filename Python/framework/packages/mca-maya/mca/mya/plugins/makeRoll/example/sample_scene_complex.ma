//Maya ASCII 2015ff05 scene
//Name: sample_scene_complex.ma
//Last modified: Fri, Mar 20, 2015 04:56:37 PM
//Codeset: 1252
requires maya "2015ff05";
requires -nodeType "makeRoll" "makeRoll.py" "1.0";
requires -nodeType "decomposeMatrix" "matrixNodes" "1.0";
requires "QDMayaTools" "6.0.10 SP4 1015";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201501210954-000000-1";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
fileInfo "RNLoadStates" "{}";
fileInfo "outsourceData" "(dp1\nS'format'\np2\nF1\nsS'misc'\np3\n(lp4\nsS'actors'\np5\n(lp6\nsS'shaders'\np7\n(lp8\nsS'references'\np9\n(lp10\nsS'audio'\np11\n(lp12\ns.";
createNode transform -s -n "persp";
	rename -uid "C4C7D143-4ADD-86FC-E083-7286FE66F559";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 2.3981527759687067 11.531669564017058 17.099412979274593 ;
	setAttr ".r" -type "double3" -373.86405991912613 359.39956155005359 1439.9999986420685 ;
	setAttr ".rpt" -type "double3" -2.6666689048390228e-013 -1.8098630676143029e-012 
		2.2545442340875369e-012 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "39537A92-462C-2A84-C892-46B03102044C";
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
	setAttr ".coi" 19.186424975020188;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -1.2636233866660191 4.4521963796016273 4.8785314693745576 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "CD178C9C-4AA1-E1DF-2310-27A83205CF13";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999972 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "8FBFC754-4C56-17AC-BA57-40BF01A62206";
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
	rename -uid "C07B9ED6-4B28-E5A4-E3CF-A6940C45D5F8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "4D266815-41E9-B6DF-FC89-25A14E282FCD";
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
	rename -uid "635FB066-4FBC-D0FD-EF00-C0BD132DAC01";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999972 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3999F92A-42C0-4509-F191-DB9AC65557BE";
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
createNode transform -n "group1";
	rename -uid "DE5BD94E-4D61-984D-31B2-91A78ED8BEC5";
	setAttr ".t" -type "double3" 0 6.8261316970545902 0 ;
createNode transform -n "move_me" -p "group1";
	rename -uid "04823609-458F-1102-D355-74B269FC75AD";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	setAttr ".t" -type "double3" 5 0 0 ;
	setAttr ".qdGuid" -type "string" "31104496-2aa2-4294-883c-47bd96d6b8e6";
createNode locator -n "move_meShape" -p "move_me";
	rename -uid "88D8552C-45F1-9384-4538-18984D36034A";
	addAttr -ci true -sn "QDAP" -ln "QDAnimPivot" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "QDCN" -ln "QDCompensationNode" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".los" -type "double3" 1.3 1.3 1.3 ;
	setAttr ".qdGuid" -type "string" "5c8c0caa-105c-406d-9e94-ca52a85ebb7f";
createNode transform -n "visu1" -p "group1";
	rename -uid "8AD386CD-4EFD-C15C-8C12-4CBF4C5BB5B4";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	addAttr -ci true -sn "manipInfo" -ln "manipInfo" -min 0 -max 0 -en " " -at "enum";
	setAttr ".qdGuid" -type "string" "47d96d8f-a184-4874-87ed-fd32d4a0a3fe";
createNode nurbsSurface -n "visuShape1" -p "visu1";
	rename -uid "CE42784F-48DD-BA2A-1C21-A4B0B3CE4709";
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
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		4.4408920985006262e-016 -1.870916604310092 -8.8817841970012523e-016
		0.37402764345615691 -1.870916604310092 -0.37402764345615758
		0.52895496607814596 -1.870916604310092 0
		0.37402764345615713 -1.870916604310092 0.37402764345615669
		4.4408920985006262e-016 -1.870916604310092 0.52895496607814518
		-0.37402764345615647 -1.870916604310092 0.37402764345615669
		-0.52895496607814541 -1.870916604310092 0
		-0.37402764345615691 -1.870916604310092 -0.37402764345615669
		-1.1102230246251565e-016 -1.870916604310092 -0.52895496607814563
		0.37402764345615691 -1.870916604310092 -0.37402764345615758
		0.52895496607814596 -1.870916604310092 0
		0.37402764345615713 -1.870916604310092 0.37402764345615669
		1.1532890843976549 -1.4660720003394037 -1.1532890843976564
		1.6309970644920138 -1.4660720003394037 0
		1.1532890843976555 -1.4660720003394037 1.1532890843976551
		5.5511151231257827e-016 -1.4660720003394037 1.6309970644920133
		-1.1532890843976549 -1.4660720003394037 1.153289084397656
		-1.6309970644920131 -1.4660720003394037 0
		-1.1532890843976549 -1.4660720003394037 -1.1532890843976547
		-5.5511151231257827e-016 -1.4660720003394037 -1.6309970644920133
		1.1532890843976549 -1.4660720003394037 -1.1532890843976564
		1.6309970644920138 -1.4660720003394037 0
		1.1532890843976555 -1.4660720003394037 1.1532890843976551
		1.6224634583102739 -1.7763568394002505e-015 -1.6224634583102757
		2.2945098271971451 -1.7763568394002505e-015 8.8817841970012523e-016
		1.6224634583102746 -1.7763568394002505e-015 1.6224634583102748
		5.5511151231257827e-016 -1.7763568394002505e-015 2.2945098271971451
		-1.6224634583102742 -1.7763568394002505e-015 1.6224634583102748
		-2.2945098271971451 -1.7763568394002505e-015 0
		-1.6224634583102746 -1.7763568394002505e-015 -1.6224634583102739
		-7.7715611723760958e-016 -1.7763568394002505e-015 -2.2945098271971451
		1.6224634583102739 -1.7763568394002505e-015 -1.6224634583102757
		2.2945098271971451 -1.7763568394002505e-015 8.8817841970012523e-016
		1.6224634583102746 -1.7763568394002505e-015 1.6224634583102748
		1.1532890843976555 1.4660720003394001 -1.1532890843976564
		1.6309970644920142 1.4660720003394001 8.8817841970012523e-016
		1.1532890843976555 1.4660720003394001 1.153289084397656
		4.4408920985006262e-016 1.4660720003394001 1.6309970644920142
		-1.1532890843976549 1.4660720003394001 1.153289084397656
		-1.630997064492014 1.4660720003394001 0
		-1.1532890843976558 1.4660720003394001 -1.1532890843976551
		-3.3306690738754696e-016 1.4660720003394001 -1.6309970644920142
		1.1532890843976555 1.4660720003394001 -1.1532890843976564
		1.6309970644920142 1.4660720003394001 8.8817841970012523e-016
		1.1532890843976555 1.4660720003394001 1.153289084397656
		0.37402764345615735 1.8709166043100875 -0.37402764345615713
		0.52895496607814607 1.8709166043100875 0
		0.37402764345615713 1.8709166043100875 0.37402764345615758
		2.2204460492503131e-016 1.8709166043100875 0.52895496607814607
		-0.37402764345615691 1.8709166043100875 0.37402764345615758
		-0.52895496607814585 1.8709166043100875 0
		-0.37402764345615691 1.8709166043100875 -0.37402764345615713
		1.1102230246251565e-016 1.8709166043100875 -0.52895496607814563
		0.37402764345615735 1.8709166043100875 -0.37402764345615713
		0.52895496607814607 1.8709166043100875 0
		0.37402764345615713 1.8709166043100875 0.37402764345615758
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		5.5511151231257827e-016 1.8709166043100875 0
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
	setAttr ".qdGuid" -type "string" "dc6f3a14-f01b-4c1b-8cf3-e29c31a7d9e8";
createNode transform -n "get_translate" -p "group1";
	rename -uid "DBA135FC-4D4B-23B3-6419-91880CB3AC2F";
	setAttr ".v" no;
createNode nurbsSurface -n "offsetShape" -p "get_translate";
	rename -uid "1798CA68-454F-FB86-D39A-C48D724F0F4D";
	addAttr -ci true -h true -sn "qdGuid" -ln "qdGuid" -dt "string";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".dor" yes;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		-1.9984014443252818e-015 -2.9709166281519499 -8.8817841970012523e-016
		0.59023991896309691 -2.9275643962882469 -0.59023991896309891
		0.83472529845161492 -2.9275643962882452 0
		0.59023991896309691 -2.9275643962882469 0.59023991896309536
		6.6613381477509392e-016 -2.9275643983291966 0.83472529139871554
		-0.59023991896309735 -2.9275643962882469 0.59023991896309624
		-0.83472529845160759 -2.9275643962882469 0
		-0.5902399189630978 -2.9275643962882469 -0.59023991896309669
		-8.8817841970012523e-016 -2.9275643983291983 -0.83472529139871021
		0.59023991896309691 -2.9275643962882469 -0.59023991896309891
		0.83472529845161492 -2.9275643962882452 0
		0.59023991896309691 -2.9275643962882469 0.59023991896309536
		1.731359970111404 -2.202053083406307 -1.7313599701114053
		2.4485127510814242 -2.2020530834063079 0
		1.7313599701114046 -2.202053083406307 1.731359970111404
		7.7715611723760958e-016 -2.2020530834063061 2.4485127510814255
		-1.7313599701114053 -2.2020530834063052 1.7313599701114049
		-2.448512751081422 -2.2020530834063088 0
		-1.7313599701114031 -2.202053083406307 -1.7313599701114031
		-1.3322676295501878e-015 -2.202053083406307 -2.4485127510814242
		1.731359970111404 -2.202053083406307 -1.7313599701114053
		2.4485127510814242 -2.2020530834063079 0
		1.7313599701114046 -2.202053083406307 1.731359970111404
		2.4002809344742158 -1.7763568394002505e-015 -2.4002809344742175
		3.3945098510390035 -1.7763568394002505e-015 8.8817841970012523e-016
		2.4002809344742166 -1.7763568394002505e-015 2.4002809344742166
		7.7715611723760958e-016 -1.7763568394002505e-015 3.394509851039003
		-2.4002809344742153 -1.7763568394002505e-015 2.4002809344742166
		-3.3945098510390035 -3.5527136788005009e-015 8.8817841970012523e-016
		-2.4002809344742162 -1.7763568394002505e-015 -2.4002809344742158
		-1.5543122344752192e-015 -1.7763568394002505e-015 -3.394509851039003
		2.4002809344742158 -1.7763568394002505e-015 -2.4002809344742175
		3.3945098510390035 -1.7763568394002505e-015 8.8817841970012523e-016
		2.4002809344742166 -1.7763568394002505e-015 2.4002809344742166
		1.7313599701114062 2.2020530834063017 -1.7313599701114057
		2.4485127502111417 2.2020530843730004 8.8817841970012523e-016
		1.7313599694960233 2.2020530843729968 1.7313599694960242
		6.6613381477509392e-016 2.2020530843730022 2.4485127502111403
		-1.7313599694960176 2.2020530843730022 1.7313599694960216
		-2.4485127502111417 2.2020530843729986 0
		-1.7313599694960193 2.2020530843730022 -1.7313599694960198
		-1.1102230246251565e-015 2.2020530834063035 -2.4485127510814251
		1.7313599701114062 2.2020530834063017 -1.7313599701114057
		2.4485127502111417 2.2020530843730004 8.8817841970012523e-016
		1.7313599694960233 2.2020530843729968 1.7313599694960242
		0.59023991397595177 2.9275643983291921 -0.59023991397595088
		0.83472529845160337 2.9275643962882434 0
		0.59023991896309802 2.9275643962882434 0.59023991896309536
		4.4408920985006262e-016 2.9275643962882416 0.83472529845160981
		-0.59023991896310202 2.9275643962882416 0.59023991896310068
		-0.8347252984516087 2.9275643962882416 0
		-0.59023991896309647 2.9275643962882416 -0.59023991896309802
		3.3306690738754696e-016 2.9275643962882452 -0.83472529845160226
		0.59023991397595177 2.9275643983291921 -0.59023991397595088
		0.83472529845160337 2.9275643962882434 0
		0.59023991896309802 2.9275643962882434 0.59023991896309536
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		7.7715611723760958e-016 2.9709166281519455 0
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
	setAttr ".qdGuid" -type "string" "ca3d6ff5-f0e6-4dfa-9e74-17e8eef51468";
createNode transform -n "roll_sphere" -p "group1";
	rename -uid "2A4FB313-4D95-8F2A-DFD5-64A816AA1373";
	addAttr -ci true -sn "manipInfo" -ln "manipInfo" -min 0 -max 0 -en " " -at "enum";
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999967 0.99999999999999978 ;
	setAttr ".rp" -type "double3" 2.2204460492503126e-016 0 2.7755575615628907e-017 ;
	setAttr ".rpt" -type "double3" -1.6146621974270451e-016 5.1999876010894877e-017 
		1.8129095197481283e-016 ;
	setAttr ".sp" -type "double3" 2.2204460492503131e-016 0 2.7755575615628914e-017 ;
	setAttr ".spt" -type "double3" -4.9303806576313227e-032 0 -6.1629758220391534e-033 ;
createNode nurbsSurface -n "rollShape" -p "roll_sphere";
	rename -uid "4A50EF3B-4D32-B29A-FE28-04AD32CEDC78";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 16 "sf[0][1]" "sf[0][3]" "sf[0][5]" "sf[0][7]" "sf[1][1]" "sf[1][3]" "sf[1][5]" "sf[1][7]" "sf[2][1]" "sf[2][3]" "sf[2][5]" "sf[2][7]" "sf[3][1]" "sf[3][3]" "sf[3][5]" "sf[3][7]";
	setAttr ".iog[0].og[1].gcl" -type "componentList" 10 "sf[0:3][0]" "sf[0:3][4]" "sf[0][2]" "sf[0][6]" "sf[1][2]" "sf[1][6]" "sf[2][2]" "sf[2][6]" "sf[3][2]" "sf[3][6]";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 3;
	setAttr ".dvv" 3;
	setAttr ".cpr" 15;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 -1.2607985810526205e-016 -2.5316183359690667e-016
		1.0000000000000002 0.19991679083637237 -0.19991679083637304
		1.0000000000000002 0.28272503694690343 -6.2210285873682239e-017
		1.0000000000000002 0.19991679083637254 0.19991679083637265
		1.0000000000000002 -1.0688447036224683e-016 0.2827250369469036
		1.0000000000000002 -0.19991679083637287 0.19991679083637279
		1.0000000000000002 -0.28272503694690393 5.7191723447539767e-017
		1.0000000000000002 -0.19991679083637304 -0.19991679083637265
		1.0000000000000002 -4.0713026586821225e-016 -0.28272503694690371
		1.0000000000000002 0.19991679083637237 -0.19991679083637304
		1.0000000000000002 0.28272503694690343 -6.2210285873682239e-017
		1.0000000000000002 0.19991679083637254 0.19991679083637265
		0.7836116248912246 0.61642997969058888 -0.6164299796905901
		0.78361162489122471 0.87176363753180319 1.0506190143399391e-016
		0.7836116248912246 0.61642997969058921 0.61642997969058944
		0.78361162489122449 2.5032091175141491e-017 0.87176363753180341
		0.78361162489122438 -0.61642997969058955 0.61642997969058966
		0.78361162489122427 -0.87176363753180375 1.6111055650702838e-016
		0.78361162489122438 -0.61642997969058977 -0.6164299796905891
		0.78361162489122449 -5.8863621644760022e-016 -0.87176363753180341
		0.7836116248912246 0.61642997969058888 -0.6164299796905901
		0.78361162489122471 0.87176363753180319 1.0506190143399391e-016
		0.7836116248912246 0.61642997969058921 0.61642997969058944
		1.2720371521314997e-016 0.86720244749154152 -0.86720244749154274
		2.6006453003825034e-016 1.2264094625656805 2.9011049772987885e-016
		2.3340538536647684e-016 0.86720244749154185 0.86720244749154207
		6.2842846585288201e-017 2.0519093763181872e-016 1.2264094625656805
		-1.5170986432008239e-016 -0.86720244749154185 0.86720244749154207
		-2.8457067914518271e-016 -1.2264094625656807 2.1934926354574317e-016
		-2.5791153447340917e-016 -0.86720244749154196 -0.86720244749154152
		-8.7348995692220601e-017 -5.0851507246572649e-016 -1.2264094625656805
		1.2720371521314997e-016 0.86720244749154152 -0.86720244749154274
		2.6006453003825034e-016 1.2264094625656805 2.9011049772987885e-016
		2.3340538536647684e-016 0.86720244749154185 0.86720244749154207
		-0.7836116248912246 0.61642997969058966 -0.6164299796905901
		-0.78361162489122449 0.87176363753180386 3.073742228895604e-016
		-0.7836116248912246 0.61642997969058977 0.61642997969058977
		-0.78361162489122471 2.6667798386661217e-016 0.87176363753180364
		-0.78361162489122482 -0.61642997969058932 0.61642997969058977
		-0.78361162489122493 -0.87176363753180353 1.5072772869100092e-016
		-0.78361162489122482 -0.61642997969058944 -0.61642997969058944
		-0.78361162489122471 -1.3429517448453574e-016 -0.87176363753180364
		-0.7836116248912246 0.61642997969058966 -0.6164299796905901
		-0.78361162489122449 0.87176363753180386 3.073742228895604e-016
		-0.7836116248912246 0.61642997969058977 0.61642997969058977
		-1 0.19991679083637304 -0.1999167908363729
		-0.99999999999999989 0.28272503694690398 1.9596904050327142e-016
		-1 0.19991679083637298 0.19991679083637298
		-1 2.0149009302559754e-016 0.28272503694690382
		-1 -0.19991679083637265 0.19991679083637287
		-1 -0.2827250369469036 4.3941756900056808e-017
		-1 -0.19991679083637257 -0.19991679083637276
		-1 1.7267359044406873e-016 -0.28272503694690371
		-1 0.19991679083637304 -0.1999167908363729
		-0.99999999999999989 0.28272503694690398 1.9596904050327142e-016
		-1 0.19991679083637298 0.19991679083637298
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		-1.0000000000000002 3.960413385886651e-016 -1.6799646886496762e-017
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "0C804498-4BC7-B6AD-7895-8EB51E05E50A";
	setAttr -s 6 ".lnk";
	setAttr -s 6 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "152C642C-44EE-E40C-EB52-4E8B803D08F1";
createNode displayLayer -n "defaultLayer";
	rename -uid "8F0DCBAC-4517-D82B-65B0-1185D7AA351A";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "791F354B-4384-1518-4B28-BFB74642E1BE";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "4CE67522-4316-9638-9110-26A890714BC2";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "06F587CF-47D0-A75C-4D2D-E2BC9938CD37";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n"
		+ "            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n"
		+ "            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n"
		+ "                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n"
		+ "                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n"
		+ "            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n"
		+ "            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n"
		+ "                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n"
		+ "                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n"
		+ "                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 1\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n"
		+ "                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n"
		+ "                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n"
		+ "                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n"
		+ "            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n"
		+ "            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n"
		+ "                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n"
		+ "                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n"
		+ "            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n"
		+ "                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n"
		+ "                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n"
		+ "                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n"
		+ "                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n"
		+ "                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n"
		+ "                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n"
		+ "            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n"
		+ "                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n"
		+ "                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n"
		+ "                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Texture Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n"
		+ "\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n"
		+ "                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n"
		+ "                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n"
		+ "                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n"
		+ "            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"right3\\\" -ps 1 26 100 -ps 2 74 64 -ps 3 74 36 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Hypershade\")) \n\t\t\t\t\t\"scriptedPanel\"\n\t\t\t\t\t\"$panelName = `scriptedPanel -unParent  -type \\\"hyperShadePanel\\\" -l (localizedPanelLabel(\\\"Hypershade\\\")) -mbv $menusOkayInPanels `\"\n\t\t\t\t\t\"scriptedPanel -edit -l (localizedPanelLabel(\\\"Hypershade\\\")) -mbv $menusOkayInPanels  $panelName\"\n\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "9CD3914D-4981-2690-5EE3-2DB254DACD36";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 375 -ast 1 -aet 375 ";
	setAttr ".st" 6;
createNode blinn -n "blinn1";
	rename -uid "597B6E01-4166-06EB-93AF-0780563D3101";
	setAttr ".c" -type "float3" 1 1 1 ;
	setAttr ".sc" -type "float3" 0.10568398 0.10568398 0.10568398 ;
	setAttr ".ec" 0.089421950280666351;
	setAttr ".sro" 0.79674798250198364;
createNode shadingEngine -n "blinn1SG";
	rename -uid "6E881E28-44ED-336A-3F89-9A91F9C93EB8";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 2 ".gn";
createNode materialInfo -n "materialInfo1";
	rename -uid "4155AFC0-4C3E-3D5D-DE01-00A08A1526A7";
createNode blinn -n "blinn2";
	rename -uid "DE36CFDD-4C24-4277-F6A4-C7A6DD2393D3";
	setAttr ".c" -type "float3" 0.611 0.101 0.5 ;
createNode shadingEngine -n "blinn2SG";
	rename -uid "560CDCC5-4E4C-AF26-9BE4-17BEA2FC6DE2";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo2";
	rename -uid "FC5B473B-4224-3F7B-CBF7-01A5E4623916";
createNode lambert -n "lambert2";
	rename -uid "686B612E-40D6-8F02-61A5-4985D31D01B4";
createNode shadingEngine -n "lambert2SG";
	rename -uid "9CD62225-415D-A912-DFA2-55950B75380D";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo3";
	rename -uid "369D96C0-4ABB-7CD1-4F9D-37AF71D3F03C";
createNode animLayer -s -n "BaseAnimation";
	rename -uid "8E3949F6-4CAC-EDA4-FCD4-97908E8F493D";
	setAttr ".pref" yes;
	setAttr ".slct" yes;
	setAttr ".ovrd" yes;
createNode lambert -n "lambert3";
	rename -uid "97D56B83-4587-50EC-ED67-E485FEFCB8B1";
	setAttr ".it" -type "float3" 0.66666669 0.66666669 0.66666669 ;
createNode shadingEngine -n "lambert3SG";
	rename -uid "2E9D9F79-486A-8186-53E2-14A31C0E54A6";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo4";
	rename -uid "E822D6D4-40E5-C22D-16BA-FEA954FA28D7";
createNode closestPointOnSurface -n "closestPointOnSurface1";
	rename -uid "EDE6D5DC-4DE4-2552-4663-AA9ECD4185D5";
createNode pointMatrixMult -n "pointMatrixMult1";
	rename -uid "D19715FF-430C-8CC7-F703-EFAF5EEBF9DE";
createNode makeRoll -n "makeRoll1";
	rename -uid "CA9AF3A1-4446-32C0-FA66-9C8F64659366";
createNode pointOnSurfaceInfo -n "pointOnSurfaceInfo1";
	rename -uid "6D1D9051-492A-C874-9490-229E23680CA0";
createNode groupId -n "groupId2";
	rename -uid "7CD95FDB-4F25-63EE-EADF-4B9BB1B616AB";
	setAttr ".ihi" 0;
createNode vectorProduct -n "vectorProduct1";
	rename -uid "295A38EF-45FA-3817-7CAA-E18CB031630B";
	setAttr ".op" 3;
	setAttr ".no" yes;
createNode vectorProduct -n "vectorProduct2";
	rename -uid "277D0957-4157-CA81-7773-47AA42916E06";
	setAttr ".op" 4;
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "68CE26EB-48F5-35F4-8B0F-5F88A6DB911A";
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
createNode multMatrix -n "multMatrix1";
	rename -uid "99B436EA-4022-10D8-3410-52806025F180";
	setAttr -s 2 ".i";
createNode vectorProduct -n "vectorProduct3";
	rename -uid "BF5E263A-4CF7-DB56-81CF-8AB85924B416";
	setAttr ".op" 4;
	setAttr ".no" yes;
createNode multMatrix -n "multMatrix2";
	rename -uid "F6E60A2A-4433-056C-8F28-5692178CBF88";
	setAttr -s 2 ".i";
createNode groupId -n "groupId3";
	rename -uid "EEC0358D-4284-7E5F-7832-B6A01C0E6D63";
	setAttr ".ihi" 0;
createNode groupId -n "groupId4";
	rename -uid "68A02A08-49B2-E972-6070-80875974255B";
	setAttr ".ihi" 0;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".st";
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
	setAttr -s 6 ".s";
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
select -ne :initialParticleSE;
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
select -ne :defaultRenderGlobals;
	setAttr ".ep" 1;
select -ne :defaultResolution;
	setAttr ".w" 640;
	setAttr ".h" 480;
	setAttr ".dar" 1.3333332538604736;
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultObjectSet;
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
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
select -ne :hardwareRenderingGlobals;
	setAttr ".vac" 2;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
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
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
connectAttr "decomposeMatrix1.or" "roll_sphere.r";
connectAttr "vectorProduct3.o" "roll_sphere.t";
connectAttr "blinn1SG.mwc" "rollShape.iog.og[0].gco";
connectAttr "groupId3.id" "rollShape.iog.og[0].gid";
connectAttr "blinn2SG.mwc" "rollShape.iog.og[1].gco";
connectAttr "groupId4.id" "rollShape.iog.og[1].gid";
connectAttr "groupId2.id" "rollShape.ciog.cog[0].cgid";
relationship "link" ":lightLinker1" "blinn1SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "blinn2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert3SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "blinn1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "blinn2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert3SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "blinn1.oc" "blinn1SG.ss";
connectAttr "rollShape.ciog.cog[0]" "blinn1SG.dsm" -na;
connectAttr "rollShape.iog.og[0]" "blinn1SG.dsm" -na;
connectAttr "groupId2.msg" "blinn1SG.gn" -na;
connectAttr "groupId3.msg" "blinn1SG.gn" -na;
connectAttr "blinn1SG.msg" "materialInfo1.sg";
connectAttr "blinn1.msg" "materialInfo1.m";
connectAttr "blinn2.oc" "blinn2SG.ss";
connectAttr "groupId4.msg" "blinn2SG.gn" -na;
connectAttr "rollShape.iog.og[1]" "blinn2SG.dsm" -na;
connectAttr "blinn2SG.msg" "materialInfo2.sg";
connectAttr "blinn2.msg" "materialInfo2.m";
connectAttr "lambert2.oc" "lambert2SG.ss";
connectAttr "visuShape1.iog" "lambert2SG.dsm" -na;
connectAttr "lambert2SG.msg" "materialInfo3.sg";
connectAttr "lambert2.msg" "materialInfo3.m";
connectAttr "lambert3.oc" "lambert3SG.ss";
connectAttr "offsetShape.iog" "lambert3SG.dsm" -na;
connectAttr "lambert3SG.msg" "materialInfo4.sg";
connectAttr "lambert3.msg" "materialInfo4.m";
connectAttr "pointMatrixMult1.o" "closestPointOnSurface1.ip";
connectAttr "offsetShape.ws" "closestPointOnSurface1.is";
connectAttr "move_me.wm" "pointMatrixMult1.im";
connectAttr ":time1.o" "makeRoll1.t";
connectAttr "vectorProduct2.o" "makeRoll1.it";
connectAttr "visu1.wm" "makeRoll1.rm";
connectAttr "vectorProduct1.o" "makeRoll1.uv";
connectAttr "offsetShape.ws" "pointOnSurfaceInfo1.is";
connectAttr "closestPointOnSurface1.u" "pointOnSurfaceInfo1.u";
connectAttr "closestPointOnSurface1.v" "pointOnSurfaceInfo1.v";
connectAttr "visu1.wim" "vectorProduct1.m";
connectAttr "pointOnSurfaceInfo1.nn" "vectorProduct1.i1";
connectAttr "visu1.wim" "vectorProduct2.m";
connectAttr "closestPointOnSurface1.p" "vectorProduct2.i1";
connectAttr "multMatrix2.o" "decomposeMatrix1.imat";
connectAttr "visu1.wm" "multMatrix1.i[0]";
connectAttr "makeRoll1.om" "multMatrix1.i[1]";
connectAttr "roll_sphere.pim" "vectorProduct3.m";
connectAttr "closestPointOnSurface1.p" "vectorProduct3.i1";
connectAttr "multMatrix1.o" "multMatrix2.i[0]";
connectAttr "roll_sphere.pim" "multMatrix2.i[1]";
connectAttr "blinn1SG.pa" ":renderPartition.st" -na;
connectAttr "blinn2SG.pa" ":renderPartition.st" -na;
connectAttr "lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "lambert3SG.pa" ":renderPartition.st" -na;
connectAttr "blinn1.msg" ":defaultShaderList1.s" -na;
connectAttr "blinn2.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert2.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert3.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of sample_scene_complex.ma
