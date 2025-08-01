from __future__ import print_function
from builtins import zip
import hou
import snippetmenu
import re
import ast

# Change these to change the prefix that the script looks for at the begining of a paramter specification (eg: folder[[name=folder_one,type=collapsible]] )
_adlMetaPrefix = 'meta'
_adlParmPrefix = 'parm'
_adlFolderPrefix = 'folder'

_hasloadedsnippets = False

_initialsnippets = {}
_vexsnippets = {}
_vexsnippets_sol = {}

_initialsnippets['agentcliplayer/localexpression'] = [
"""blendratio = blendratio;
weight = weight;

overrideclipspeed = overrideclipspeed;
clipspeedmultiplier = clipspeedmultiplier;
overridelocomotionspeed = overridelocomotionspeed;
locomotionspeedmultiplier = locomotionspeedmultiplier;

randomizeclipspeed = randomizeclipspeed;
clipspeedvariance = clipspeedvariance;
clipspeedseed = clipspeedseed;

setinitialcliptime = setinitialcliptime;
initialcliptime = initialcliptime;

randomizecliptime = randomizecliptime;
randomclipoffset = randomclipoffset;
randomclipoffsetseed = randomclipoffsetseed;""",
    'Pass Through',
]

_initialsnippets['agentcliplayer/localweightexpression'] = [
"""blendratios = blendratios;
weights = weights;""",
    'Pass Through',
]

_initialsnippets['crowdstate::3.0/localexpression'] = [
"""clipspeedmultiplier = clipspeedmultiplier;
locomotionspeedmultiplier = locomotionspeedmultiplier;

randomizeclipspeed = randomizeclipspeed;
clipspeedvariance = clipspeedvariance;
clipspeedseed = clipspeedseed;""",
    'Pass Through',
]

_initialsnippets['crowdtransition::3.0/localexpression'] = [
"""instate = instate;
outstate = outstate;
useoutclip = useoutclip;
outclip = outclip;""",
    'Pass Through',
]

_initialsnippets['popforce/localforceexpression'] = [
    "force = force;",
        'Pass Through',
]

_initialsnippets['popforce/localnoiseexpression'] = [
"""amp = amp;
rough = rough;
atten = atten;
turb = turb;
pulselength = pulselength;
swirlscale = swirlscale;
swirlsize = swirlsize;
offset = offset;""",
    'Pass Through',
    "amp *= rand(@id);",
    'Randomize Amplitude',
]

_initialsnippets['popattract/primuvcode'] = [
"""goalprim = goalprim;
goalprimuv = goalprimuv;""",
    'Pass Through',
    "goalprimuv.x = @nage;",
    'Follow Curve by Normalized Age',
]

_initialsnippets['popattract/goalcode'] = [
"""goal = goal;
goalvel = goalvel;""",
    'Pass Through',
]

_initialsnippets['popattract/forcecode'] = [
"""forcemethod = forcemethod;
predictintercept = predictintercept;
forcescale = forcescale;
reversaldist = reversaldist;
peakdist = peakdist;
mindist = mindist;
maxdist = maxdist;
ambientspeed = ambientspeed;
speedscale = speedscale;""",
    'Pass Through',
]

_initialsnippets['popaxisforce/localshapeexpression'] = [
"""// 0: sphere
// 1: torus
type = type;
center = center;
axis = axis;
radius = radius;
height = height;""",
    'Pass Through',
]

_initialsnippets['popaxisforce/localspeedexpression'] = [
"""orbitspeed = orbitspeed;
liftspeed = liftspeed;
suctionspeed = suctionspeed;""",
    'Pass Through',
]

_initialsnippets['popaxisforce/localfalloffexpression'] = [
"""softedge = softedge;
innerstrength = innerstrength;
outerstrength = outerstrength;""",
    'Pass Through',
]

_initialsnippets['popaxisforce/localbehavior'] = [
"""treataswind = treataswind;
airresist = airresist;""",
    'Pass Through',
]

_initialsnippets['popcolor/localconstant'] = [
    "color = color;",
    'Pass Through',
    "color = @P;",
    'Position',
    "color = @Cd * 0.9;",
    'Darken Gradually',
]

_initialsnippets['popcolor/localrandom'] = [
    "seed += @ptnum;",
    'Random by Point',
    "seed += @id;",
    'Random by Id',
]

_initialsnippets['popcolor/localramp'] = [
    "ramp = @nage;",
    'Normalized Age',
    "ramp = @age;",
    'Age',
    "ramp = length(@v);",
    'Speed',
    "ramp = @P.y;",
    'Height',
]

_initialsnippets['popcolor/localblendramp'] = [
"""startcolor = startcolor;
endcolor = endcolor;
ramp = @nage;""",
    'Pass Through',
]

_initialsnippets['popcolor/localalphaconstant'] = [
    "alpha = alpha;",
    'Pass Through',
    "alpha = length(@v);",
    'Speed',
    "alpha = fit01(@nage, 1, 0);",
    'Fade with Age',
    'alpha = rand(@id + ch("../seed"));',
    'Random',
]

_initialsnippets['popcolor/localalpharamp'] = [
    "ramp = @nage;",
    'Pass Through',
]

_initialsnippets['popcurveforce/localradius'] = [
"""maxradius = maxradius;
airresist = airresist;""",
    'Pass Through',
]

_initialsnippets['popcurveforce/localforce'] = [
"""scalefollow = scalefollow;
scalesuction = scalesuction;
scaleorbit = scaleorbit;
scaleincomingvel = scaleincomingvel;""",
    'Pass Through',
]

_initialsnippets['popcurveincompressibleflow/localresist'] = [
"""airresist = airresist;
spinresist = spinresist;""",
    'Pass Through',
]

_initialsnippets['popcurveincompressibleflow/localvel'] = [
"""velscale = velscale;
velfallscale = velfallscale;""",
    'Pass Through',
]

_initialsnippets['popcurveincompressibleflow/localavel'] = [
"""avelscale = avelscale;
avelfallscale = avelfallscale;""",
    'Pass Through',
]

_initialsnippets['popdrag/localdragexpression'] = [
"""airresist = airresist;
windvelocity = windvelocity;""",
    'Pass Through',
"""airresist *= @nage;""",
    'Scale Drag by Normalized Age',
]

_initialsnippets['popdragspin/localdragexpression'] = [
"""spinresist = spinresist;
goalaxis = goalaxis;
goalspinspeed = goalspinspeed;""",
    'Pass Through',
"""spinresist *= @nage;""",
    'Scale Drag by Normalized Age',
]

_initialsnippets['popgroup/rulecode'] = [
    "ingroup = 1;",
    'All Particles',
    "ingroup = 0;",
    'No Particles',
    "ingroup = !(@id %5);",
    'Every Fifth Particle by Id',
    "ingroup = length(@v) > 1;",
    'Fast Particles',
]

_initialsnippets['popgroup/randomcode'] = [
"""seed = seed;
chance = chance;
randombehavior = randombehavior;""",
    'Pass Through',
]

_initialsnippets['popinstance/localexpression'] = [
"""instancepath = instancepath;
pscale = pscale;""",
    'Pass Through',
    'instancepath = sprintf("%s%d", instancepath, @id % 5);',
    "Every Fifth Id to Different Instance",
    'pscale *= fit01(@nage, 0.1, 1);',
    "Grow with Age",
]

_initialsnippets['popinteract/localforceexpression'] = [
"""positionforce = positionforce;
velforce = velforce;
coreradius = coreradius;
falloffradius = falloffradius;""",
    'Pass Through',
]

_initialsnippets['popkill/rulecode'] = [
    "dead = 1;",
    'All Particles',
    "dead = 0;",
    'No Particles',
    "dead = !(@id %5);",
    'Every Fifth Particle by Id',
    "dead = length(@v) > 1;",
    'Fast Particles',
    "dead = i@numhit > 0;",
    'Just Hit',
]

_initialsnippets['popkill/randomcode'] = [
"""seed = seed;
chance = chance;
randombehavior = randombehavior;""",
    'Pass Through',
]

_initialsnippets['poplocalforce/localforce'] = [
"""thrust = thrust;
lift = lift;
sideslip = sideslip;""",
    'Pass Through',
]

_initialsnippets['popproperty/localexpression'] = [
"""pscale = pscale;
mass = mass;
spinshape = spinshape;
bounce = bounce;
bounceforward = bounceforward;
friction = friction;
dynamicfriction = dynamicfriction;
drag = drag;
dragshape = dragshape;
dragcenter = dragcenter;
dragexp = dragexp;
cling = cling;""",
    'Pass Through',
]

_initialsnippets['poplookat/code'] = [
"""mode = mode;
method = method;
target = target;
refpath = refpath;
up = up;
dps = dps;
torque = torque;
spinresist = spinresist;
useup = useup;""",
    'Pass Through',
]

_initialsnippets['popsoftlimit/localexpression'] = [
"""t = t;
size = size;
// 0: Box, 1: Sphere
type = type;
invert = invert;
force = force;
vscale = vscale;""",
    'Pass Through',
]

_initialsnippets['popspeedlimit/localexpression'] = [
"""speedmin = speedmin;
speedmax = speedmax;
spinmin = spinmin;
spinmax = spinmax;""",
    'Pass Through',
]

_initialsnippets['popsprite/localexpression'] = [
"""spriteshop = spriteshop;

// 0: Uses offset/size
// 1: Uses textureindex/row/col
cropmode = cropmode;
textureoffset = textureoffset;
texturesize = texturesize;

textureindex = textureindex;
texturerow = texturerow;
texturecol = texturecol;

spriterot = spriterot;
spritescale = spritescale;""",
    'Pass Through',
]

_initialsnippets['poptorque/localforce'] = [
"""axis = axis;
amount = amount;""",
    'Pass Through',
]

_initialsnippets['popwind/localwindexpression'] = [
"""wind = wind;
windspeed = windspeed;
airresist = airresist;""",
    'Pass Through',
"""windspeed *= rand(@id);""",
    'Randomize Magnitude',
    "wind = length(wind) * cross(@P, {0, 1, 0}); ",
    'Orbit the Origin',
]

_initialsnippets['popwind/localnoiseexpression'] = [
"""amp = amp;
rough = rough;
atten = atten;
turb = turb;
pulselength = pulselength;
swirlscale = swirlscale;
swirlsize = swirlsize;
offset = offset;""",
    'Pass Through',
    "amp *= rand(@id);",
    'Randomize Amplitude',
]

_initialsnippets['popproximity/localexpression'] = [
"""distance = distance;
maxcount = maxcount;""",
    'Pass Through',
"""distance *= @pscale;""",
    'Scale by pscale',
]

_initialsnippets['popmetaballforce/localexpression'] = [
"""forcescale = forcescale;""",
    'Pass Through',
"""forcescale *= rand(@id);""",
    'Randomize by Id',
]

_initialsnippets['popadvectbyvolumes/localexpression'] = [
"""forcescale = forcescale;
velscale = velscale;
airresist = airresist;
velblend = velblend;
forceramp = forceramp;""",
    'Pass Through',
"""airresist *= rand(@id);
forcescale *= rand(@id);""",
    'Randomize by Id',
]

_initialsnippets['popspinbyvolumes/localexpression'] = [
"""torquescale = torquescale;
vorticityscale = vorticityscale;
spinresist = spinresist;
angvelblend = angvelblend;""",
    'Pass Through',
"""spinresist *= rand(@id);
torquescale *= rand(@id);""",
    'Randomize by Id',
]

_initialsnippets['popadvectbyvolumes/localexpression'] = [
"""forcescale = forcescale;
velscale = velscale;
airresist = airresist;
velblend = velblend;
forceramp = forceramp;""",
    'Pass Through',
"""airresist *= rand(@id);
forcescale *= rand(@id);""",
    'Randomize by Id',
]

_initialsnippets['rbdconstraintproperties/conelocalexpression'] = [
"""max_up_rotation = max_up_rotation;
max_out_rotation = max_out_rotation;
max_twist = max_twist;
softness = softness;
cfm = cfm;
bias_factor = bias_factor;
relaxation_factor = relaxation_factor;
positioncfm = positioncfm;
positionerp = positionerp;
goal_twist_axis = goal_twist_axis;
goal_up_axis = goal_up_axis;
constrained_twist_axis = constrained_twist_axis;
constrained_up_axis = constrained_up_axis;
disablecollisions = disablecollisions;
constraintiterations = constraintiterations;""",
    'Pass Through'
]

_initialsnippets['rbdconstraintproperties/gluelocalexpression'] = [
"""strength = strength;
halflife = halflife;
propagationrate = propagationrate;
propagationiterations = propagationiterations;""",
    'Pass Through',
"""float minS = 0.5;
float maxS = 1.5;
strength *= fit01(rand(@primnum), minS, maxS);""",
    'Randomize Strength'
]

_initialsnippets['rbdconstraintproperties/hardlocalexpression'] = [
"""cfm = cfm;
erp = erp;
numangularmotors = numangularmotors;
axis1 = axis1;
axis2 = axis2;
targetw = targetw;
maxangularimpulse = maxangularimpulse;
disablecollisions = disablecollisions;
constraintiterations = constraintiterations;""",
    'Pass Through'
]

_initialsnippets['rbdconstraintproperties/softlocalexpression'] = [
"""stiffness = stiffness;
dampingratio = dampingratio;
disablecollisions = disablecollisions;
constraintiterations = constraintiterations;""",
    'Pass Through',
"""float minS = 0.5;
float maxS = 1.5;
stiffness *= fit01(rand(@primnum), minS, maxS);""",
    'Randomize Stiffness'
]

# DOP version
_initialsnippets['vellumconstraintproperty/localexpression'] = [
"""stiffness = stiffness;
stiffnessexp = stiffnessexp;
compressstiffness = compressstiffness;
compressstiffnessexp = compressstiffnessexp;
dampingratio = dampingratio;
restlength = restlength;
restscale = restscale;
restvector = restvector;
plasticthreshold = plasticthreshold;
plasticrate = plasticrate;
plastichardening = plastichardening;
breakthreshold = breakthreshold;
breaktype = breaktype;
remove = remove;
broken = broken;""",
    'Pass Through',
]

# SOP version
_initialsnippets['vellumconstraintproperty/localexpression'] = [
"""stiffness = stiffness;
stiffnessexp = stiffnessexp;
compressstiffness = compressstiffness;
compressstiffnessexp = compressstiffnessexp;
dampingratio = dampingratio;
restlength = restlength;
restvector = restvector;
plasticthreshold = plasticthreshold;
plasticrate = plasticrate;
plastichardening = plastichardening;
breakthreshold = breakthreshold;
breaktype = breaktype;
remove = remove;""",
    'Pass Through',
]

# SOP version
_initialsnippets['rbdconetwistconstraintproperties/localexpression'] = [
"""max_up_rotation = max_up_rotation;
max_out_rotation = max_out_rotation;
max_twist = max_twist;
softness = softness;
computeinitialerror = computeinitialerror;
enablesoft = enablesoft;
angularlimitstiffness = angularlimitstiffness;
angularlimitdampingratio = angularlimitdampingratio;
twisttranslationrange = twisttranslationrange;
outtranslationrange = outtranslationrange;
uptranslationrange = uptranslationrange;
positionlimitstiffness = positionlimitstiffness;
positionlimitdampingratio = positionlimitdampingratio;
cfm = cfm;
bias_factor = bias_factor;
relaxation_factor = relaxation_factor;
positioncfm = positioncfm;
positionerp = positionerp;
goal_twist_axis = goal_twist_axis;
goal_up_axis = goal_up_axis;
constrained_twist_axis = constrained_twist_axis;
constrained_up_axis = constrained_up_axis;
motor_enabled = motor_enabled;
motor_targetcurrentpose = motor_targetcurrentpose;
motor_target = motor_target;
motor_targetp = motor_targetp;
motor_hastargetprev = motor_hastargetprev;
motor_targetprev = motor_targetprev;
motor_targetprevp = motor_targetprevp;
motor_normalizemaximpulse = motor_normalizemaximpulse;
motor_maximpulse = motor_maximpulse;
motor_erp = motor_erp;
motor_cfm = motor_cfm;
motor_targetangularstiffness = motor_targetangularstiffness;
motor_targetangulardampingratio = motor_targetangulardampingratio;
motor_targetpositionstiffness = motor_targetpositionstiffness;
motor_targetpositiondampingratio = motor_targetpositiondampingratio;
disablecollisions = disablecollisions;
numiterations = numiterations;
restlength = restlength;
Cd = Cd;""",
    'Pass Through',
]

# LOP version
_initialsnippets['lpetag/vexpression'] = [
"""tag = tag;""",
    'Pass Through',
]


def installInitialSnippets():
    """ Copies the initial snippets into _vexsnippets and adds
        the comment prefix.
    """
    for parm in _initialsnippets:
        rawlist = _initialsnippets[parm]
        pairlist = list(zip(rawlist[::2], rawlist[1::2]))
        item_list = []
        sol_list = []
        for (body, title) in pairlist:
            sol_list.append(body.strip())
            sol_list.append(title)
            body = '// ' + title + '\n' + body
            item_list.append(body)
            item_list.append(title)
        _vexsnippets[parm] = item_list
        _vexsnippets_sol[parm] = sol_list


def ensureSnippetsAreLoaded():
    global _hasloadedsnippets

    if not _hasloadedsnippets:
        _hasloadedsnippets = True
        installInitialSnippets()
        (snippets, snippets_sol) = snippetmenu.loadSnippets(
            hou.findFiles('VEXpressions.txt'), '//')
        _vexsnippets.update(snippets)
        _vexsnippets_sol.update(snippets_sol)


def buildSnippetMenu(snippetname):
    """ Given a snippetname, determine what
        snippets should be generated
    """
    ensureSnippetsAreLoaded()
    if snippetname in _vexsnippets:
        return list(_vexsnippets[snippetname])
    else:
        return ["", "None"]


def buildSingleLineSnippetMenu(snippetname):
    """ Given a snippetname, determine what
        snippets should be generated
    """
    ensureSnippetsAreLoaded()
    if snippetname in _vexsnippets_sol:
        return list(_vexsnippets_sol[snippetname])
    else:
        return ["", "None"]


# Strings representing channel calls
chcalls = [
    'ch', 'chf', 'chi', 'chu', 'chv', 'chp', 'ch2', 'ch3', 'ch4',
    'vector(chramp', 'chramp',
    'vector(chrampderiv', 'chrampderiv',
    'chs',
    'chdict', 'chsop'
]
# Expression for finding ch calls
chcall_exp = re.compile(f"""
\\b  # Start at word boundary
({"|".join(re.escape(chcall) for chcall in chcalls)})  # Match any call string
\\s*[(]\\s*  # Opening bracket, ignore any surrounding whitespace
('\\w+'|"\\w+")  # Single or double quoted string
\\s*[),]  # Optional white space and closing bracket or comma marking end of first argument
""", re.VERBOSE)
# Number of components corresponding to different ch calls. If a call string is
# not in this dict, it's assumed to have a single component.
ch_size = {
    'chu': 2, 'chv': 3, 'chp': 4, 'ch2': 4, 'ch3': 9, 'ch4': 16,
}
# This expression matches comments (single and multiline) and also strings
# (though it will miss strings with escaped quote characters).
comment_or_string_exp = re.compile(
    r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
    re.DOTALL | re.MULTILINE
)




# The following 2 functions are from StackOverflow (I barely understand how they work if I'm being honest):
# Question: https://stackoverflow.com/questions/1648537/how-to-split-a-string-by-commas-positioned-outside-of-parenthesis
# Answer Author: https://stackoverflow.com/users/140894/don-odonnell
# Answer: https://stackoverflow.com/a/1653602
def srchrepl(srch, repl, string):
    """Replace non-bracketed/quoted occurrences of srch with repl in string"""

    resrchrepl = re.compile(r"""(?P<lbrkt>[([{])|(?P<quote>['"])|(?P<sep>["""
                            + srch + """])|(?P<rbrkt>[)\]}])""")
    return resrchrepl.sub(_subfact(repl), string)

def _subfact(repl):
    """Replacement function factory for regex sub method in srchrepl."""
    level = 0
    qtflags = 0
    def subf(mo):
        nonlocal level, qtflags
        sepfound = mo.group('sep')
        if  sepfound:
            if level == 0 and qtflags == 0:
                return repl
            else:
                return mo.group(0)
        elif mo.group('lbrkt'):
            level += 1
            return mo.group(0)
        elif mo.group('quote') == "'":
            qtflags ^= 1            # toggle bit 1
            return "'"
        elif mo.group('quote') == '"':
            qtflags ^= 2            # toggle bit 2
            return '"'
        elif mo.group('rbrkt'):
            level -= 1
            return mo.group(0)
    return subf

# Basic wrapper for the previous two functions, allowing for simple and robust splitting
def srchsplit(srch, code):
    # Code for ASCII/Unicode group-separator
    GRPSEP = chr(29)
    return srchrepl(srch, GRPSEP, code).split(GRPSEP)

# If a preset key is present in the setting dictionary, this is called and the relevant set of parameters then get applied to the 
# There might be a better way to format this code for multiline expressions, but this works well enough
def _checkPresets(currentSettings):
    presetName = currentSettings['preset']
    presets = {}

    # This preset optionally uses the input max parameter to decide both values
    presets['zeroCentered'] = {'min':-currentSettings.get('max',1), 'max':currentSettings.get('max',1) }
    # This preset configures the appropriate tags for a LOP string parameter, retaining preexisting tags
    presets['lopPrimSelect'] = { 'tags': currentSettings.get('tags',{}) | {'sidefx::usdpathtype': 'primlist', 'script_action':
"""
import loputils
loputils.selectPrimsInParm(kwargs, True,
allowinstanceproxies=kwargs['node'].parm(
'allowinstanceproxies').eval() != 0)
""",
                                        'script_action_icon':'BUTTONS_reselect', 'script_action_help':
"""
Select primitives in the Scene Viewer or Scene Graph Tree pane.
Ctrl-click to select using the primitive picker dialog.
Shift-click to select using the primitive pattern editor.
Alt-click to toggle movement of the display flag.
"""  } }
    # Generally, the attribSelect presets follow the same parameter as the selection parameter in the "Attribute Adjust Float/Vector/Int" node 
    # Configures the appropriate menu settings and tags for a string parameter with an attribute selector and visualizing button
    presets['attribSelect'] = {'menu_script_language':'Python','menu_type':'StringReplace','item_generator_script':
"""
r = []
node = hou.pwd()
inputs = node.inputs()
if inputs and inputs[0]:
    geo = inputs[0].geometry()
    if geo:
        c = node.parm('class').evalAsString()
        if c == 'detail':
            attrs = geo.globalAttribs()
        elif c == 'primitive':
            attrs = geo.primAttribs()
        elif c == 'point':
            attrs = geo.pointAttribs()
        else: # vertex
            attrs = geo.vertexAttribs()
        for a in attrs:
            r.extend([a.name(), a.name()])
return r
""", 'tags': currentSettings.get('tags',{}) | {'script_action_help':'Toggle visualization Ctrl-LMB: Open the visualization editor',
                                               'script_action_icon':'VIEW_visualization',
                                               'script_action':
"""
import soputils  
viz = soputils.getFalseColorVisualizerDefaults()
soputils.actionToggleVisualizer(kwargs, viz_defaults=viz)
"""} }
    # Same as above, but filters only float attributes, using an appropriate default visualizer
    presets['attribSelectFloat'] = {'menu_script_language':'Python','menu_type':'StringReplace','item_generator_script':
"""
r = []
node = hou.pwd()
inputs = node.inputs()
if inputs and inputs[0]:
    geo = inputs[0].geometry()
    if geo:
        c = node.parm('class').evalAsString()
        if c == 'detail':
            attrs = geo.globalAttribs()
        elif c == 'primitive':
            attrs = geo.primAttribs()
        elif c == 'point':
            attrs = geo.pointAttribs()
        else: # vertex
            attrs = geo.vertexAttribs()
        for a in attrs:
            if a.dataType() == hou.attribData.Float and not a.isArrayType() and a.size() == 1:
                r.extend([a.name(), a.name()])
return r
""", 'tags': currentSettings.get('tags',{}) | {'script_action_help':'Toggle visualization Ctrl-LMB: Open the visualization editor',
                                               'script_action_icon':'VIEW_visualization',
                                               'script_action':
"""
import soputils  
viz = soputils.getFalseColorVisualizerDefaults()
soputils.actionToggleVisualizer(kwargs, viz_defaults=viz)
"""} }
    # Same as above, but filters only vector (float[3]) attributes, using an appropriate default visualizer
    presets['attribSelectVector'] = {'menu_script_language':'Python','menu_type':'StringReplace','item_generator_script':
"""
r = []
node = hou.pwd()
inputs = node.inputs()
if inputs and inputs[0]:
    geo = inputs[0].geometry()
    if geo:
        c = node.parm('class').evalAsString()
        if c == 'detail':
            attrs = geo.globalAttribs()
        elif c == 'primitive':
            attrs = geo.primAttribs()
        elif c == 'point':
            attrs = geo.pointAttribs()
        else: # vertex
            attrs = geo.vertexAttribs()
        for a in attrs:
            if a.dataType() == hou.attribData.Float and not a.isArrayType() and a.size() == 3:
                r.extend([a.name(), a.name()])
return r
""", 'tags': currentSettings.get('tags',{}) | {'script_action_help':'Toggle visualization Ctrl-LMB: Open the visualization editor',
                                               'script_action_icon':'VIEW_visualization',
                                               'script_action':
"""
import soputils  
soputils.actionToggleVisualizer(kwargs)
"""} }
    # Same as above, but filters only int attributes, using an appropriate default visualizer
    presets['attribSelectInt'] = {'menu_script_language':'Python','menu_type':'StringReplace','item_generator_script':
"""
r = []
node = hou.pwd()
inputs = node.inputs()
if inputs and inputs[0]:
    geo = inputs[0].geometry()
    if geo:
        c = node.parm('class').evalAsString()
        if c == 'detail':
            attrs = geo.globalAttribs()
        elif c == 'primitive':
            attrs = geo.primAttribs()
        elif c == 'point':
            attrs = geo.pointAttribs()
        else: # vertex
            attrs = geo.vertexAttribs()
        for a in attrs:
            if a.dataType() == hou.attribData.Int and not a.isArrayType() and a.size() == 1:
                r.extend([a.name(), a.name()])
return r
""", 'tags': currentSettings.get('tags',{}) | {'script_action_help':'Toggle visualization Ctrl-LMB: Open the visualization editor',
                                               'script_action_icon':'VIEW_visualization',
                                               'script_action':
"""
import soputils  
viz = soputils.getRandomColorVisualizerDefaults()
soputils.actionToggleVisualizer(kwargs, viz_defaults=viz)
"""} }
    # Same as above, but filters only string attributes, using an appropriate default visualizer
    presets['attribSelectString'] = {'menu_script_language':'Python','menu_type':'StringReplace','item_generator_script':
"""
r = []
node = hou.pwd()
inputs = node.inputs()
if inputs and inputs[0]:
    geo = inputs[0].geometry()
    if geo:
        c = node.parm('class').evalAsString()
        if c == 'detail':
            attrs = geo.globalAttribs()
        elif c == 'primitive':
            attrs = geo.primAttribs()
        elif c == 'point':
            attrs = geo.pointAttribs()
        else: # vertex
            attrs = geo.vertexAttribs()
        for a in attrs:
            if a.dataType() == hou.attribData.String and not a.isArrayType() and a.size() == 1:
                r.extend([a.name(), a.name()])
return r
""", 'tags': currentSettings.get('tags',{}) | {'script_action_help':'Toggle visualization Ctrl-LMB: Open the visualization editor',
                                               'script_action_icon':'VIEW_visualization',
                                               'script_action':
"""
import soputils  
viz = soputils.getRandomColorVisualizerDefaults()
soputils.actionToggleVisualizer(kwargs, viz_defaults=viz)
"""} }
    
    return presets.get(presetName,{})


_setting_aliases = {'minlock':'min_is_strict','maxlock':'max_is_strict','default_value':'default'}

# This creates a dictionary of parameters with any existing parameter settings found in the input code
def _getAdlSettings(code, settingname, itemTitle, enablelocating):
    adlSettingCall_exp = re.compile(f"(?s)(?<="+settingname+"\[\[).*?(?=\]\])", re.VERBOSE)
    foundparms = set()
    definedParmCollection= {}
    matchindex = 0
    for match in adlSettingCall_exp.finditer(code):
        matchindex += 1
        currentmatch = match[0]
        definedSettings = {}
        # Currently using a more complex matching function, but leaving the old method in the case that there is an unintended downside (like performance)
        # SEP_MATCHER = re.compile(r"\|\|(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
        # for currentset in SEP_MATCHER.split(currentmatch):
        for currentset in srchsplit('||',currentmatch):
            # Grab key-value pairs that are separated by a comma sign, which are in turn separated by an equal sign
            newdict = {}
            # COMMA_MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
            # for sub in COMMA_MATCHER.split(currentset):
            for sub in srchsplit(',',currentset):
                if '=' in sub: 
                    subsplit = sub.split('=', 1)
                    subKey = subsplit[0].strip()
                    # Try to evaluate the value directly, falling back to a standard write if it fails
                    try:
                        subVal = ast.literal_eval( subsplit[1].strip() )
                        # subVal = eval( subsplit[1].strip() )
                    except (ValueError, NameError):
                        subVal = subsplit[1].strip()
                else:
                    # If there isn't an equals sign, assume that this is a boolean value intended to be enabled.
                    subKey = sub.strip()
                    subVal = True

                if subKey in _setting_aliases:
                    # Check if the current key name has an alias available and swap it out
                    subKey = _setting_aliases[subKey]
                newdict[subKey] = subVal
            # Write the current settings to the larger dict
            definedSettings = definedSettings | newdict

        # If the itemTitle is empty, assume that values should be written directly to the top-level dictionary
        if itemTitle == None or itemTitle == '':
            definedParmCollection = definedParmCollection | definedSettings
        else:
            if itemTitle not in definedSettings or isinstance(definedSettings[itemTitle], int):
                if enablelocating:
                    # If the item title is not present or is an int, assume the intent to get a nearby parameter
                    # LIMITATION: Only checks between the previous match at the current. Ideally, this would consider all occurences before the current setting match
                    # I'm certain this could be optimized pretty dramatically, since it currently does two extensive RegEx operations, one of which is likely redundant
                    chindex = definedSettings.get(itemTitle,-1)
                    beforeSetting = adlSettingCall_exp.split(code)[matchindex-1]
                    intendedItem = chcall_exp.findall(beforeSetting)[chindex][1][1:-1]
                    definedSettings[itemTitle] = intendedItem
                else:
                    # Ignore the current settings if they do not have a proper item title and locating is disabled
                    continue

            # Continute to the next iteration if the current parm has already been found
            targetparm = definedSettings[itemTitle]
            if targetparm in foundparms:
                continue
            foundparms.add(targetparm)

            # If the preset key is present, add the corresponding preset settings to the dict
            if 'preset' in definedSettings:
                definedSettings = definedSettings | _checkPresets(definedSettings)

            # Write current settings to the larger dict
            definedParmCollection[targetparm]=definedSettings

    return definedParmCollection

class _adlTemplateMaker:
    """Main class for taking an input dictionary of parameter settings and creating a template from it."""
    def __init__(self, parmSettings, name, label, size):
        self.parmSettings = parmSettings
        self.name = name
        multiparm = self.parmSettings.get('is_multiparm', 0)
        if multiparm:
            self.name += '#'*multiparm
        self.label = str(self.parmSettings.get('label',label))
        self.size = int(self.parmSettings.get('size',size))

    def _initializeTupleValues(self, targetDict, targetKey, fallback):
        """Checks if a target dictionary value is a tuple, and if not converts it to one."""
        tupleVals = targetDict.get(targetKey,fallback)
        if( isinstance(tupleVals, tuple) != 1):
            tupleVals = tuple([tupleVals],)
        return tupleVals
    
    def __dictSplitter(self, dict):
        dictSets = {}
        if dict:
            keySet = []
            valSet = []
            for key in dict:
                keySet.append(key)
                valSet.append(dict[key])

            dictSets['keys']=tuple(keySet)
            dictSets['vals']=tuple(valSet)
        else:
            dictSets['keys']=()
            dictSets['vals']=()
        return dictSets

    def __getMenuKwargs(self):
        menu_kwargs = {}
        if 'menu_pairs' in self.parmSettings:
            splitDict = self.__dictSplitter(self.parmSettings['menu_pairs'])
            menu_kwargs['menu_items'] = splitDict.get('keys',())
            menu_kwargs['menu_labels'] = splitDict.get('vals',())
        elif 'menu_items' in self.parmSettings:
            menu_kwargs['menu_items'] = self.parmSettings['menu_items']
            menu_kwargs['menu_labels'] = self.parmSettings.get('menu_labels',())
        else:
            menu_kwargs['menu_items'] = ()
            menu_kwargs['menu_labels'] = ()
        if 'item_generator_script' in self.parmSettings:
            menu_kwargs['item_generator_script'] = self.parmSettings['item_generator_script']                 
            menu_kwargs['item_generator_script_language'] = getattr(hou.scriptLanguage, self.parmSettings.get('item_generator_script_language','Python') )
        else:
            menu_kwargs['item_generator_script'] = ''
            menu_kwargs['item_generator_script_language'] = None
        menu_kwargs['menu_type'] = getattr(hou.menuType, self.parmSettings.get('menu_type','Normal'))
        menu_kwargs['icon_names'] = self.parmSettings.get('icon_names',())
        self.menu_kwargs =  menu_kwargs

    def getCommonSettings(self):
        # Common parameter settings are explicitly defined here, with more particular ones being set later
        self.is_hidden = int(self.parmSettings.get('is_hidden',0))
        self.join_with_next = int(self.parmSettings.get('join_with_next',0))
        self.tags = dict(self.parmSettings.get('tags',{}))
        self.is_label_hidden = int(self.parmSettings.get('is_label_hidden',0))
        self.help = str(self.parmSettings.get('help',''))
        self.default_expression_language = self._initializeTupleValues({'deflang': getattr( hou.scriptLanguage, self.parmSettings.get('default_expression_language','Hscript')) }, 'deflang',hou.scriptLanguage.Hscript)
        self.script_callback = self.parmSettings.get('script_callback',None)
        self.script_callback_language = getattr( hou.scriptLanguage, self.parmSettings.get('script_callback_language', 'Hscript'))

        self.disable_when = self.parmSettings.get('disable_when','')
        self.hide_when = self.parmSettings.get('hide_when','')
        
        self.direct_kwargs = self.parmSettings.get('kwargs',{})

    def __getDefaults(self, fallback):
        self.default_expression = self._initializeTupleValues(self.parmSettings, 'default_expression', '')
        self.default_value = self._initializeTupleValues(self.parmSettings, 'default', fallback)

    def __getCommonNumberSettings(self):
        self.min_is_strict = int(self.parmSettings.get('min_is_strict',0))
        self.max_is_strict = int(self.parmSettings.get('max_is_strict',0))
        self.look = getattr(hou.parmLook, self.parmSettings.get('look','Regular'))
        self.naming_scheme = getattr(hou.parmNamingScheme,self.parmSettings.get('naming_scheme','XYZW'))
    
    def __getCommonRampSettings(self):
        self.default_value = int(self.parmSettings.get('default',2))
        if 'default_basis' in self.parmSettings: self.default_basis = getattr(hou.rampBasis, self.parmSettings['default_basis'])
        else: self.default_basis = None
        self.show_controls = self.parmSettings.get('show_controls', None)

    def makeFloat(self):
        """Create a generic Float Parameter Template"""
        self.__getDefaults(0)
        self.__getCommonNumberSettings()
        self.min = float(self.parmSettings.get('min',0))
        self.max = float(self.parmSettings.get('max',1))
        kwargs = {'default_value':self.default_value,
                  'min':self.min, 
                  'max':self.max, 
                  'min_is_strict':self.min_is_strict, 
                  'max_is_strict':self.max_is_strict, 
                  'look':self.look, 
                  'naming_scheme':self.naming_scheme, 
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden, 
                  'is_label_hidden':self.is_label_hidden, 
                  'join_with_next':self.join_with_next, 
                  'help':self.help, 
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression':self.default_expression, 
                  'default_expression_language':self.default_expression_language}
        # Merge direct kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.FloatParmTemplate(self.name, self.label, self.size, **kwargs )
    
    def makeInteger(self):
        """Create a generic Integer Parameter Template"""
        self.__getMenuKwargs()
        self.__getDefaults(0)
        self.__getCommonNumberSettings()
        self.min = int(self.parmSettings.get('min',0))
        self.max = int(self.parmSettings.get('max',10))
        kwargs = {'default_value':self.default_value,
                  'min':self.min,
                  'max':self.max,
                  'min_is_strict':self.min_is_strict,
                  'max_is_strict':self.max_is_strict,
                  'look':self.look,
                  'naming_scheme':self.naming_scheme,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'is_label_hidden':self.is_label_hidden,
                  'join_with_next':self.join_with_next,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression':self.default_expression,
                  'default_expression_language':self.default_expression_language}
        # Merge menu arguments and any direct kwargs
        kwargs = kwargs | self.menu_kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.IntParmTemplate(self.name, self.label, self.size, **kwargs )
    
    def makeToggle(self):
        """Create a toggle Parameter Template"""
        self.default_value = self.parmSettings.get('default',0)
        self.default_expression = self.parmSettings.get('default_expression','')
        kwargs = {'default_value':self.default_value,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'is_label_hidden':self.is_label_hidden,
                  'join_with_next':self.join_with_next,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression':self.default_expression,
                  'default_expression_language':self.default_expression_language[0] }
        # Merge direct kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.ToggleParmTemplate(self.name, self.label, **kwargs )

    def makeRamp(self):
        """Create a Ramp Parameter Template, as a float type"""
        self.__getCommonRampSettings()
        kwargs = {'default_value':self.default_value,
                  'default_basis':self.default_basis,
                  'show_controls':self.show_controls,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression_language':self.default_expression_language[0]}
        # Merge direct kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.RampParmTemplate(self.name, self.label, hou.rampParmType.Float, **kwargs )
    
    def makeColorRamp(self):
        """Create a Ramp Parameter Template, as a color type"""
        self.__getCommonRampSettings()
        if 'color_type' in self.parmSettings: self.default_basis = getattr(hou.colorType, self.parmSettings['color_type'])
        else: self.color_type = None
        kwargs = {'default_value':self.default_value,
                  'default_basis':self.default_basis,
                  'show_controls':self.show_controls,
                  'color_type':self.color_type,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression_language':self.default_expression_language[0]}
        kwargs = kwargs | self.direct_kwargs
        return hou.RampParmTemplate(self.name, self.label, hou.rampParmType.Color, **kwargs )

    def makeString(self):
        """Create a generic String Parameter Template"""
        self.__getMenuKwargs()
        # String menus prefer the default value to be one of the item names, not an empty value
        if self.menu_kwargs['menu_items']:
            defFallback = self.menu_kwargs['menu_items'][0]
        else:
            defFallback=''
        self.__getDefaults(defFallback)
        self.naming_scheme = getattr(hou.parmNamingScheme, self.parmSettings.get('naming_scheme', 'Base1'))
        self.string_type = getattr(hou.stringParmType, self.parmSettings.get('string_type', 'Regular'))
        self.file_type = getattr(hou.fileType, self.parmSettings.get('file_type', 'Any'))
        kwargs = {'default_value':self.default_value,
                  'naming_scheme':self.naming_scheme,
                  'string_type':self.string_type,
                  'file_type':self.file_type,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'is_label_hidden':self.is_label_hidden,
                  'join_with_next':self.join_with_next,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression':self.default_expression, 
                  'default_expression_language':self.default_expression_language}
        # Merge menu arguments and any direct kwargs
        kwargs = kwargs | self.menu_kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.StringParmTemplate(self.name, self.label, self.size, **kwargs )
    
    def makeNodeString(self):
        """Create a String Parameter Template, as a Node Reference"""
        self.__getDefaults('')
        kwargs = {'default_value':self.default_value,
                  'string_type':hou.stringParmType.NodeReference,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'is_label_hidden':self.is_label_hidden,
                  'join_with_next':self.join_with_next,
                  'help':self.help,
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'tags':self.tags,
                  'default_expression':self.default_expression, 
                  'default_expression_language':self.default_expression_language}
        # Merge direct kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.StringParmTemplate(self.name, self.label, self.size, **kwargs )
    
    def makeDict(self):
        """Create a Data Parameter Template, as a Key Value Dictionary"""
        self.__getDefaults('')
        self.look = getattr(hou.parmLook, self.parmSettings.get('look','Regular'))
        self.naming_scheme = getattr(hou.parmNamingScheme, self.parmSettings.get('naming_scheme', 'XYZW'))
        kwargs = {'data_parm_type':hou.dataParmType.KeyValueDictionary,
                  'look':self.look,
                  'naming_scheme':self.naming_scheme,
                  'disable_when':self.disable_when,
                  'is_hidden':self.is_hidden,
                  'is_label_hidden':self.is_label_hidden,
                  'join_with_next':self.join_with_next,
                  'help':self.help, 
                  'script_callback':self.script_callback,
                  'script_callback_language':self.script_callback_language, 
                  'default_expression':self.default_expression,
                  'tags':self.tags,
                  'default_expression':self.default_expression,
                  'default_expression_language':self.default_expression_language}
        # Merge direct kwargs
        kwargs = kwargs | self.direct_kwargs
        return hou.DataParmTemplate(self.name, self.label, self.size, **kwargs )
    
    def makeDirect(self):
        """Directly create a Parameter Template from a user-defined class string and arguments"""
        templateClass = getattr(hou, self.parmSettings['template'] )
        if 'args' in self.parmSettings:
            # Assume that all argument handling is being done directly in the parameter settings
            direct_args = self.parmSettings['args']
            direct_kwargs = self.parmSettings.get('kwargs',{})
            template = templateClass( *direct_args, **direct_kwargs)
        else:
            # Fallback to constructing the basic args if they are not present. Not recommended.
            print('Using automatic argument construction for '+self.name+'. Explicit arguments recommended through setting args=(foo,bar)')
            self.label = str(self.parmSettings.get('label',self.label))
            direct_kwargs = self.parmSettings.get('kwargs',{})
            template = templateClass( self.name, self.label, self.size, **direct_kwargs )
        return template

def _adlAddSpareParmsToStandardFolder(node, parmname, refs, definedParmCollection, definedFolderCollection, adlMetadata):
    """
    Takes a list of (name, template) in refs and injects them into the
    standard-named folder for generated parms.  If it doesn't exist,
    create the folder and place before parmname.
    """
    if not refs and not definedFolderCollection:
        return          # No-op
    
    ptg = node.parmTemplateGroup()

    independent_folder_templates = {}
    folder_templates = {}
    if definedFolderCollection:
        # Process existing folder settings
        for currentname in definedFolderCollection:
            adlFolderSettings = definedFolderCollection[currentname]
            folderLabel = adlFolderSettings.get( 'label', currentname.title().replace("_", " ") )

            direct_kwargs = adlFolderSettings.get('kwargs',{})
            folder_aliases = {'collapsible':'Collapsible',
                              'simple':'Simple',
                              'tabs':'Tabs',
                              'radiobuttons':'RadioButtons',
                              'multiparmblock':'MultiparmBlock',
                              'scrollingmultiparmblock':'ScrollingMultiparmBlock',
                              'tabbedmultiparmblock':'TabbedMultiparmBlock',
                              'importblock':'ImportBlock',
                              'borderless':'Simple',
                              'Borderless':'Simple'}
            folder_type = adlFolderSettings.get('folder_type', 'Simple')
            if folder_type in folder_aliases:
                # If an alias is found, swap it out for the input value, otherwise leave the original
                folder_type= folder_aliases[folder_type]
                
            folder_type = getattr(hou.folderType, folder_type )
            is_hidden = adlFolderSettings.get('is_hidden', False)
            ends_tab_group = adlFolderSettings.get('ends_tab_group', False)
            tags = adlFolderSettings.get('tags',{})
            # Since borderless isn't actualy a folder type, merge the needed tags with any existing ones
            if adlFolderSettings.get('folder_type','') == 'borderless' or adlFolderSettings.get('folder_type','') == 'Borderless': tags = tags | {'sidefx::look':'blank'}

            conditionals = adlFolderSettings.get('conditionals',{})
            # since disablewhen and hidewhen are fairly common usecases, it is possible to directly specify them instead of using the conditionals dict (which still takes priority)
            disable_when = adlFolderSettings.get('disable_when','')
            if hou.parmCondType.DisableWhen not in conditionals and disable_when:
                conditionals[hou.parmCondType.DisableWhen] = disable_when
            hide_when = adlFolderSettings.get('hide_when','')
            if hou.parmCondType.HideWhen not in conditionals and hide_when:
                conditionals[hou.parmCondType.HideWhen] = hide_when

            tab_conditionals = adlFolderSettings.get('tab_conditionals',{})
            tab_disable_when = adlFolderSettings.get('tab_disable_when','')
            if hou.parmCondType.DisableWhen not in tab_conditionals and tab_disable_when:
                tab_conditionals[hou.parmCondType.DisableWhen] = tab_disable_when
            tab_hide_when = adlFolderSettings.get('tab_hide_when','')
            if hou.parmCondType.HideWhen not in conditionals and tab_hide_when:
                tab_conditionals[hou.parmCondType.HideWhen] = tab_hide_when

            kwargs = {'folder_type':folder_type,'is_hidden':is_hidden,'ends_tab_group':ends_tab_group,'tags':tags,'conditionals':conditionals,'tab_conditionals':tab_conditionals}
            kwargs = kwargs | direct_kwargs

            if ptg.find(currentname):
                # If the folder is already present, incorporate it's child parm_templates
                parm_templates = ptg.find(currentname).parmTemplates()
                kwargs = kwargs | {'parm_templates':parm_templates}

            template = hou.FolderParmTemplate(currentname,folderLabel, **kwargs)
            if(adlFolderSettings.get('independent',0)):
                independent_folder_templates[currentname] = template
            else:
                folder_templates[currentname] = template

    # We consider a multiparm any parameter with a number in it.
    # This might have false positives, but it is important to not try
    # to create a parameter before a multiparm as that slot
    # won't exist.  We also use a single standard folder name
    # for all the multiparm snippets.
    ismultiparm = any(map(str.isdigit, parmname))

    foldername = 'folder_generatedparms_' + parmname
    if ismultiparm:
        foldername = 'folder_generatedparms'

    folder = ptg.find(foldername)
    if not folder:
        folder = hou.FolderParmTemplate(
            foldername,
            "Generated Channel Parameters",
            folder_type=hou.folderType.Simple,
        )
        folder.setTags({"sidefx::look": "blank"})
        if not ismultiparm:
            ptg.insertBefore(parmname, folder)
        else:
            ptg.insertBefore(ptg.entries()[0], folder)

    # If any folders were set as independent from any parameters, place them first.
    # This is mainly useful for top-level folders with subfolders.
    if independent_folder_templates:
        for indep_foldername in independent_folder_templates:
            currentFolderTemplate = independent_folder_templates[indep_foldername]
            # If a parent folder is specificed, target it instead of the default folder
            parentfolder = definedFolderCollection[indep_foldername].get('parent_folder','')
            if parentfolder:
                # Since a parent folder was specified, confirm it's existence
                parentfolder = ptg.find(parentfolder)
                if not parentfolder:
                    print("Parent folder for "+indep_foldername+" does not exist. Using default folder instead.")
                    parentfolder = ptg.find(foldername)
            else:
                parentfolder = ptg.find(foldername)
            # Check for existence of the current template folder
            indepfolder = ptg.find(indep_foldername)
            if indepfolder:
                ptg.replace(indep_foldername, currentFolderTemplate)
            else:
                ptg.appendToFolder(ptg.findIndices(parentfolder), currentFolderTemplate)

    # Insert/replace the parameter templates
    indices = ptg.findIndices(foldername)
    for name, template in refs:
        if 'folder' in definedParmCollection.get(name,{}):
            destinationFolderName = definedParmCollection.get(name,{}).get('folder',foldername)
            destinationFolder = ptg.find(destinationFolderName)
            if destinationFolder:
                manualindices = ptg.findIndices(destinationFolder)
            else:
                # Check if the destination folder for the parameter has a preexisting template, or if it should use the default configuration
                if destinationFolderName in folder_templates:
                    # Check if a parent folder was specified and target it instead of the default folder
                    parentfolder = definedFolderCollection[destinationFolderName].get('parent_folder','')
                    if parentfolder:
                        # Since a parent folder was specified, confirm it's existence
                        parentfolder = ptg.find(parentfolder)
                        if not parentfolder:
                            # Fallback to the standard folder. Automatically constructing a parent folder from here seems like a recursive nightmare.
                            print("Parent folder for "+destinationFolderName+" does not exist. Using default folder instead.")
                            parentfolder = ptg.find(foldername)
                    else:
                        # Default to the standard folder if no parent is specified
                        parentfolder = ptg.find(foldername)
                    folderTemplate= folder_templates[destinationFolderName]
                else:
                    parentfolder = foldername
                    folderTemplate = hou.FolderParmTemplate(
                        destinationFolderName, 
                        destinationFolderName.title().replace("_", " "),
                        folder_type=hou.folderType.Simple,
                    )
                # Append the new folder to it's parent folder (either defined or the default) and output it's indices
                ptg.appendToFolder(ptg.findIndices(parentfolder), folderTemplate)
                manualindices = ptg.findIndices(folderTemplate)
        else:
            manualindices = ptg.findIndices(foldername)

        if name in definedFolderCollection:
            # The existing parameter is a folder, assume this parameter is reading a value from it
            continue
        else:
            exparm = node.parm(name) or node.parmTuple(name)
            if exparm:
                ptg.replace(name, template)
            else:
                ptg.appendToFolder(manualindices, template)
    node.setParmTemplateGroup(ptg)

# This adds support for inline hscript ch calls for use in OpenCL, (this is most useful for compiler overrides, though generally as a last resort)
def _hscriptRefsFromChCalls(node, code, definedParmCollection, adlMetadata):
    # Remove comments
    code = comment_or_string_exp.sub(remove_comments, code)

    # Loop over the channel refs found in the VEX, work out the corresponding
    # template type, remember for later (we might need to check first if the
    # user wants to replace existing parms).
    refs = []
    existing = []
    foundnames = set()
    for match in chcall_exp.finditer(code):
        call = match.group(1)
        name = match.group(2)[1:-1]

        # If the same parm shows up more than once, only track the first
        # case.  This avoids us double-adding since we delay actual
        # creation of parms until we've run over everything.
        if name in foundnames:
            continue
        foundnames.add(name)
        
        size = ch_size.get(call, 1)
        label = name.title().replace("_", " ")

        if name not in definedParmCollection:
            if call == "chs":
                template = hou.StringParmTemplate(name, label, size)
            elif call == "chf":
                template = hou.FloatParmTemplate(name, label, size, min=0, max=1)
            else:
                template = hou.IntParmTemplate(name, label, size)

        else:
            # If a corresponding setting collection is found, make use of the parameter configuration system
            adlParmSettings = definedParmCollection[name]
            tm = _adlTemplateMaker(adlParmSettings, name, label, size)

            if 'template' in adlParmSettings:
                # If enabled, this uses the template string to decide which class is used, with args and kwargs being taken directly from the dictionary (if they exist)
                template = tm.makeDirect()

            else:
                tm.getCommonSettings()

                if adlParmSettings.get('is_toggle',0):
                    template = tm.makeToggle()

                else:
                    # If not using manual template definition and there is not an appropriate type, use the existing template categorization
                    if call == "chs":
                        template = tm.makeString()
                    elif call == "chf":
                        template = tm.makeFloat()
                    else:
                        template = tm.makeInteger()
                    
            # Apply any hidewhen conditions, since they can't be set directly in the ParmTemplate arguments
            if 'hide_when' in adlParmSettings:
                template.setConditional(hou.parmCondType.HideWhen, tm.hide_when) 


        exparm = node.parm(name) or node.parmTuple(name)
        if exparm:
            if not exparm.isSpare():
                # The existing parameter isn't a spare, so just skip it
                continue
            if adlMetadata.get('replaceall',0) or definedParmCollection.get(name,{}).get('replace',0):
                # Parameter replacing has been enabled for either the current parameter, or the entire snippet
                refs.append((name, template))
            else:
                extemplate = exparm.parmTemplate()
                etype = extemplate.type()
                ttype = template.type()
                if (
                    etype != ttype or
                    extemplate.numComponents() != template.numComponents() or
                    (ttype == hou.parmTemplateType.String and
                    extemplate.stringType() != template.stringType())
                ):
                    # The template type is different, remember the name and template
                    # type to replace later
                    existing.append((name, template))
                else:
                    # No difference in template type, we can skip this
                    continue
        else:
            # Remember the parameter name and template type to insert later
            refs.append((name, template))

    # If there are existing parms with the same names but different template
    # types, ask the user if they want to replace them
    if existing:
        exnames = ", ".join(f'"{name}"' for name, _ in existing)
        if len(existing) > 1:
            msg = f"Parameters {exnames} already exist, replace them?"
        else:
            msg = f"Parameter {exnames} already exists, replace it?"
        result = hou.ui.displayCustomConfirmation(
            msg, ("Replace", "Skip Existing", "Cancel"), close_choice=2,
            title="Replace Existing Parameters?",
            suppress=hou.confirmType.DeleteSpareParameters,
        )
        if result == 0:  # Replace
            refs.extend(existing)
        elif result == 2:  # Cancel
            return
    
    return refs
    


# This subsitution function replaces comments with spaces and leaves strings
# alone. This has the effect of skipping over strings so it doesn't get confused
# by comment characters inside a string.
def remove_comments(match):
    s = match.group(0)
    if s.startswith('/'):
        return ' '
    else:
        return s

def _addSpareParmsToStandardFolder(node, parmname, refs):
    """
    Takes a list of (name, template) in refs and injects them into the
    standard-named folder for generated parms.  If it doesn't exist,
    create the folder and place before parmname.
    """
    if not refs:
        return          # No-op

    # We consider a multiparm any parameter with a number in it.
    # This might have false positives, but it is important to not try
    # to create a parameter before a multiparm as that slot
    # won't exist.  We also use a single standard folder name
    # for all the multiparm snippets.
    ismultiparm = any(map(str.isdigit, parmname))

    ptg = node.parmTemplateGroup()
    foldername = 'folder_generatedparms_' + parmname
    if ismultiparm:
        foldername = 'folder_generatedparms'

    folder = ptg.find(foldername)
    if not folder:
        folder = hou.FolderParmTemplate(
            foldername,
            "Generated Channel Parameters",
            folder_type=hou.folderType.Simple,
        )
        folder.setTags({"sidefx::look": "blank"})
        if not ismultiparm:
            ptg.insertBefore(parmname, folder)
        else:
            ptg.insertBefore(ptg.entries()[0], folder)

    # Insert/replace the parameter templates
    indices = ptg.findIndices(folder)
    for name, template in refs:
        exparm = node.parm(name) or node.parmTuple(name)
        if exparm:
            ptg.replace(name, template)
        else:
            ptg.appendToFolder(indices, template)
    node.setParmTemplateGroup(ptg)

def createSpareParmsFromOCLBindings(node, parmname):
    """ 
    Parse the @BIND commands in an OpenCL kernel and create corresponding
    spare parameters
    """
    parm = node.parm(parmname)
    code = parm.evalAsString()

    # Use unexpanded string for the following, so that behaviour is identical to VEX
    code_unexpanded = parm.unexpandedString()

    # Extract parameter metadata dictionary
    adlMetadata = _getAdlSettings(code_unexpanded,_adlMetaPrefix, '', 0)
    if adlMetadata.get('disable_all',0):
        # Bypass all setting gathering if disable_all is true
        definedParmCollection = {}
        definedFolderCollection = {}
    else:
        # Extract a dictionary of any existing parameter settings
        definedParmCollection = _getAdlSettings(code_unexpanded, '\ ', 'parm', 0) | _getAdlSettings(code_unexpanded, _adlParmPrefix, 'parm', 0)
        definedFolderCollection = _getAdlSettings(code_unexpanded, _adlFolderPrefix, 'name', 0)

    # Extract bindings
    bindings = hou.text.oclExtractBindings(code)

    channellinks = []
    ramplinks = []
    refs = []

    iscop = False
    # To allow for this script to be backwards-compatible with Houdini versions < 20.5, only check for Cops in certain cases
    houversion = hou.applicationVersion()
    if houversion[0]+(houversion[1]/10) >= 20.5:
        if node.type().category() == hou.copNodeTypeCategory():
            iscop = True

    # Sadly, SOP and DOP opencl have completely different
    # binding names.  Use the base bindings type to differntiate
    if node.parm('bindings') is not None:
        # SOP based (also COP)
        bindparm = 'bindings'
        bindparmprefix = 'bindings'
        bindparmsuffix = {
            'name' : '_name',
            'type'   : '_type',
            'ramp' : '_ramp',
            'ramptype' : '_ramptype',
            'rampsize' : '_rampsize',
            'layertype' : '_layertype',
            'layerborder' : '_layerborder',
            'volume' : '_volume',
            'geometry' : '_geometry',
            'input' : '_input',
            'portname' : '_portname',
            'vdbtype' : '_vdbtype',
            'forcealign' : '_forcealign',
            'resolution' : '_resolution',
            'voxelsize' : '_voxelsize',
            'xformtoworld' : '_xformtoworld',
            'xformtovoxel' : '_xformtovoxel',
            'attribute' : '_attribute',
            'attribclass' : '_attribclass',
            'attribtype' : '_attribtype',
            'attribsize' : '_attribsize',
            'precision' : '_precision',
            'readable' : '_readable',
            'writeable' : '_writeable',
            'optional' : '_optional',
            'defval' : '_defval',
            'timescale' : '_timescale',
            'intval' : '_intval',
            'fval'   : '_fval',
            'v2val'  : '_v2val',
            'v3val'  : '_v3val',
            'v4val'  : '_v4val',
            }
    elif node.parm('paramcount') is not None:
        # DOP based
        bindparm = 'paramcount'
        bindparmprefix = 'parameter'
        bindparmsuffix = {
            'name' : 'Name',
            'type'   : 'Type',
            'ramp' : 'Ramp',
            'rampsize' : 'RampSize',
            'volume' : 'Volume',
            'geometry' : 'Geometry',
            'input' : None,
            'portname' : None,
            'vdbtype' : None,
            'forcealign' : None,
            'resolution' : 'Resolution',
            'voxelsize' : 'VoxelSize',
            'xformtoworld' : 'XformToWorld',
            'xformtovoxel' : 'XformToVoxel',
            'attribute' : 'Attribute',
            'attribclass' : 'Class',
            'attribtype' : 'AttributeType',
            'attribsize' : 'AttributeSize',
            'precision' : 'Precision',
            'readable' : 'Input',
            'writeable' : 'Output',
            'optional' : 'Optional',
            'defval' : 'DefVal',
            'timescale' : 'TimeScale',
            'intval' : 'Int',
            'fval'   : 'Flt',
            'v2val'  : 'Flt2',
            'v3val'  : 'Flt3',
            'v4val'  : 'Flt4',
        }
    else:
        # Unknown
        pass

    inputs = node.parm('inputs')
    outputs = node.parm('outputs')

    # Add any inline hscript refs
    refs = refs + _hscriptRefsFromChCalls(node, code_unexpanded, definedParmCollection, adlMetadata)

    # Loop over each binding to see if it exists on explicit bindings,
    # if not add it.
    for binding in bindings:
        isgeo = binding['type'] in ('attribute', 'volume', 'vdb')
        islayer = binding['type'] == 'layer'

        # Search our node's bindings...
        numbind = node.parm(bindparm).evalAsInt()
        found = False
        for i in range(1, numbind+1):
            name = node.parm(bindparmprefix + str(i) + bindparmsuffix['name']).evalAsString()
            if name == binding['name']:
                found = True
                break
        if not found:
            requiresparm = False
            tuplesize = 1
            isint = False
            isramp = False

            # Add to our list if we should have spare parms...
            if binding['type'] in ('int', 'float', 'float2', 'float3', 'float4'):
                requiresparm = True
                if binding['type'] == 'int':
                    isint = True
                if binding['type'] == 'float2':
                    tuplesize = 2
                    # Only cops supports v2
                    if not iscop:
                        requiresparm = False
                if binding['type'] == 'float3':
                    tuplesize = 3
                if binding['type'] == 'float4':
                    tuplesize = 4

            # If it is optional and has a defval we want to
            # trigger it
            if isgeo and binding['readable'] and binding['optional'] and binding['defval']:
                requiresparm = True
                # Some cases we don't support...
                if binding['type'] == 'attribute':
                    if binding['attribtype'] == 'floatarray' or binding['attribtype'] == 'intarray':
                        requiresparm = False
                    elif binding['attribtype'] == 'int':
                        isint = True
                        if binding['attribsize'] != 1:
                            requiresparm = False
                    elif binding['attribtype'] == 'float':
                        tuplesize = binding['attribsize']
                        if tuplesize not in (1, 3, 4):
                            requiresparm = False

            # extraparm does not work for layer, and may not be wanted
            # if islayer and binding['readable'] and binding['optional'] and binding['defval']:
            #    requiresparm = True

            if binding['type'] == 'ramp':
                isramp = True
                requiresparm = True
                ramptype = hou.rampParmType.Color
                if binding['ramptype'] == 'float':
                    ramptype = hou.rampParmType.Float

            name = binding['name']
            label = name.title().replace("_", " ")
            if requiresparm:
                # We want to avoid conflict with existing OpenCL parms.
                # we have no need to exactly match as the source isn't a
                # ch("") like it is in VEX.
                internalname = name + '_val'

                # In cops we have prefixed internal parms so we don't
                # have to worry about conflicts so much, but we want to
                # fall back to _val if that already existed.
                exparm = node.parm(internalname) or node.parmTuple(internalname)
                if not exparm and iscop:
                    internalname = name

                if name not in definedParmCollection:
                    if isramp:
                        template = hou.RampParmTemplate(internalname, label, ramptype)
                    elif isint:
                        template = hou.IntParmTemplate(internalname, label, tuplesize)
                    else:
                        template = hou.FloatParmTemplate(internalname, label, tuplesize, min=0, max=1)
                else:
                    # If a corresponding setting collection is found, make use of the parameter configuration system
                    adlParmSettings = definedParmCollection[name]
                    tm = _adlTemplateMaker(adlParmSettings, internalname, label, tuplesize)

                    if 'template' in adlParmSettings:
                        # If enabled, this uses the template string to decide which class is used, with args and kwargs being taken directly from the dictionary (if they exist)
                        template = tm.makeDirect()

                    else:
                        tm.getCommonSettings()
            
                        if adlParmSettings.get('is_toggle',0):
                            template = tm.makeToggle()

                        else:
                            # If not using manual template definition and there is not an appropriate type, use the existing template categorization
                            if isramp:
                                if ramptype == hou.rampParmType.Float:
                                    template = tm.makeRamp()
                                else:
                                    template = tm.makeColorRamp()
                            elif isint:
                                template = tm.makeInteger()
                            else:
                                template = tm.makeFloat()

                    # Apply any hidewhen conditions, since they can't be set directly in the ParmTemplate arguments
                    if 'hide_when' in adlParmSettings:
                        template.setConditional(hou.parmCondType.HideWhen, tm.hide_when) 

                # Check if we have an existing parm.
                # note the user may have removed an explicit binding,
                # but left the existing parm, in this case we'll link
                # to that...
                exparm = node.parm(internalname) or node.parmTuple(internalname)
                if not exparm:
                    refs.append((internalname, template))

                # Create our new binding...
                node.parm(bindparm).set(numbind+1)
                numbind += 1

                # Write back our binding values...
                for key in bindparmsuffix:
                    if bindparmsuffix[key] is None:
                        continue
                    if key in ('intval', 'fval', 'v2val', 'v3val', 'v4val', 'v4bval', 'm4val', 'ramp'):
                        continue
                    keyparmname = bindparmprefix + str(numbind) + bindparmsuffix[key]
                    parm = node.parm(keyparmname) or node.parmTuple(keyparmname)
                    if parm: parm.set(binding[key])
                if isramp:
                    s = '_ramp_rgb' if ramptype == hou.rampParmType.Color else bindparmsuffix['ramp']
                    ramplinks.append(( internalname, bindparmprefix + str(numbind) + s))
                else:
                    if isint:
                        t = 'intval'
                    elif tuplesize == 1:
                        t = 'fval'
                    else:
                        t = 'v%dval' % tuplesize
                    channellinks.append(( internalname,  bindparmprefix + str(numbind) + bindparmsuffix[t], binding[t]))

        if inputs is not None and (binding['readable'] or (not binding['readable'] and not binding['writeable'])) and (isgeo or islayer):
            num = inputs.evalAsInt()
            found = False
            lookupname = binding['portname']
            if lookupname == '':
                lookupname = binding['name']
            for i in range(1, num+1):
                name = node.parm('input' + str(i) + '_name').evalAsString()
                if name == lookupname:
                    found = True
                    break
            if not found:
                inputs.set(num+1)
                i = num+1
                node.parm('input' + str(i) + '_name').set(lookupname)
                if isgeo:
                    layertype = 'geo'
                else:
                    if not binding['readable'] and not binding['writeable']:
                        layertype = 'metadata'
                    else:
                        layertype = binding['layertype']
                if layertype == 'float?': layertype = 'floatn'
                node.parm('input' + str(i) + '_type').set(layertype)
                node.parm('input' + str(i) + '_optional').set(binding['optional'])

        if outputs is not None and binding['writeable'] and (isgeo or islayer):
            num = outputs.evalAsInt()
            found = False
            lookupname = binding['portname']
            if lookupname == '':
                lookupname = binding['name']
            for i in range(1, num+1):
                name = node.parm('output' + str(i) + '_name').evalAsString()
                if name == lookupname:
                    found = True
                    break
            if not found:
                outputs.set(num+1)
                i = num+1
                node.parm('output' + str(i) + '_name').set(lookupname)
                layertype = 'geo' if isgeo else binding['layertype']
                if layertype == 'float?': layertype = 'floatn'
                node.parm('output' + str(i) + '_type').set(layertype)

    # add an unbound input to provide output layer size
    if inputs is not None and outputs is not None and not inputs.evalAsInt() and outputs.evalAsInt():
        inputs.set(1)
        node.parm('input1_name').set('')
        node.parm('input1_optional').set(True)

    # Completed the binding loop, we've extended our bindings to have
    # all the new explicit bindings that we think need parms and build
    # a refs list of them.  channellinks has triples of how we want
    # to then re-link, which we can do after the refs are built.
    _adlAddSpareParmsToStandardFolder(node, parmname, refs, definedParmCollection, definedFolderCollection, adlMetadata)

    for (internalname, srcname, value) in channellinks:
        parm = node.parm(internalname) or node.parmTuple(internalname)
        if parm:
            parm.set(value)
            srcparm = node.parm(srcname) or node.parmTuple(srcname)
            if srcparm: srcparm.set(parm)

    for (internalname, srcname) in ramplinks:
        parm = node.parm(internalname) or node.parmTuple(internalname)
        lin = hou.rampBasis.Linear
        if parm: parm.set(hou.Ramp((lin, lin),(0,1),(0,1)))
        srcparm = node.parm(srcname) or node.parmTuple(srcname)
        # Link the point count
        if srcparm: srcparm.setExpression("ch('" + internalname + "')")
        # Setup opmultiparms
        cmd = 'opmultiparm ' + node.path() + ' "' + srcname + '#pos" "' + internalname + '#pos" "' + srcname + '#value" "' + internalname + '#value" "' + srcname + '#interp" "' + internalname + '#interp" "' + srcname + '#cr" "' + internalname + '#cr" "' + srcname + '#cg" "' + internalname + '#cg" "' + srcname + '#cb" "' + internalname + '#cb"'
        (res, err) = hou.hscript(cmd)

        # Manually link already exisiting parms
        # this should be evalAsInt, but for some reason that is still
        # 1 at this point?
        npt = 2 # parm.evalAsInt()
        for i in range(npt):
            node.parm(srcname + str(i+1) + 'pos').set(node.parm(internalname + str(i+1) + 'pos'))
            node.parm(srcname + str(i+1) + 'interp').set(node.parm(internalname + str(i+1) + 'interp'))
            x = node.parm(internalname + str(i+1) + 'value')
            if x:
                node.parm(srcname + str(i+1) + 'value').set(x)
            else:
                node.parm(srcname + str(i+1) + 'cr').set(node.parm(internalname + str(i+1) + 'cr'))
                node.parm(srcname + str(i+1) + 'cg').set(node.parm(internalname + str(i+1) + 'cg'))
                node.parm(srcname + str(i+1) + 'cb').set(node.parm(internalname + str(i+1) + 'cb'))

    # no need to dirty an opencl node as we affected cooking parmeters
    # when we updated bindings.

def createSpareParmsFromChCalls(node, parmname):
    """
    For each ch() call in the given parm name, create a corresponding spare
    parameter on the node.
    """

    parm = node.parm(parmname)
    original = parm.unexpandedString()
    simple = True
    if len(parm.keyframes()) > 0:
        # The parm has an expression/keyframes, evaluate it to the get its
        # current value
        code = parm.evalAsString()
        simple = False
    else:
        code = original.strip()
        if len(code) > 2 and code.startswith("`") and code.endswith("`"):
            # The whole string is in backticks, evaluate it
            code = parm.evalAsString()
            simple = False


    # Extract parameter metadata dictionary
    adlMetadata = _getAdlSettings(code,_adlMetaPrefix, '', 0)
    if adlMetadata.get('disable_all',0):
        # Bypass all setting gathering if disable_all is true
        definedParmCollection = {}
        definedFolderCollection = {}
    else:
        # Extract a dictionary of any existing parameter settings
        definedParmCollection = _getAdlSettings(code, '\ ', 'parm', 1) | _getAdlSettings(code, _adlParmPrefix, 'parm', 1)
        definedFolderCollection = _getAdlSettings(code, _adlFolderPrefix, 'name', 0)


    # Remove comments
    code = comment_or_string_exp.sub(remove_comments, code)

    # Loop over the channel refs found in the VEX, work out the corresponding
    # template type, remember for later (we might need to check first if the
    # user wants to replace existing parms).
    refs = []
    existing = []
    foundnames = set()
    for match in chcall_exp.finditer(code):
        call = match.group(1)
        name = match.group(2)[1:-1]

        # If the same parm shows up more than once, only track the first
        # case.  This avoids us double-adding since we delay actual
        # creation of parms until we've run over everything.
        if name in foundnames:
            continue
        foundnames.add(name)
        
        size = ch_size.get(call, 1)
        label = name.title().replace("_", " ")

        if name not in definedParmCollection:
            if call in ("vector(chramp", "vector(chrampderiv"):
                # Result was cast to a vector, assume it's a color
                template = hou.RampParmTemplate(name, label, hou.rampParmType.Color)
            elif call in ("chramp", "chrampderiv"):
                # No explicit cast, assume it's a float
                template = hou.RampParmTemplate(name, label, hou.rampParmType.Float)
            elif call == "chs":
                template = hou.StringParmTemplate(name, label, size)
            elif call == "chsop":
                template = hou.StringParmTemplate(
                    name, label, size, string_type=hou.stringParmType.NodeReference)
            elif call == "chi":
                template = hou.IntParmTemplate(name, label, size)
            elif call == "chdict":
                template = hou.DataParmTemplate(
                    name, label, size,
                    data_parm_type=hou.dataParmType.KeyValueDictionary
                )
            else:
                template = hou.FloatParmTemplate(name, label, size, min=0, max=1)

        else:
            # If a corresponding setting collection is found, make use of the parameter configuration system
            adlParmSettings = definedParmCollection[name]
            tm = _adlTemplateMaker(adlParmSettings, name, label, size)

            if 'template' in adlParmSettings:
                # If enabled, this uses the template string to decide which class is used, with args and kwargs being taken directly from the dictionary (if they exist)
                template = tm.makeDirect()

            else:
                tm.getCommonSettings()
    
                if adlParmSettings.get('is_toggle',0):
                    template = tm.makeToggle()

                else:
                    # If not using manual template definition and there is not an appropriate type, use the existing template categorization
                    if call in ("vector(chramp", "vector(chrampderiv"):
                        template = tm.makeColorRamp()
                    elif call in ("chramp", "chrampderiv"):
                        # No explicit cast, assume it's a float
                        template = tm.makeRamp()
                    elif call == "chs":
                        template = tm.makeString()
                    elif call == "chsop":
                        template = tm.makeNodeString()
                    elif call == "chi":
                        template = tm.makeInteger()
                    elif call == "chdict":
                        template = tm.makeDict()
                    else:
                        template = tm.makeFloat()
                  
            # Apply any hidewhen conditions, since they can't be set directly in the ParmTemplate arguments
            if 'hide_when' in adlParmSettings:
                template.setConditional(hou.parmCondType.HideWhen, tm.hide_when)  


        exparm = node.parm(name) or node.parmTuple(name)
        if exparm:
            if name in definedFolderCollection:
                # The existing parameter is a folder, assume this parameter is reading a value from it
                continue
            if not exparm.isSpare():
                # The existing parameter isn't a spare, so just skip it
                continue
            if adlMetadata.get('replaceall',0) or definedParmCollection.get(name,{}).get('replace',0):
                # Parameter replacing has been enabled for either the current parameter, or the entire snippet
                refs.append((name, template))
            else:
                extemplate = exparm.parmTemplate()
                etype = extemplate.type()
                ttype = template.type()
                if (
                    etype != ttype or
                    extemplate.numComponents() != template.numComponents() or
                    (ttype == hou.parmTemplateType.String and
                    extemplate.stringType() != template.stringType())
                ):
                    # The template type is different, remember the name and template
                    # type to replace later
                    existing.append((name, template))
                else:
                    # No difference in template type, we can skip this
                    continue
        else:
            # Remember the parameter name and template type to insert later
            refs.append((name, template))

    # If there are existing parms with the same names but different template
    # types, ask the user if they want to replace them
    if existing:
        exnames = ", ".join(f'"{name}"' for name, _ in existing)
        if len(existing) > 1:
            msg = f"Parameters {exnames} already exist, replace them?"
        else:
            msg = f"Parameter {exnames} already exists, replace it?"
        result = hou.ui.displayCustomConfirmation(
            msg, ("Replace", "Skip Existing", "Cancel"), close_choice=2,
            title="Replace Existing Parameters?",
            suppress=hou.confirmType.DeleteSpareParameters,
        )
        if result == 0:  # Replace
            refs.extend(existing)
        elif result == 2:  # Cancel
            return

    _adlAddSpareParmsToStandardFolder(node, parmname, refs, definedParmCollection, definedFolderCollection, adlMetadata)

    if refs:
        if simple:
            # Re-write the contents of the snippet so the node will re-run the
            # VEX and discover the new parameters.
            # (This is really a workaround for a bug (#123616), since Houdini
            # should ideally know to update VEX snippets automatically).
            parm.set(original)



