//Maya ASCII 2015ff05 scene
//Name: hair.ma
//Last modified: Wed, Aug 12, 2015 01:09:55 PM
//Codeset: 1252
requires maya "2015ff05";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201504171404-000000-1";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
fileInfo "outsourceData" "(dp1\nS'format'\np2\nF1\nsS'misc'\np3\n(lp4\nsS'actors'\np5\n(lp6\nsS'shaders'\np7\n(lp8\nsS'references'\np9\n(lp10\nsS'audio'\np11\n(lp12\ns.";
fileInfo "scene-info" "{\"project\": \"big4\", \"version\": 1.4, \"references\": [], \"user\": \"hgodard\", \"audio\": [], \"scene\": \"C:/Users/hgodard/Desktop/NEW/dynamicChain/hair.ma\", \"refnodes\": [], \"shaders\": []}";
fileInfo "RNLoadStates" "{}";
createNode transform -s -n "persp";
	rename -uid "1605C767-4C2B-142A-FEC9-6498F77C94E5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 5.7766885796616352 6.1525611507453073 6.7048149834592659 ;
	setAttr ".r" -type "double3" -24.338352729602423 37.800000000000047 2.0126143805003664e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "4F3B60DB-4DDA-1356-E631-B0B3F832ED14";
	setAttr -k off ".v" no;
	setAttr ".cap" -type "double2" 1 1 ;
	setAttr ".fl" 16.551;
	setAttr ".coi" 10.588318838772256;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "1F1E0E16-4B8A-D28B-FF6D-7BA8183BD7D3";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "19156676-46A6-3801-B189-3DAC4F55A2D2";
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
	rename -uid "1B0B461D-4560-2689-0C0B-5BA66BA50AFC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "446F87CF-469A-2D37-1591-1594E0C5C7AE";
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
	rename -uid "15C20BD0-40B9-829F-1F42-C7BBA863AB31";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "C7C1A440-4F4D-AE7B-B583-9F811751B18C";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pPlane1";
	rename -uid "E939F2AC-451C-7F61-D1D4-79938E6DAEEC";
	setAttr ".t" -type "double3" 0 1 0 ;
createNode mesh -n "pPlaneShape1" -p "pPlane1";
	rename -uid "BEC844C5-465B-3416-6694-429CB8B7EA10";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ns" 0.051936;
createNode transform -n "hairSystem1";
	rename -uid "E90BBCD1-40CB-70BD-02DF-C7A4E914073B";
createNode hairSystem -n "hairSystemShape1" -p "hairSystem1";
	rename -uid "2FB328A4-4669-383C-B4FC-878FC43749FB";
	setAttr -k off ".v";
	setAttr ".evo" 0;
	setAttr ".sfn" 0.1;
	setAttr -s 2 ".sts[0:1]"  0 1 1 1 0.2 1;
	setAttr -s 2 ".ats[0:1]"  0 1 1 1 0.2 1;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr ".clc[0]"  0 0.5 1;
	setAttr ".cfl[0]"  0 0 1;
	setAttr -s 2 ".hws[0:1]"  0.80000001 1 1 1 0.2 1;
	setAttr -s 3 ".hcs";
	setAttr ".hcs[0].hcsp" 0;
	setAttr ".hcs[0].hcsc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".hcs[0].hcsi" 1;
	setAttr ".hcs[1].hcsp" 0.30000001192092896;
	setAttr ".hcs[1].hcsc" -type "float3" 0.80000001 0.80000001 0.80000001 ;
	setAttr ".hcs[1].hcsi" 1;
	setAttr ".hcs[2].hcsp" 1;
	setAttr ".hcs[2].hcsc" -type "float3" 1 1 1 ;
	setAttr ".hcs[2].hcsi" 1;
	setAttr ".dsc[0]"  0 1 1;
	setAttr ".actv" yes;
createNode nucleus -n "nucleus1";
	rename -uid "EAD77833-4500-D023-8836-05BEBA942220";
	setAttr ".v" no;
createNode transform -n "pPlane1Follicle5050";
	rename -uid "189EDBAC-40EB-4F4E-CA74-D892AC4BAC84";
	setAttr ".v" no;
createNode follicle -n "pPlane1FollicleShape5050" -p "pPlane1Follicle5050";
	rename -uid "70D54783-48D1-6996-693F-73837BA28AA9";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.5;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "curve1" -p "pPlane1Follicle5050";
	rename -uid "CF223300-43A2-105F-239A-A080E2F0FC22";
createNode nurbsCurve -n "curveShape1" -p "curve1";
	rename -uid "01A34535-4C7B-ED76-0F1D-AFBD71CC22A9";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0 0 0
		0 0 0.55555555560000003
		0 0 1.111111111
		0 0 1.6666666670000001
		0 0 2.2222222220000001
		0 0 2.7777777779999999
		0 0 3.3333333330000001
		0 0 3.888888889
		0 0 4.4444444440000002
		0 0 5
		;
createNode transform -n "curve2";
	rename -uid "466EDAA3-45F7-C96C-DF0F-A6A1BFF40663";
createNode nurbsCurve -n "curveShape2" -p "curve2";
	rename -uid "8D92B79F-4199-739A-C2BB-6FB48B4097D0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".tw" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "C3048B04-4ADF-AA71-975C-749CA1E98DDE";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "50ABF09D-43F8-0B23-CF04-66980B159685";
createNode displayLayer -n "defaultLayer";
	rename -uid "7CD41AD2-467A-D979-9527-57BDA889E073";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F7C641DA-4884-6D25-34AB-639AEC2809BF";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "40471C3C-43C7-5754-6849-EE9C340EBFBA";
	setAttr ".g" yes;
createNode polyPlane -n "polyPlane1";
	rename -uid "38AFEF0C-4D0F-578A-BBB2-4FB183D15824";
	setAttr ".sw" 1;
	setAttr ".sh" 1;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "4B3305CB-4383-E9B4-4093-428F2CFC204C";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 10000 -ast 1 -aet 10000 ";
	setAttr ".st" 6;
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
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "polyPlane1.out" "pPlaneShape1.i";
connectAttr ":time1.o" "hairSystemShape1.cti";
connectAttr "pPlane1FollicleShape5050.oha" "hairSystemShape1.ih[0]";
connectAttr "nucleus1.noao[0]" "hairSystemShape1.nxst";
connectAttr "nucleus1.stf" "hairSystemShape1.stf";
connectAttr ":time1.o" "nucleus1.cti";
connectAttr "hairSystemShape1.cust" "nucleus1.niao[0]";
connectAttr "hairSystemShape1.stst" "nucleus1.nias[0]";
connectAttr "pPlane1FollicleShape5050.ot" "pPlane1Follicle5050.t" -l on;
connectAttr "pPlane1FollicleShape5050.or" "pPlane1Follicle5050.r" -l on;
connectAttr "pPlaneShape1.wm" "pPlane1FollicleShape5050.iwm";
connectAttr "pPlaneShape1.o" "pPlane1FollicleShape5050.inm";
connectAttr "curveShape1.l" "pPlane1FollicleShape5050.sp";
connectAttr "curve1.wm" "pPlane1FollicleShape5050.spm";
connectAttr "hairSystemShape1.oh[0]" "pPlane1FollicleShape5050.crp";
connectAttr "pPlane1FollicleShape5050.ocr" "curveShape2.cr";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pPlaneShape1.iog" ":initialShadingGroup.dsm" -na;
// End of hair.ma
