#ifndef _cloneToQuad
#define _cloneToQuad

#include "stdafx.h"



template<typename T> struct PointerHolder
{
	std::vector<T*> ptrs;
	/*
	T* AllocateItems(int count)
	{
		T * p = new T[count];
		data.push_back(p);
		return p;  
	}
	*/
	void shut() { for (auto p : ptrs) { delete p; }  }

	~PointerHolder() { shut() ; }
};
/*
template struct PointerHolder<typename T>
{
	std::vector<uniqe_ptr<T>> m_data;

	T*AllocateItems(size_t count)
	{
		m_data.push_back(new T[count]);
		return m_data.back().get();
	}

};
*/

struct Vertex
// Needed by OpenSubdiv to interpolate
{
    Vertex() {}

    void Clear( void * =0 ) {
         point[0] = point[1] = point[2] = .0; }

    void AddWithWeight(Vertex const & src, double weight) {
        point[0] += weight * src.point[0];
        point[1] += weight * src.point[1];
        point[2] += weight * src.point[2];
    }

    double point[3];
};

struct Scalar
// Needed by OpenSubdiv to interpolate
{
    Scalar() {}

    void Clear( void * =0 ) {
         value = .0; }

    void AddWithWeight(Scalar const & src, double weight) {
        value += weight * src.value; }

    double value ;
};



struct ClonedData
{
	int				V ;				// num vertices
	int				F ;				// num face/polygons
	MPointArray		pnts;			// dim V
	
	MIntArray		polyCounts;		// dim F
	MIntArray		polyVertexIds;

	int				E ;				// num edges
	vecPairII		edgeVertexIds;	// dim E * 2
	boolVec			smoothEdges ;	// are edges smooth ?  dim E

	int				S ;				// num of uvSet
	MStringArray	uvSetNames ;	// dim S
	vecMFloatArray	Us, Vs ;		// dim S * numUV per set
	vecMIntArray	polyUvCounts ;	// dim F
	vecMIntArray	polyUvIds ;	

	MBoundingBox	bb ;
	doubleVec		u_params, v_params ;// dim V
	doubleVec		heights ;			// dim V, vertical height
	double			baseArea ;
};


struct QuadData
{
	int		V ;							// num vert
	int		F ;							// num poly
	int		E ;							// num edge

	MIntArray		polyCounts;			// dim F
	MIntArray		polyVertexIds;

	vecMIntArray	edgeVertices ;		// dim E * 2

	int		Q ;							// num quad  ( <= F )
	intVec	quadIds ;					// polyIds of quads (4 vertices)

	vecMIntArray	adjPolyIds ;		// dim V * num adjacent poly

	intVec			shiftIds ;			// dim F  of offsets
};


struct TesselatedData
{
	int V ;
	int F ;

	MPointArray		pnts;
	MIntArray		polyCounts;
	MIntArray		polyVertexIds;

	MObject			ownerObj ;	// virtual transform.
	MObject			mshObj ;	// mesh itself
	//MFnMesh		msh ;		// "=" not defined !
};


struct SubdivData
{
	Descriptor					descriptor ;
	Refiner	*					refiner_ptr ;
	//PatchTable *				patchTable_ptr ;
	const LimitStencilTable *	limitTable_ptr ;	// dim quadData.Q  *  clonedData.V

	PointerHolder<int>		intPtrHolder ;
	PointerHolder<float>	floatPtrHolder ;
	
	void shut() {
		//delete refiner_ptr ; // CRASH ?
		//delete patchTable_ptr ;
		//delete limitTable_ptr ;
		intPtrHolder.shut() ;
		floatPtrHolder.shut() ;   }
	
	//~SubdivData() { shut() ; }
};



class CloneToQuad : public MPxNode
{
public:
	CloneToQuad();
	virtual				~CloneToQuad();

	static  MTypeId		id;
	static  MString		name;

	static  void*		nodeCreator();

	static  MStatus     nodeInitializer();
	static	MStatus		init_AETemplate();


	// smooth attributes
	
	static	MObject		clonedMesh;			// mesh to clone to every quad of the quadMesh
	static	MObject		clonedChanged;		// to update quadMesh and clonedMesh
	static  MObject     quadMesh;

	static	MObject		cloneUVs ;			// bool to copy or not the UVs from clonedMesh to tessMesh

	static	MObject		scaleHeight;		// scale along normal
	static	MObject		offsetHeight;		// offset along normal
	static	MObject		areaScale ;			// boolean to scale regarding the quad area.

	static	MObject		boundaryInterpolation ;
	static	MObject		normalInterpolation ;

	static	MObject		crease ;
	static	MObject		corner ;

	static	MObject		relativeMatrix ;
	static	MObject		shiftIds ;			// shift poly-vertex-ids

	static	MObject		outMesh ;
	//static	MObject		outComponents ;

	//
	virtual MStatus		compute(const MPlug& plug, MDataBlock& data);
	

private:
	
	ClonedData		clonedData;
	MStatus			update_clonedData( MDataBlock& data );

	MStatus			get_quadMesh( MDataBlock& data, MObject& quad_Obj );

	QuadData		quadData ;
	void			update_quadData(MFnMesh& quad_Msh, MObject& quad_Obj, MArrayDataHandle& shift_Hs );
	
	TesselatedData	tessData ;
	void			update_tessData( bool& do_UVs );

	SubdivData		subdivData ;
	void			update_subdivData( short& boundaryId, float& crease_value, float& corner_value );

	void			create_world_tessMesh( MObject& quad_Obj, MFnMesh& quad_Msh,
											double& scale,
											double& offset,
											double& area_scale,
											short&	normal_mode );

	void			relative_tessMesh( MMatrix& relative_MM ) ;

	//void			transfer_shaders() ;
};

#endif






