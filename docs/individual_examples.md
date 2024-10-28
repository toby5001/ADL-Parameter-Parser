# Individual Examples
The following are a series of VEX snippets which demonstrate different aspect of the parser's functionality. I'd recommend pasting them into a wrangle and seeing what happens. OpenCL is also supported, and the parser's syntax is identical. In addition to any functionality you see here, any functionality you see on a ParmTemplate's documentation page is also supported.
# Table of Contents
- [Common Arguments](#common-arguments)
- [Parameter Targeting](#parameter-targeting)
- [Toggle Parameters](#toggle-parameters)
- [Menu Parameters](#menu-parameters)
- [Presets](#presets)
- [Limits](#limits)
- [Visibility](#visibility)
- [Conditional Visibility](#conditional-visibility)
- [Folders](#folders)
    - [Independent Folders](#independent-folders)
    - [Parent Folders](#parent-folders)
- [Expressions](#expressions)
- [Help](#help)
- [Tags](#tags)
- [Direct Template Specification](#direct-template-specification)
- [Direct Kwargs](#direct-kwargs)
- [Metadata (Overall Parser Controls)](#metadata)
## Common arguments
In it's simplest form, the parser can be used to set default, min, and max values.
```
v@P += chv('offset1'); // [[ default=2 ]]
v@P += chv('offset2'); // [[ default=(1,2,3) ]]
v@P.y += chf('offset2'); // [[ default=1.5, min=-2, max=2, min_is_strict=1 ]]
```

## Parameter targeting
###### :warning: ***Parameters MUST be explicitly defined in OpenCL, as it uses a different way of specifying parameters.***
```
// This will result in standard sliders for x_offset and z_offset, with a custom default and maximum value for y_offset.
v@P.x += chf('x_offset');
v@P.y += chf('y_offset'); // [[ default=2, max=4 ]]
v@P.z += chf('z_offset');
// If a specific parm is not specified in brackets, it will look for the nearest parameter reference before it in the code.
```
```
// Alternatively, you can directly declare a target parameter
v@P.x += chf('x_offset');
v@P.y += chf('y_offset');
v@P.z += chf('z_offset');
// [[ parm=x_offset, default=1, min=-3, max=3]]
// [[ parm=z_offset, default=2.3, min=-3, max=3]]
```

## Toggle parameters
It is fairly common to want to treat an integer parameter as a boolean to be toggled in the interface. This tells the parser to treat the current parameter as a toggle parameter instead of whatever it's standard parameter template might be.
```
// The following will create a toggle parameter instead of a standard int
if(chi('enable_offset')){ // [[is_toggle]]
    v@P.y += 2;
}
```

## Menu parameters
Menu parameters will automatically be created if a relevant menu argument is specified for either a string or int parameter. You can either specify `menu_items` and `menu_labels` separately (or just `menu_items` alone), or as a `menu_pairs` dict. You can also specify things like item generators and icons. See the documentation for [StringParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/StringParmTemplate.html) or [IntParmTemplate](https://www.sidefx.com/docs/houdini/hom/hou/IntParmTemplate.html) for more information.
```
string bark_type = chs('bark_type'); // [[ menu_items=('elm','oak'), menu_labels=('Elm Tree','Oak Tree') ]]
// For strings, default values are one of the menu_items, while it is an index for ints
string wood_type = chs('wood_type'); // [[ default=oak, menu_pairs={'elm':'Elm Tree','oak':'Oak Tree'} ]]
int branch_type = chi('branch_type'); // [[ default=1, menu_items=('Elm Tree','Oak Tree')]]
```

## Presets
For a few common usecases, there are presets which can be specified that populate the appropriate tags and arguments for complex parameters.
- **attribSelect** (along with attribSelectFloat, attribSelectVector, attribSelectInt, and attribSelectString for only showing certain types)
    ```
    // attribSelect creates the appropriate tags and menu configurations needed to have an attribute selector and visualizer.
    string target_attribute = chs('attribute_to_modify'); // [[default=mask, preset=attribSelect]]
    ```
- **lopPrimSelect**
    ```
    // lopPrimSelect create the appropriate tags for a string parameter which autocompletes Solaris paths
    // with a primitive selection button as well
    string prim_to_read = chs('prim_to_read'); // [[ preset=lopPrimSelect ]]
    ```

## Limits
```
/* This will create a float slider, which locked to it's min and max values. */
v@P.y += chf('y_offset'); // [[ min=-2, max=2, min_is_strict=1, max_is_strict=1]]
```

## Visibility
```
/* This will create a toggle joined to a float slider,
    in addition to an invisible string parm. */
chs('object'); // [[is_hidden]]
if(chi('enable_offset') ){ // [[ is_toggle, is_label_hidden=1, join_with_next=1]]
    v@P.y += chf('y_offset');
}
```

## Conditional visibility
It is possible to specify disable_when and hide_when conditionals, which is especially useful when combined with menus, toggles, and folders.
```
// This is similar to the previous snippet, but the sliders have their visibility tied to the toggle.
if(chi('enable_offset') ){ // [[ is_toggle, is_label_hidden=1, join_with_next=1]]
    v@P.y += chf('y_offset'); // [[ disable_when='{ enable_offset != 1 }' ]]
    v@P.z += chf('z_offset'); // [[ hide_when='{ enable_offset != 1 }' ]]
}
```

## Folders
In addition to parameters, you can also define folders.\
If you simply define a folder in a parameter configuration through `[[folder=my_folder]]` without a separate folder configuration, a standard folder will be automatically created.
```
vector offset = chv('offset'); // [[ folder=offseting ]]
float mask = chf('offset_amount'); // [[ folder=offseting ]]
```
For more control, it is possible to specify a folder configuration in the same way as a parameter through `folder[[...]]`. These folder configurations will only be used if the folder is referenced in a parameter. See [Independent Folders](#independent-folders) below to change this.
```
// folder[[name=offsetting, folder_type=Collapsible, disable_when='{ enable_offset != 1 }' ]]
int enable_offset = chi('enable_offset'); // [[is_toggle,default=1]]
vector offset = chv('offset'); // [[ folder=offsetting ]]
float mask = chf('offset_amount'); // [[ folder=offsetting, min_is_strict=1, max_is_strict=1 ]]
v@P += offset*mask;
```

### Independent Folders
By default, folders are only constructed if they appear in a specific parameter, but they can be set to be created independent of (and before) the parameters. Independent folders will be placed in the order they are found, NOT the order they are used in bracketed settings. Try disabling the independent argument to see the different behavior.
```
// folder[[name=empty_folder, independent=1, folder_type=RadioButtons ]]
// It is also possible to specify parent folders, though be cautious about the order they are called.
// folder[[name=main_config, independent=1, folder_type=Tabs, parent_folder=containing_folder]]
// folder[[name=secondary_config, independent=1, folder_type=Tabs, parent_folder=containing_folder]]
chf('slider1'); // [[folder=main_config]]
```

### Parent Folders
It is also possible to specify parent folders, though be cautious about the order they are called, as the script will only do so much to resolve paren't folders that don't already exist. In scenarios with complex nested folders, it can be best to specify the root folder as independent so that you can be sure of the order they will be brought in.
```
// folder[[name=containing_folder, independent=1, folder_type=RadioButtons ]]
// It is also possible to specify parent folders, though be cautious about the order they are called.
// folder[[name=main_config, independent=1, folder_type=Tabs, parent_folder=containing_folder]]
// folder[[name=secondary_config, independent=1, folder_type=Tabs, parent_folder=containing_folder]]
chf('slider1'); // [[folder=main_config]]
```

## Expressions
It is possible to specify default expressions, which can be simple parameter references, or complex multi-line code snippets themselves
```
float mask = chf('mask'); // [[ min=-1, default_expression='sin(deg($T*0.25*$PI))' ]]
```
```
float val1 = chf('val1');
float mask = chf('mask');
/* 
[[ default_expression_language=Python, default_expression=
'''import math
output = math.sin( hou.time() )
return output''']]
*/
```

## Help
As with the rest of the paramter parser, both single-line or multi-line strings are supported.
```
v@P.y += sin(@P.x*M_PI*chf('freq'))*chf('amp');
// [[parm=freq, max=5, help='The density with which the function moves between -1 and 1]]
/* [[parm=amp, min=-2,max=-2,help=
"""This controls the overal amplitude of the function,
or in this case how much the y position is displaced up and down.
"""]] */
```
## Tags
You are also able to directly specify parameter tags as a dictionary, which can allow for some complex behavior.
```
chf('float_slider'); // [[ max=10, tags={'sidefx::slider':'snap_to_int'} ]]
```

## Direct Template Specification
For the most control (and complexity) you can specify a parameter template, which will override all the automatic template selection and default values that the parser normaly does. It is highly recomended to explicitly specify your arguments as well, as they can vary across templates.
```
chf('float_one');
chi('sep'); // [[template='SeparatorParmTemplate', args=('sep',), kwargs={} ]]
chf('button_one');
/* [[template='ButtonParmTemplate',args=('button_one','Button One'), 
kwargs={'script_callback':"print('Click!')",'tags':{'script_callback_language':'python'} } ]] */
```

## Direct Kwargs
If you want to use a part of a ParmTemplate that isn't already supported, or just want to directly specify things yourself, it is possible to pass Kwargs directly into a template, which will override any default or otherwise defined arguments. This should be written as a python-style dictionary.
```
chf('slider'); // [[ min=1,max=4,default=2, kwargs={'default_value':(3.5,), 'script_callback':"print('test',1+2)" } ]]
```

## Metadata
There are also a few settings which you might want to define for your entire script using `meta[[...]]`, including the ability to disable the enhanced parser altogether (disable_all). This is useful for seeing how the parameters will be created if you don't have the script installed. By default, the parser will not modify parameters that already exist, but this can be changed with the replace_all setting. NOTE: Replace does not effect folders, as updating their position and dependencies is a headache I didn't feel was necessary.
```
// Try changing the disableall setting to see the difference!
// meta[[ disable_all=1, replace_all=1 ]]
chf('slider'); // [[min=-3.2,max=5,default=2]]
```