# ADL Parameter Parser

This is a drop-in replacement for Houdini's vexpressionmenu.py which adds support for simple (and complex!) in-line parameter specification (similar to OSL). The script is compatible with VEX and OpenCL and will work anywhere that the "Create Spare Parameters" button can be found (it's that little plus button next to most code blocks).

![](docs/media/demo-adl_mxPost.gif)

The idea of this script is to fufill a similar purpose to OSL, where you might have a piece of code that you use often, but that doesn't need a complex asset surrounding it. This allows for a complete interface to be specified within your code, which can be transported through a simple copy and paste. While the initial intent of this script was just to have an easy way to set a min and max value (and a toggle isntead of an integer slider), it supports *all* aspects of a parameter template, meaning that you can build truly complex interfaces.

# Full Snippet Examples
The fastest way to see what you can do with the parser is to see it in use. A majority of my own larger snippets have been created with this parser in mind, and use a large amount of the functionality: [Houdini Snippets Repo](https://github.com/toby5001/Houdini-Snippets)

# Individual Argument Examples
Small snippets demonstrating individual parts of the parser can be found [here](docs/individual_examples.md).

# Overview
### Configuration
All configurations are specified within a set of double brackets. With no prefix, these are assumed to be for standard parameters,
but if they are led by either "folder" or "meta" you can specify folders or whole-snippet settings. You can either specify a specific parameter to target through `[[parm=my_parameter]]`, or allow the script to automatically find the closest parameter reference before it.\
###### :warning: ***Automatic parameter finding can only be done in VEX. They must be specifically declared in OpenCL.***
VEX Example:
```
v@P.y += chf('my_float'); // [[ max=6 ]]
// folder[[ name=my_folder, folder_type=Collapsible ]]
v@Cd = chv('color'); // [[default=0.5, folder=my_folder]]
```
###### :warning: ***Parameters are created in the order that they are found in the snippet and NOT in the order the parameter configurations are found.***
### Arguments
All arguments supported by a parameter template are supported here, so the best way to see a list of arguments is to check the documentation for the relevant ParmTemplate. For example, if you wanted to see what was available for a float parameter, any argument you see in the *\_\_init__* section [here](https://www.sidefx.com/docs/houdini/hom/hou/FloatParmTemplate.html) in SideFX's documentation can be used in your parameter specification.
### Differences/Additions to Python Equivalents
There are a few minor ease-of-use changes which have been made to how some parameters are defined, but they are generally identical. The three major differences are as follows:
1. Default values can be specified using a single value, instead of requiring a tuple (which can still be used). In addition, both `default` and `default_value` are both valid parameters and are treated the same. This applies to `default_expression` and `default_expression_language` as well.
2. When specifying a value that is a part of a class (like folder_type), you only should include the end portion as a string. This means that for a collapsible folder you would say `folder_type= Collapsible` instead of `folder_type= hou.folderType.Collapsible`
3. While paramter templates don't technically have a `hide_when` argument, they can be declared in the same way you might declare a `disable_when` argument.
4. To use a toggle parameter, specify `is_toggle` in your parameter configuration.

# Installation
Method 1 **(recommended)** - User Prefs Folder:\
 ``$USER_PREFS/pythonX.Xlibs`` (for example ``C:\Users\Andrew\Documents\houdini20.0\python3.10libs\vexpressionmenu.py``)\
Method 2 - Overwriting the original in directly in Houdini's core files:\
``$HFS\Houdini\pythonX.Xlibs`` (for example ``C:\Program Files\Side Effects Software\Houdini 20.0.688\houdini\python3.10libs``)

# Compatibility
This script is a modification of Houdini's own `vexpressionmenu.py` script. The script is kept up to date with the latest production version of `vexpressionmenu.py`. It has been tested in Houdini 20.5 (Python 3.11), Houdini 20.0 (Python 20.0), and Houdini 19.5 (Python 3.9) and is likely compatible with other versions.

# Changed Arguments and New Functionality
### Default Values
Default values can be specified using a single value, instead of requiring a tuple (which can still be used). In addition, both `default` and `default_value` are both valid parameters and are treated the same. This applies to `default_expression` and `default_expression_language` as well.
### Arguments with Class Values
When specifying an argument value that is a part of a class (like `folder_type`), you only should include the end portion as a string. This means that for a collapsible folder you would say `folder_type= Collapsible` instead of `folder_type= hou.folderType.Collapsible`
### hide_when Conditional 
While paramter templates don't technically have a `hide_when` argument, they can be declared in the same way you might declare a `disable_when` argument.
### Toggle Parameters
To use a toggle parameter, specify `is_toggle` in your parameter configuration. For more information and examples check [here](./docs/individual_examples.md/#toggle-parameters).
### Linking Folders and Parent Folders
It is possible to specify a folder within a parameter configuration for the parameter to be placed in (`[[folder=folder_name]]`). In addition, a parent folder can be specified within folder configurations (`folder[[parent_folder=folder_name]]`). For more information and examples check [here](./docs/individual_examples.md/#folders).

# All Standard Parameter Types
These are all of the parameter templates that are used for creating parameters. For a complete list of supported arguments, check the SideFX documentation for the relevant ParmTemplate that you need. The parser should support all of the arguments listed.
- [hou.FloatParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/FloatParmTemplate.html)
    - `ch("my_value")` - 1 float
    - `chf("my_value")` - 1 float
    - `chu("my_value")` - 2 floats
    - `chv("my_value")` - 3 floats
    - `chp("my_value")` - 4 floats
    - `ch2("my_value")` - 4 floats
    - `ch3("my_value")` - 9 floats
    - `ch4("my_value")` - 16 floats
    - `#bind parm my_value float` - 1 float
    - `#bind parm my_value float2` - 2 floats - ***COPs (Copernicus) only***
    - `#bind parm my_value float3` - 3 floats
    - `#bind parm my_value float4` - 4 floats
- [hou.IntParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/IntParmTemplate.html)
    - `chi("my_value")`
    - `#bind parm my_value int`
- [hou.StringParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/StringParmTemplate.html)
    - `chs("my_value")`
    - `chsop("my_value")` - ***Modification of standard string parameter***
- [hou.RampParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/RampParmTemplate.html)
    - `chramp("my_value")` - Float Ramp
    - `chrampderiv("my_value")` - Float Ramp
    - `vector(chramp("my_value"))` - Color Ramp
    - `vector(chrampderiv("my_value"))` - Color Ramp
    - `#bind ramp my_ramp float` - Float Ramp
    - `#bind ramp my_ramp float3` - Color Ramp
- [hou.DataParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/DataParmTemplate.html)
     - `chdict("my_value")`