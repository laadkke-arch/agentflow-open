# Pre-comment snapshot — not original edit history

Direct REST search returned 470 results, incomplete_results=false, first page 50. All first 40 human User accounts (none marked Bot, no admin-only titles); retained in order. No comments opened before this commit. Current body extracts, not original historical snapshot; author knowledge only provisional until edit timeline verified. `updated_at` includes activity, not proof of edit. Section snippets are verbatim public author text (omitted longer portions; raw endpoint above). For each row need and workaround are extracted by section heading, not inferred from outcome.

## #8764 — RichTextEdit Node
https://github.com/godotengine/godot-proposals/issues/8764 · 2024-01-01T11:46:20Z · current updated 2024-01-06T06:07:01Z

Need (excerpt): there is no node that allows the end user to edit RichText with formatting and and other more advanced features

Requested operation (excerpt): this would add great potential for godot to be used as a stand alone app development environment.
which I honostly think a lot of people including myself are using it for. 

Godot has great UI design elements and nodes. and is very simplistic to use. therefore I believe it's honestly one of the simplest ways for beginners, who don't know much about programming, to be able to make an application quite quickly and speedily.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8766 — Add support for creating interactable UIs in 3D space
https://github.com/godotengine/godot-proposals/issues/8766 · 2024-01-01T13:24:47Z · current updated 2025-05-29T08:11:24Z

Need (excerpt): I wanted to setup player interactable screen with few buttons on it (vis ref photo). 
![image](https://github.com/godotengine/godot-proposals/assets/62170918/38a314bb-42f0-4c38-80e8-cf0edeb1342d)
https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3I0MDVleTFxOTIwZm54dmFqZXprYmpqZzkycHluN200ZmJucjdkciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YdJAFlCWvyrKhIoFzp/giphy.gif

Requested operation (excerpt): Working on few mine learning projects in unreal, you were able to just draw 2D items (Widgets) into 3D space and when setting their collisions right, you were able to interact with them using raycasts.

I would like to have something like this in Godot as well. I saw the example project and though. Just having this like a node would be so much simpler.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8768 — Add support for AMD FSR 3 frame generation (currently, FSR 2.2 is supported)
https://github.com/godotengine/godot-proposals/issues/8768 · 2024-01-01T15:00:39Z · current updated 2026-11-12T08:07:16Z

Need (excerpt): Currently FSR 2 is in use, it has slightly worse upscaling and no Frame Generation.

Requested operation (excerpt): The biggest part of FSR 3 is Frame Generation support. It works surprisingly good even for games where it wasn't implemented by developers (and was added by modders). By data from real frames, it creates intermediate ones.

- It can almost double the original performance of the game (in CP2077, for example, it can turn 40 FPS into 70+)
- Which provides enough space for very demanding games (that are still going to work fast).
- It may be handy to use it only for 3D space and not UI-space (if pos

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8769 — Add the ability to copy images to clipboard
https://github.com/godotengine/godot-proposals/issues/8769 · 2024-01-01T20:48:06Z · current updated 2024-01-01T22:27:10Z

Need (excerpt): Currently, the class DisplayServer has clipboard_get() to get text, clipboard_set() to set text and clipboard_get_image() to get the image data from the clipboard, but doesn't have clipboard_set_image() for setting the image data to the clipboard. 
This prevents me from implementing the ability to quickly copy the image data from my tool to paste it in some other tool.

Requested operation (excerpt): Add clipboard_set_image() method to DisplayServer class to enable the ability to implement image copy/paste functionality. 
If some platform doesn't support this functionality, then do nothing / print a warning.

Workaround (excerpt): I haven't tested this method yet, but if it's possible, the only workaround is to create a C++ Dll / GDExtension, pass DisplayServer.WindowGetNativeHandle(DisplayServer.HandleType.WindowHandle) into it together with the image bytes, dimensions and encoding, and then implement the desired functionality with the help of WinAPI's winuser.h.
If this doesn't work, then the only option is to save the WIP texture into a file, then reload this file in the image editing app, then copy-paste it to your actual .psd project to work on it there. 
It's doable this way, but I expect my tool's users to transfer the WIP texture back and forth at least a few dozens to a few hundred times, so having the ability to directly copy/paste images would save them a lot of time and mental energy.

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8770 — Add HTTP/2 support to HTTPClient
https://github.com/godotengine/godot-proposals/issues/8770 · 2024-01-01T23:35:40Z · current updated 2024-05-12T22:40:27Z

Need (excerpt): The HTTPClient and its high-level node analog HTTPResponse only support HTTP/1.1 in the TCP implementation, which is used in all platforms except Web. While the API is serviceable and the implementation is functional, only supporting 1.1 places additional request processing load on web servers and can increase transaction latency.

Requested operation (excerpt): Minimally implement HTTP/2 support for TCP HTTPClient without changing the HTTPRequest node or the HTTPClient public interface.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8771 — Add binary `if` statement
https://github.com/godotengine/godot-proposals/issues/8771 · 2024-01-02T00:42:41Z · current updated 2025-07-30T06:33:32Z

Need (excerpt): sometimes a simple ``if`` statement (like ``if x: y()``) is short enough to fit on 1 line
but this is less readable, so i still put it across 2 lines.

when i try to type it in _binary if_ form (like the _trinary if_ but without the ``else``)
i am disappointed that it just gives an error:
``y() if x``

Requested operation (excerpt): the _binary if_ would be a goodly readable way to put a short ``if`` statement on just 1 line:
instead of
```GDScript
if x:
	y()
```
or the not recommended
```GDScript
if x: y()
```
i could type
```GDScript
y() if x
```

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8772 — Support a GDExtension that intentionally doesn't work with Windows `FreeLibrary`
https://github.com/godotengine/godot-proposals/issues/8772 · 2024-01-02T01:16:29Z · current updated 2024-01-16T19:08:47Z

Need (excerpt): When I write my GDExtension and hit "Reload Current Project" in the Godot editor, the GDExtension fails to start. This is because when you build a DLL with Go, it doesn't support FreeLibrary: https://github.com/golang/go/issues/11100. Supporting it isn't trivial and there don't appear to be plans to do so.

The sequence of events looks like this:

1. When the Godot editor on Windows starts for the first time:
    1. `GDExtension::open_library` copies my `libgdext.windows.x86_64.dll` to `~libgdext.windows.x86_64.dll`.  
        (https://github.com/godotengine/godot-cpp/issues/955)
    1. It loads `~libgdext.windows.x86_64.dll`.
1. I press "Reload Current Project":
    1. `GDExtension::close_library` calls `FreeLibrary` on `~libgdext.windows.x86_64.dll`, which **succeeds but does nothing** with my Go DLL.
    3. It tries to delete `~libgdex

Requested operation (excerpt): Make the new instance kill the old instance and wait until it's terminated before attempting GDExtension initialization.

<details><summary>Old approach, ~1foo.dll, ~2foo.dll, ... (click to open)</summary>

If `~foo.dll` can't be deleted, try `~1foo.dll`, `~2foo.dll`, and so on, until the file can either be deleted or doesn't already exist.

This won't change anything for normal GDExtensions: their filenames and cleanup will continue to behave the same. It only kicks in with GDExtension binaries

Workaround (excerpt): No external workaround.

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8773 — Add shader global include path support in ProjectSettings
https://github.com/godotengine/godot-proposals/issues/8773 · 2024-01-02T03:30:02Z · current updated 2024-01-05T00:51:29Z

Need (excerpt): I'm put my one common shaderinc file in `res://xd/shaderinc/comm.shaderinc`.
And in many shader I'm use it use `include "res://xd/shaderinc/comm.shaderinc"`.
But oneday, I want to remange my project, and move `res://xd/shaderinc/comm.shaderinc` to `res://xd/utils/shaderinc/comm.shaderinc`
And I found I must change all my shader file's line  `include "res://xd/shaderinc/comm.shaderinc"` to  `include "res://xd/utils/shaderinc/comm.shaderinc"`.
It will take much time, and future, if I want renamage, I must to to this work again.

Requested operation (excerpt): Add a `Shader Include Directiory` in `ProjectSettings`.
And I will set is to `res://xd/shaderinc`, and in shader file, I will change `include "res://xd/shaderinc/comm.shaderinc"` to `include "comm.shaderinc"`
Oneday I want renamage, I can only reset the `Shader Include Directiory` in `ProjectSettings`. All of the shader files not need change.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8774 — Add support for StringName in len function
https://github.com/godotengine/godot-proposals/issues/8774 · 2024-01-02T05:50:31Z · current updated 2024-01-02T14:17:28Z

Need (excerpt): len(&"test") throws an error, but is expected to return the length of the StringName, similar to how len("test") would show the length of the String. Strings and StringName can be used interchangeably in most other GDScript contexts however where len works for Strings, it does not work for StringNames.

Requested operation (excerpt): Update the GDScript len function to also support returning the length of a StringName.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8775 — Add a version of C# `GD.VarToBytes()` that uses Span instead of an array
https://github.com/godotengine/godot-proposals/issues/8775 · 2024-01-02T08:40:48Z · current updated 2024-01-03T15:01:08Z

Need (excerpt): `GD.BytesToVar` takes in a `Span` allowing the use of unsafe arrays, while `GD.VarToBytes` does not allow you to provide a Span to put data into. Instead, `GD.VarToBytes` internally allocates a safe array, forcing an unnecessary allocation. This can be important when using the method many times a second, as it can add unnecessary stress on the Garbage Collector.

Requested operation (excerpt): Add an overload for `GD.VarToBytes` that takes in a `Span` and a length, and returns `void`.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8777 — Improve GDExtension Tooling with Editor Debugger Tools
https://github.com/godotengine/godot-proposals/issues/8777 · 2024-01-02T19:38:18Z · current updated 2024-06-11T08:55:14Z

Need (excerpt): The Editor's debug tooling aspects are very restrictive and limited regarding GDExtension tooling.  In C++ modules, the tooling would have immediate access to things like ScriptDebugger, EditorDebuggerNode, and so on to interact with critical aspects of the debug subsystem, such as setting breakpoints, adding breakpoints to the Editor Debugger Panel, etc.

Requested operation (excerpt): This change provides several benefits:

**Setting breakpoints**
Plug-in and tool developers will be able to use `EditorDebuggerSession::set_breakpoint` as a way to access the same code path that the `CodeEdit` widget does by interacting with `EditorDebuggerNode` to toggle breakpoints. This allows tooling to set a breakpoint within the script debugger subsystem and register the UI entry in the breakpoints panel.

**Checking Breakpoints**
Adding the `ScriptDebugger` via the `EngineDebugger` single

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8778 — Update command palette when modifying shortcuts without having to restart the editor.
https://github.com/godotengine/godot-proposals/issues/8778 · 2024-01-02T20:40:34Z · current updated 2024-01-09T14:31:17Z

Need (excerpt): Currently for the command palette to have the shortcuts updated, the editor needs to be restarted.

Requested operation (excerpt): Have the command palette update similar to how to the editor drop-down menus do.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8779 — Replace ParallaxBackground and ParallaxLayer with different workflow
https://github.com/godotengine/godot-proposals/issues/8779 · 2024-01-03T01:13:01Z · current updated 2024-04-05T20:23:06Z

Need (excerpt): While I was making sure my lighting system supported camera rotation, I noticed the parallax nodes in Godot doesn't, which would prevent a lot of useful scenarios for my system. I noticed `ParallaxBackground` inherits from `CanvasLayer` but doesn't behave as a `CanvasLayer` is intended. It also has to jump through some hoops to adhere to the camera's transforms, but even then doesn't support rotation, and has tons various bugs and stale issues that date back to early 3.x. Even if these bugs were fixed, it inherently requires a strict hierarchy of `ParallaxBackground` -> `ParallaxLayer`, making it impossible to modify background layers with non-parallax backgrounds, or even by themselves as a group.

Requested operation (excerpt): Instead of inheriting from `CanvasLayer`, it should be either a `Node2D` or `Sprite2D`, and be a standalone node. This would allow for automatic transforms adhering to the current camera, and more flexibility (you can always just put it inside a `CanvasLayer` if you really want it to be). This also means faster and less confusing setup, the ability to group the layers (in a `CanvasGroup` or otherwise), and possibly better performance on mobile (someone in rendering, please correct me if I'm wron

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8780 — Add support for installing/managing addons via Git URL
https://github.com/godotengine/godot-proposals/issues/8780 · 2024-01-03T02:41:55Z · current updated 2025-01-23T17:20:55Z

Need (excerpt): Note: I used addons and plugins interchangeably here but what I mean is an extension or library that is meant to be self-contained and managed externally.

I'd like to create packages which aid in the development of Godot projects, but currently the process for importing addons isn't as clean as other engines/platforms due to the lack of dependencies and version management if you forgo the Asset Library. As I've been thinking about what it would take to actually implement https://github.com/godotengine/godot-proposals/issues/142 (dependency management for addons) I realized we would first need a mechanism to actually retrieve the addons that are listed as dependencies, which may come from Github/some other online source.

Additionally, the [official tutorial for installing a plugin](https://docs.godotengine.org/en/stable/tutorials/plugins

Requested operation (excerpt): Something that I really miss from Unity is the ability add a package via URL by inputting it into the engine itself:

![upm-ui-giturl](https://github.com/godotengine/godot-proposals/assets/11141862/d9123bd6-280c-4c6f-ad94-305fabe9a8d2)

Which then allows the engine to internally handle installation and updates for you. I think something like this would be a perfect addition to Godot as it would address 3 different concerns:

1. Improves user experience for adding Git-based plugins since you woul

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8781 — It's time to add an Export feature for the Android platform
https://github.com/godotengine/godot-proposals/issues/8781 · 2024-01-03T09:08:52Z · current updated 2024-01-03T15:07:39Z

Need (excerpt): on the android platform godot editor the export button is accidentally closed

Requested operation (excerpt): ![Screenshot_2024-01-03-15-54-43-783_com android chrome](https://github.com/godotengine/godot-proposals/assets/65835193/7c50a7f6-2a34-4f9d-a7bc-e65187b1aa3f)

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8783 — Add AUX mode to the `AnimationPlayer` to make the `AnimationPlaybackTrack` be blendable like the `AudioTrack`
https://github.com/godotengine/godot-proposals/issues/8783 · 2024-01-03T14:45:00Z · current updated 2026-07-25T07:52:09Z

Need (excerpt): AnimationPlaybackTrack cannot be blended.

Requested operation (excerpt): AnimationPlaybackTrack functions like a simple StateMachine, but it only calls the AnimationPlayer's `play()` and `seek()` methods and cannot blend. This causes a limitation as mentioned in https://github.com/godotengine/godot/issues/70338.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8784 — Add area intersection signals to PhysicsBody nodes
https://github.com/godotengine/godot-proposals/issues/8784 · 2024-01-03T16:41:42Z · current updated 2024-01-15T21:12:15Z

Need (excerpt): TL;DR: I'd like to add the likes of area_entered/exited (and their _shape_ variants) signals to all PhysicsBodies.

Basically it all started with me implementing character swimming. To my surprise I found out there's no way to tell if `CharacterBody3D` has entered `Area3D` (representing water) from the character itself. This seems like an omission, because it's a very common use case, but currently requires clunky workarounds. It also strays from the otherwise signals-oriented design.
(Also, on `RigidBody` type nodes we have signals for collisions but not `Area` intersections.)

Requested operation (excerpt): `PhysicsBody` classes get 4 new signals corresponding to those on `Areas`.
`entered_area(area)`
`entered_area_shape(area_rid, area, area_shape_id, body_shape_id)`
`exited_area(area)`
`exited_area_shape(area_rid, area, area_shape_id, body_shape_id)`

This allows bodies and scripts attached to them to be aware of which areas they enter and with which shapes of those areas they intersect with minimal extra code.

Workaround (excerpt): TL;DR: I'd like to add the likes of area_entered/exited (and their _shape_ variants) signals to all PhysicsBodies.

Basically it all started with me implementing character swimming. To my surprise I found out there's no way to tell if `CharacterBody3D` has entered `Area3D` (representing water) from the character itself. This seems like an omission, because it's a very common use case, but currently requires clunky workarounds. It also strays from the otherwise signals-oriented design.
(Also, on `RigidBody` type nodes we have signals for collisions but not `Area` intersections.)

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8785 — Optimizing 3D mesh into list of triangle strips/fans to save VRAM
https://github.com/godotengine/godot-proposals/issues/8785 · 2024-01-03T16:42:25Z · current updated 2024-01-04T15:12:58Z

Need (excerpt): The main limit to the game's performance is the triangle count of the map. If it's too large, the RAM/VRAM usage becomes way too high. I'm trying to avoid loading up parts when needed since the player will be able to teleport at times.

Requested operation (excerpt): Godot could automatically convert the list of triangles in a mesh to a list of triangle fans or strips, which would save a lot of memory. For example, a cube could go from storing 36 verticies (12 triangles), to 8 verticies (2 triangle strips). A small list of triangles would be stored alongside in case there's any gaps that couldn't be filled automatically.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8786 — Add left/right ctrl/alt/shift keycode
https://github.com/godotengine/godot-proposals/issues/8786 · 2024-01-03T19:29:56Z · current updated 2024-01-03T19:37:50Z

Need (excerpt): I can't separately check the status of the left ctrl/alt/shift and the right ctrl/alt/shift
我无法分别检测左ctrl/alt/shift与右ctrl/alt/shift按键的状态

Requested operation (excerpt): By adding the keycodes to allow me to check the status of the left and right ctrl/alt/shift separately
通过增加键码来允许我分别检查左右ctrl/alt/shift的状态

Example use "leftcctrl" keycode to only check the state of the left ctrl on keyboard

The original keycode does not need to be deleted, and can be used to check the left and right ctrl/alt/shift keys at the same time

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8787 — Automatically pick up `EXT_mesh_gpu_instancing` gltf extension
https://github.com/godotengine/godot-proposals/issues/8787 · 2024-01-03T20:02:19Z · current updated 2024-02-22T11:56:04Z

Need (excerpt): The `EXT_mesh_gpu_instancing` extension (https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Vendor/EXT_mesh_gpu_instancing/README.md) is currently not recognized. You need to set up mesh instancing manually using `MultiMeshInstance`. This is time consuming and way harder to do than for example in a 3d modeling software like blender (https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html#gpu-instances), that supports the `EXT_mesh_gpu_instancing` extension for exporting.

Requested operation (excerpt): Having support in godot for the `EXT_mesh_gpu_instancing` extension would simplify the 3d asset import workflow, especially for larger scenes with a lot of mesh instancing.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8788 — Notify users about window size changes
https://github.com/godotengine/godot-proposals/issues/8788 · 2024-01-03T20:34:47Z · current updated 2025-03-08T13:46:47Z

Need (excerpt): Accessing the notification, when the size of the root window changes is very unintuitive.
This problem has been discussed in the bug report https://github.com/godotengine/godot/issues/79336 which was solved by improving the documentation. However the unintuitive way could be improved.

Requested operation (excerpt): The problem itself can be solved by making `NOTIFICATION_WM_SIZE_CHANGED` available to child nodes of the window. That allows users to easily access when the root window is changed.
Since this change could have a negative performance impact, the performance impact needs to be evaluated beforehand.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8789 — Make Editor Viewport Message into a Label Node
https://github.com/godotengine/godot-proposals/issues/8789 · 2024-01-03T20:45:34Z · current updated 2024-01-04T00:35:44Z

Need (excerpt): ![image](https://github.com/godotengine/godot-proposals/assets/105675984/692cec28-4d0c-4b26-8822-7555a85198ec)

Currently this text is rendered directly into the viewport, and there is no way to access it inside the editor.

Requested operation (excerpt): I think this would align more with Godot's philosophy of "The Godot Editor is a Godot Game":

https://docs.godotengine.org/en/stable/getting_started/introduction/godot_design_philosophy.html#the-godot-editor-is-a-godot-game

I could see situations where the text in that field could be modified or exposed. I personally could use it as a stopgap for: #8445, by using the text that will be exposed to indirectly know that the gizmo is being manipulated. 

It would also allow users to easily move, del

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8790 — Add changed_text signal to Label and RichTextLabel
https://github.com/godotengine/godot-proposals/issues/8790 · 2024-01-03T23:07:48Z · current updated 2025-05-09T11:56:44Z

Need (excerpt): I want to add custom underlines to some of my labels, which get updated at runtime. 

To achieve this, I place a `NinePatchRectangle` under each line of the text, of which I want to update the position and scale accordingly to decorate the displayed text, as well as add or remove new ones if necessary.

Requested operation (excerpt): The `Label` and `RichTextLabel` classes receive a `text_changed` signal that passes over the new text value.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8791 — Allow setting `AnimationPlayer` interpolation modes per keyframe
https://github.com/godotengine/godot-proposals/issues/8791 · 2024-01-03T23:40:45Z · current updated 2024-08-31T14:09:05Z

Need (excerpt): AnimationPlayer easing and bezier curves are currently very restrictive and don't allow for much.
- A key frame can only ease in or ease out based on the easing setting set per-keyframe
- Cannot preview the easing curve
- Bezier Curves cannot be switched to or out of after creating a track, and the entire track is forced to use them.
- Editing Bezier curves can be difficult due to them always separating XYZ values, as well as difference in value ranges.

Requested operation (excerpt): The main idea behind this proposal is give the ability to set interpolation modes and use Bezier Curves per keyframe, rather than per track. As well as smaller ideas for some misc. improvements that are closely related.
A concern would be performance due to increased complexity, let me know if this would be an issue.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8792 — TileSet Editor should allow multi-selection and duplication of Alternative Tiles
https://github.com/godotengine/godot-proposals/issues/8792 · 2024-01-04T06:07:58Z · current updated 2024-01-04T10:00:16Z

Need (excerpt): It is tedious to manipulate many Alternative Tiles at a time.  If I want to make flipped and rotated versions of all my tiles, I must methodically set the "Flip H", "Flip V", and "Transpose" checkboxes for all 7 alternatives of each tile (I have over 20 base tiles just for some basic grass Terrain).  Furthermore, after completing this task once, Godot crashed, undoing the process for me.

Requested operation (excerpt): Assume all the Alternative Tiles have already been created.  7 Alternatives for each of my 20 Base Tiles.  Setting the flags for one row of my Alternatives currently takes 19 clicks: 1 to select each of the 7 Alternatives, and a total of 12 flags to be set per row.

19 clicks * 20 base tiles = **380 clicks**.

With multi-selection, this is reduced to **8 clicks**:
1. Select the 1st and 2nd columns of Alternative tiles
2. Select the 5th and 6th columns
3. Check "Flip H"
4. Select the 2nd and 3rd 

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8793 — Reimport buttons possibly confuse new and seasoned users of Godot
https://github.com/godotengine/godot-proposals/issues/8793 · 2024-01-04T12:05:25Z · current updated 2024-04-22T01:32:27Z

Need (excerpt): When a user makes changes to an imported 3D model or image, to save the changes the option available is 'Reimport'. This is confusing and counterintuitive to users as you would expect the button that saves changes would be titled 'Save'.

![Screenshot 2024-01-04 115831](https://github.com/godotengine/godot-proposals/assets/40317509/cf84cdf5-c188-4dd7-ba2b-262332639eed)

![Screenshot 2024-01-04 115934](https://github.com/godotengine/godot-proposals/assets/40317509/fd877ffb-e7dc-4a0b-ad15-21c1fc48427b)

Requested operation (excerpt): I haven't found information whether Godot works differently to other software with regards to making changes set and saved on files. In Uneal Engine if you make a change, you can Apply and save the changes, or you can click the item and select 'Save', it's much the same in Unity. If you save an alteration to an MS Word document, you would expect the file to be saved to the file, but not re-imported after the fact. 

Perhaps it's technically correct the way Godot does re-import/re-load a file aft

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8794 — Move 'Default Clear Color' setting to Editor Settings window instead of Project Settings
https://github.com/godotengine/godot-proposals/issues/8794 · 2024-01-04T12:30:31Z · current updated 2024-01-04T14:28:51Z

Need (excerpt): It isn't intuitive that to change the background colour of the 2D View and the '3D Advanced Import Settings' window that you have to go into **Project Settings>Rendering>Environment>Default Clear Color**.

It would seem more logical for it to be in Editor Settings window with the ability then to save the preference the next time you re-open Godot and start a new project.

Requested operation (excerpt): Personally I find the light grey colour #4d4d4d to be too bright for sprites and tilesets, and it is also too bright for for the '3D Advanced Import Settings' window. But as it is in Project settings it is not saved between different projects as other theme options are.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8795 — Ability to turn off the 2D Views Ruler guide permanently in Editor Settings
https://github.com/godotengine/godot-proposals/issues/8795 · 2024-01-04T12:43:49Z · current updated 2024-01-04T13:56:05Z

Need (excerpt): There is no way to permanently turn off the Ruller guide in the 2D view. In other software you can toggle it on or off permanently, for example Photoshop. 

I find it clutters the workspace and rarely have use for it.

Requested operation (excerpt): I find it clutters the workspace and rarely have use for it as I'm sure many other users would say.

It would still be nice to have the option within the 2D view to toggle it on and off where necassary, but also a permanent one too.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8796 — Add `Export selected resource (without dependencies)` filter for export preset.
https://github.com/godotengine/godot-proposals/issues/8796 · 2024-01-04T12:52:29Z · current updated 2025-09-19T07:53:41Z

Need (excerpt): But the presets about `export selected scene (include dependency)` and `export selected resources (include dependency)` in Godot will pack the complete dependencies of the scene or resource into the PCK. At this time, there will be redundancy like below.

There has A.tscn , B.tscn, C.tscn.
![image](https://github.com/godotengine/godot-proposals/assets/1620585/7a8dab6f-b453-42e6-9a23-a0f3dc4268ac)
![image](https://github.com/godotengine/godot-proposals/assets/1620585/29c8a0a4-c965-4ec8-be01-936703650cd5)
![image](https://github.com/godotengine/godot-proposals/assets/1620585/0b23575e-86f9-4f2d-b8bd-932cb62941b5)

A dependent C
B dependent C
C dependent nothing 

Create three export presets to :
Pack A.tscn into A.pck.
Pack B.tscn into C.pck.
Pack C.tscn into C.pck.

![image](https://github.com/godotengine/godot-proposals/assets/1620585/f999

Requested operation (excerpt): After all, I will load all the PCKs in the launcher anyway, and even if a single PCK has no dependencies, it does not affect its usage.

If PCKs can be exported without dependencies, I can even control which files are packed into the same PCK through a Python script. 
For example, I can pack all modified files into a patch.pck based on Git commit records. Or in a DLC branch, I can package all changes in the branch into a DLC.pck. Or I can scan the project and pack it into several PCKs with a chu

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8797 — Add support for more output types in AudioDriver
https://github.com/godotengine/godot-proposals/issues/8797 · 2024-01-04T14:08:23Z · current updated 2026-10-02T18:57:47Z

Need (excerpt): To get the data that needs to be outputted in any other format than int32_t, the buffer should be created. Which is memory allocation that can be easily prevented.

Requested operation (excerpt): Change `void AudioDriver::audio_server_process(int p_frames, int32_t *p_buffer, bool p_update_mix_time)` to the template function and create private functions that convert from int32_t to the needed type.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8799 — FatELF Support the export of x86_64 and arrm64 in one for Linux
https://github.com/godotengine/godot-proposals/issues/8799 · 2024-01-04T19:07:44Z · current updated 2024-01-04T22:19:21Z

Need (excerpt): The problem is that most Studios won't have enough resources to export all games in both architectures

Requested operation (excerpt): ARM64 is getting more and more in the mainstream with Powerful Devices. While macOS has wonderful App Support, Linux is sadly still a desert.
With this option is would be easier, straightforward and more main stream ready to just export every game in both architectures without the need of having to project files for Linux and export the project twice.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8800 — Add static method to PackedScene to return a new PackedScene from a Node
https://github.com/godotengine/godot-proposals/issues/8800 · 2024-01-04T19:11:29Z · current updated 2024-01-04T20:42:20Z

Need (excerpt): Take the following:

```GDScript
# Example made up on the spot:
var grabbed_enemy = get_node("Enemy")
var stored_scene = PackedScene.new()
stored_scene.pack(grabbed_enemy)
```

I have been thinking that having to create a completely empty **PackedScene** as a starting point is just... awkward.
That isn't to say `pack()` itself is bad. Sometimes you want to override an existing **PackedScene**, and that is completely fine.

This is not a big deal for most people, but it's fairly more noticeable in advanced use-cases. Say, saving many **PackedScene**s in separate parts of the codebase.

Requested operation (excerpt): Add a new static method to **PackedScene**. I'd call it `from()`.[^1]
Like `pack()`, it would require a single **Node** parameter, but it would return a new **PackedScene** with the node packed inside it, ready to go.

It's not a novel concept, now that static methods are supported (**FileAccess**, **DirAccess**, **Image**, some **Color**'s methods, etc.). Therefore, I also feel like the documentation should encourage using `from()`.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8801 — Make query_string_from_dict static in HTTPClient
https://github.com/godotengine/godot-proposals/issues/8801 · 2024-01-04T19:46:51Z · current updated 2024-07-05T07:53:03Z

Need (excerpt): Creating an `HTTPClient` object every time I need to use `query_string_from_dict` in `HTTPRequest`.

Requested operation (excerpt): The problem can be solved by making the `query_string_from_dict` method of `HTTPClient` static. I don't see any inconvenience in making this change.

In a single line, you can perform the conversion of a dictionary of parameters to a string.

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8803 — Ability to write godot console output to log file
https://github.com/godotengine/godot-proposals/issues/8803 · 2024-01-05T08:44:31Z · current updated 2024-01-22T19:52:42Z

Need (excerpt): Not getting any log output neither `syslog` nor `file` or `append` type

https://github.com/godotengine/godot/issues/86785

Requested operation (excerpt): Implementing --log /path/to/log.file in need of file logging states we working with file rather than redirect detection.
For logrotate important to handle SIGHUP to reopen log file.

I think as a future improvement same as predefined --headless parameter might be a good idea to have:

* --background (fork after start)
* --pid /path/to/pid.file (store process ID to be able to use `Type=forked` in systemd unit file it will help to restart process if it dies)

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8804 — TileMap Merging Improvements!
https://github.com/godotengine/godot-proposals/issues/8804 · 2024-01-05T11:55:54Z · current updated 2024-01-06T12:11:37Z

Need (excerpt): I want to propose better tileset merging options. If you want to add something or a new tile to your already existing tilemap it creates or saves it as a new tileset and than if we delete the previous tileset the progress and all its tiles is gone. In short their should be a option to simply add the new tile to the exisiting tileset without creting a new tileset, and this will ensure that the progress is not resetted cause if you merge the tilesets now they save it as a new tileset and the progress(already exisitng tiles in levels are all cleared)

https://github.com/godotengine/godot-proposals/assets/109503120/2b51889f-f3fe-4a58-bd67-35ff3f14950e

Summary:
A feature to merge the new tile in the existing tileset without creating a new tileset

Requested operation (excerpt): This can help alot if a new tile is needed to be added in the current tileset, Also fixes the previous bug/problem of tilemap clearing all the tiles after merging. Can help if the tileset is not finalized and needs to add/remove tiles from it for experimentation.
Basically it allows users to edit the tilesets more easily

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8805 — Show error when attempting to compare the type of statically typed variable
https://github.com/godotengine/godot-proposals/issues/8805 · 2024-01-05T12:56:50Z · current updated 2024-07-12T04:56:40Z

Need (excerpt): There is no small feature for typification

Requested operation (excerpt): Show a warning / error when checking the type of a variable whose type is already defined via typeof()
(In any case, it can be changed in the settings)

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8806 — open_scene_from_path but no close_scene or close_scene_from_path 
https://github.com/godotengine/godot-proposals/issues/8806 · 2024-01-05T13:54:51Z · current updated 2025-06-03T00:05:28Z

Need (excerpt): When a scene is open in the editor, changes I make via tool script are not saved into the scene file.

Requested operation (excerpt): With a close_scene method I could close the scene tab make the changes via my tool script and then reopen the scene again with open_scene_from_path

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8807 — Exporting Plugin/AssetLib workflow implementation
https://github.com/godotengine/godot-proposals/issues/8807 · 2024-01-05T21:08:19Z · current updated 2024-01-09T00:06:06Z

Need (excerpt): When creating a custom add-on, the official method mentioned in godot docs in [making_plugins](https://docs.godotengine.org/es/3.5/tutorials/plugins/editor/making_plugins.html#) there's no info on how to exactly export a plugin when its completed. there's a section in [Generating PCK files](https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html) that explain how to export a project as non run-able and select specific folders to be exported, this approach works sometimes but it doesn't feel like a proper way and also it requires some workarounds and dealing with export configuration. The general UX feeling to this issue is that add-ons and packages creation in this scenario get combined in the same category as exporting the game, sharing the same windows, causing that everyone who is making an add-on also has to create

Requested operation (excerpt): So first, there is already an implementation to allow export .pck or .zip as mentioned in the [docs - Generating PCK files](https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html), doing this we can also select a specific folder and their dependencies to be exported if we go to the `Resources` section > Then select `Export selected resource (and dependencies)` > select the checkbox of the resources and assets to be exported.

![export example](https://github.com/godotengine/

Workaround (excerpt): When creating a custom add-on, the official method mentioned in godot docs in [making_plugins](https://docs.godotengine.org/es/3.5/tutorials/plugins/editor/making_plugins.html#) there's no info on how to exactly export a plugin when its completed. there's a section in [Generating PCK files](https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html) that explain how to export a project as non run-able and select specific folders to be exported, this approach works sometimes but it doesn't feel like a proper way and also it requires some workarounds and dealing with export configuration. The general UX feeling to this issue is that add-ons and packages creation in this scenario get combined in the same category as exporting the game, sharing the same windows, causing that everyone who is making an add-on also has to create

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8809 — Add a session number command line argument to distinguish multiple instances of Godot
https://github.com/godotengine/godot-proposals/issues/8809 · 2024-01-06T00:34:08Z · current updated 2025-03-29T12:30:18Z

Need (excerpt): When you select multiple instances from the Debug -> Run Multiple Instances menu, each of the sessions shows up in the debugger separately with a number:

<img width="528" alt="Screenshot 2024-01-05 at 6 06 38 PM" src="https://github.com/godotengine/godot-proposals/assets/1646875/34c13ae5-4906-426b-937c-9625d6895ce5">

However, there is no way to detect which is which in GDScript. I would like to be able to detect this number from GDScript so that I can check for session ID 2 and have it be the server (launch 1 -> only client, launch 2 -> client and server, launch 3 or 4 -> one server and the rest are clients).

Aside from solving the problem of fighting over the server, I would like to manually implement a system to use subfolders for config files, where session 1 stores in `user://1/`, session 2 stores in `user://2/`, etc. Currently all

Requested operation (excerpt): I propose passing the session number to each session, so that we can identify the session number from GDScript by reading the OS command line arguments:

```gdscript
func _ready():
	print(OS.get_cmdline_args())
```

<img width="426" alt="Screenshot 2024-01-05 at 6 13 33 PM" src="https://github.com/godotengine/godot-proposals/assets/1646875/0e47af33-6f7e-4925-bf6f-2d4dd90598ec">

Why start from 1? This matches what shows up in the Godot editor. The number 0 is probably better suited towards speci

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

## #8810 — Reveal scene/resource in FileSystem dock when middle-clicking it in the inspector or Scene tree dock
https://github.com/godotengine/godot-proposals/issues/8810 · 2024-01-06T01:20:50Z · current updated 2024-01-10T00:50:56Z

Need (excerpt): CURRENT
Now, to determine the location of the resource in the project folder, you need to perform the following actions:

1. For resources :
1.1. Find resource in Inspector window
1.2 Select from context menu "Show In FileSystem"

![select_resource_old](https://github.com/godotengine/godot-proposals/assets/7798042/a2a25fb1-fbe3-4c24-bbd5-c5e9d243ee50)

2. For scenes:
2.1 Point at scene tab
2.2 Select from context menu "Show In FileSystem"

![select_scene_old](https://github.com/godotengine/godot-proposals/assets/7798042/44bb52cb-6a26-4dbb-b56e-8e06c5b3834f)

3. For subscenes:
3.1 Open subscene in new tab
3.2 Point at subscene tab
3.3 Select from context menu "Show in FileSystem"

![select_nested_scene_old](https://github.com/godotengine/godot-proposals/assets/7798042/e8cf1adf-8e8f-4aab-a4e7-dfd0454c8d09)

This action needs to be performed

Requested operation (excerpt): NEW
This action needs to be performed quite often, so I suggest adding a hotkey for it. - Middle Mouse Button  or Left Mose Button 

1. For resources:
1.1 Find resource in Inspector window
1.2 Press Middle Mouse Button (MMB) to  to determine the location of the resource in the project folder

![select_resource_new](https://github.com/godotengine/godot-proposals/assets/7798042/2effc5c9-2023-4965-a25a-2eacd3eb7934)

2. For scenes:
2.1 Point current scene root node at scene tree
2.2  Press Middle M

Workaround (excerpt): section not found

Prior awareness: only named alternatives in these excerpts; actual creation-time body, prior use and knowledge unknown unless independently confirmed.

