//Maya ASCII 2015ff05 scene
//Name: dynamicChain_and_dynamicTime.ma
//Last modified: Wed, Aug 12, 2015 01:07:24 PM
//Codeset: 1252
requires maya "2015ff05";
requires -nodeType "dynamicChain" "dynamicChain.py" "3.0";
requires -nodeType "dynamicTime" "dynamicTime.py" "1.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201504171404-000000-1";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
fileInfo "outsourceData" "(dp1\nS'format'\np2\nF1\nsS'misc'\np3\n(lp4\nsS'actors'\np5\n(lp6\nsS'shaders'\np7\n(lp8\nsS'references'\np9\n(lp10\nsS'audio'\np11\n(lp12\ns.";
fileInfo "scene-info" "{\"project\": \"big4\", \"version\": 1.4, \"references\": [], \"user\": \"hgodard\", \"audio\": [], \"scene\": \"C:/Users/hgodard/Desktop/NEW/dynamicChain/dynamicChain_and_dynamicTime.ma\", \"refnodes\": [], \"shaders\": []}";
fileInfo "RNLoadStates" "{}";
createNode transform -s -n "persp";
	rename -uid "EF83A4B7-4E43-D12D-C253-18AB52DC1E6A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.796856455221163 8.3891646288458119 4.0404242170180851 ;
	setAttr ".r" -type "double3" -53.538352729602792 9.4000000000000856 8.0596098421297932e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "76FE8AB0-4E96-0915-D25C-3F80DCCDDFAD";
	setAttr -k off ".v" no;
	setAttr ".cap" -type "double2" 1 1 ;
	setAttr ".fl" 16.551;
	setAttr ".coi" 9.6112904349909201;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "6D433D50-4B95-310F-5FEA-4490837A79EF";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "142DEC2A-4A8A-A4BA-62E7-7595529F3192";
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
	rename -uid "BC955F12-444F-10C9-CD3E-7797BDF83218";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "49CD3500-47CD-CE45-78AF-4C908B114F12";
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
	rename -uid "2EB32163-48F6-08E5-498A-229899157237";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "BFEFA3DF-4CE3-03B1-D029-05AE87731D4C";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "joint1";
	rename -uid "56387982-41D1-197A-803D-EA905013F745";
	setAttr ".t" -type "double3" 2 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 89.999999999999986 0 ;
createNode joint -n "joint2" -p "joint1";
	rename -uid "06D4AD8E-4E7A-D2CE-92B6-2DA0FBF4C9B9";
	setAttr ".t" -type "double3" 1.9999999999999996 0 -4.4408920985006242e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -45.000000000000007 0 ;
createNode joint -n "joint3" -p "joint2";
	rename -uid "A457C2FB-431E-F23F-E301-3EB8B3C15F00";
	setAttr ".t" -type "double3" 1.4142135623730947 0 -4.4408920985006262e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode joint -n "joint4" -p "joint3";
	rename -uid "911E894F-4C7B-3E95-DCCA-CD9353A4164D";
	setAttr ".t" -type "double3" 1.414213562373094 0 -1.1102230246251565e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 44.999999999999986 0 ;
createNode joint -n "joint5" -p "joint4";
	rename -uid "509CD779-446D-8B03-5A47-259C43F2B41A";
	setAttr ".t" -type "double3" 1.0000000000000009 0 4.4408920985006262e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 45.00000000000005 0 ;
createNode joint -n "joint6" -p "joint5";
	rename -uid "805EBC44-4C8F-EC2B-EC07-1289047D86EB";
	setAttr ".t" -type "double3" 1.4142135623730949 0 -2.2204460492503131e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 224.99999999999997 0 ;
createNode joint -n "joint";
	rename -uid "27D091AF-4171-BCF8-3EB1-A8A16B2ADEFA";
createNode joint -n "joint7" -p "joint";
	rename -uid "4C8CC46E-43FA-4065-CF5D-23A9347345E2";
createNode joint -n "joint8" -p "joint7";
	rename -uid "104C9710-4488-DFB3-B482-629B232898FB";
createNode joint -n "joint9" -p "joint8";
	rename -uid "F58FC003-46A6-26D2-C16D-9882F72B5FCC";
createNode joint -n "joint10" -p "joint9";
	rename -uid "61276628-46A7-AE62-DB38-86A6FBCF894F";
createNode joint -n "joint11" -p "joint10";
	rename -uid "9C4AA891-4EDF-3841-3359-3499E18CD635";
	setAttr ".t" -type "double3" 1.4142135623730927 0 -2.6645352591003757e-015 ;
	setAttr ".r" -type "double3" 0 225.00000000000006 0 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "4DA1E1F5-466F-D23E-1EF5-8DB4B21B93FC";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "4F16B98E-4114-F820-1CD2-3B84958DEEEF";
createNode displayLayer -n "defaultLayer";
	rename -uid "F12EECA9-46A8-4ED2-AA0E-D99DC4DCAE22";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "5581AAC9-4E56-F3DF-A870-318D5735542F";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "8FE6A974-47A6-6708-5CC4-36BA0B17F10D";
	setAttr ".g" yes;
createNode dynamicChain -n "dynamicChain";
	rename -uid "A34BFE57-4C32-584C-2E89-5E88E6E41C23";
	setAttr ".uw" 0.5;
	setAttr ".ma" 5;
	setAttr -s 5 ".ilvs";
	setAttr -s 2 ".awrp[0:1]"  0 0.60000002 2 1 1 1;
	setAttr ".uwrp[0]"  0 1 1;
	setAttr ".mrp[0]"  0 1 1;
	setAttr ".srp[0]"  0 0.5 1;
	setAttr ".drp[0]"  0 0.5 1;
	setAttr -s 2 ".grp[0:1]"  0 0.1 2 1 1 1;
	setAttr -s 5 ".ros";
	setAttr -s 5 ".ros";
	setAttr -s 5 ".jos";
	setAttr -s 5 ".jos";
	setAttr ".stm" 0;
	setAttr -s 5 ".olvs";
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "109DDB19-403C-0226-73F3-12B6A8C25EC4";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 10000 -ast 1 -aet 10000 ";
	setAttr ".st" 6;
createNode dynamicTime -n "dynamicTime1";
	rename -uid "89C26FBB-4477-C746-56C6-E489F6E38144";
	setAttr -s 6 ".ims";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".mcfr" 30;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr ".hwfr" 30;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "joint1.s" "joint2.is";
connectAttr "joint2.s" "joint3.is";
connectAttr "joint3.s" "joint4.is";
connectAttr "joint4.s" "joint5.is";
connectAttr "joint5.s" "joint6.is";
connectAttr "dynamicChain.olvs[0].ot" "joint.t";
connectAttr "dynamicChain.olvs[0].or" "joint.r";
connectAttr "joint.s" "joint7.is";
connectAttr "dynamicChain.olvs[1].ot" "joint7.t";
connectAttr "dynamicChain.olvs[1].or" "joint7.r";
connectAttr "joint7.s" "joint8.is";
connectAttr "dynamicChain.olvs[2].ot" "joint8.t";
connectAttr "dynamicChain.olvs[2].or" "joint8.r";
connectAttr "joint8.s" "joint9.is";
connectAttr "dynamicChain.olvs[3].ot" "joint9.t";
connectAttr "dynamicChain.olvs[3].or" "joint9.r";
connectAttr "joint9.s" "joint10.is";
connectAttr "dynamicChain.olvs[4].ot" "joint10.t";
connectAttr "dynamicChain.olvs[4].or" "joint10.r";
connectAttr "joint10.s" "joint11.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "dynamicTime1.ot" "dynamicChain.t";
connectAttr "joint.ro" "dynamicChain.ros[0]";
connectAttr "joint7.ro" "dynamicChain.ros[1]";
connectAttr "joint8.ro" "dynamicChain.ros[2]";
connectAttr "joint9.ro" "dynamicChain.ros[3]";
connectAttr "joint10.ro" "dynamicChain.ros[4]";
connectAttr "joint.jo" "dynamicChain.jos[0]";
connectAttr "joint7.jo" "dynamicChain.jos[1]";
connectAttr "joint8.jo" "dynamicChain.jos[2]";
connectAttr "joint9.jo" "dynamicChain.jos[3]";
connectAttr "joint10.jo" "dynamicChain.jos[4]";
connectAttr "joint.pm" "dynamicChain.ilvs[0].rm";
connectAttr "joint1.wm" "dynamicChain.ilvs[0].im";
connectAttr "joint2.wm" "dynamicChain.ilvs[0].gm";
connectAttr "joint1.wm" "dynamicChain.ilvs[1].rm";
connectAttr "joint2.wm" "dynamicChain.ilvs[1].im";
connectAttr "joint3.wm" "dynamicChain.ilvs[1].gm";
connectAttr "joint2.wm" "dynamicChain.ilvs[2].rm";
connectAttr "joint3.wm" "dynamicChain.ilvs[2].im";
connectAttr "joint4.wm" "dynamicChain.ilvs[2].gm";
connectAttr "joint3.wm" "dynamicChain.ilvs[3].rm";
connectAttr "joint4.wm" "dynamicChain.ilvs[3].im";
connectAttr "joint5.wm" "dynamicChain.ilvs[3].gm";
connectAttr "joint4.wm" "dynamicChain.ilvs[4].rm";
connectAttr "joint5.wm" "dynamicChain.ilvs[4].im";
connectAttr "joint6.wm" "dynamicChain.ilvs[4].gm";
connectAttr ":time1.o" "dynamicTime1.t";
connectAttr "joint1.wm" "dynamicTime1.ims[0]";
connectAttr "joint2.wm" "dynamicTime1.ims[1]";
connectAttr "joint3.wm" "dynamicTime1.ims[2]";
connectAttr "joint4.wm" "dynamicTime1.ims[3]";
connectAttr "joint5.wm" "dynamicTime1.ims[4]";
connectAttr "joint6.wm" "dynamicTime1.ims[5]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of dynamicChain_and_dynamicTime.ma
