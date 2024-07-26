// This is just the ripple points inbuilt snippet with a few sliders tweaked. All parts of the Adl Parameter Parser are supported,
// though OpenCL bindings only directly support Float, Vector, and Int parameters. (you can still use menus and toggles just like in vex)

// Ripple Points
#bind parm center float3 
#bind parm height val=.1 float
#bind parm width val=.5 float
#bind parm phase float
#bind point &P float3

// [[parm=height,min=-4,max=4,default=1]]
// [[parm=width,min=0,max=8,default=.5]]
// [[parm=phase,min=-10,max=10]]

@KERNEL
{
    float3 pos = @P;
    pos.y += sin( (length((pos -@center).xz) / @width + @phase) * M_PI ) * @height;
    @P.set(pos);
}