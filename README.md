# RustCodeFormatter
RustCodeFromatter is a plugin for Sublime Text 3 (will not work for ST2) which allows the formatting of rust code. This plugin is a binding for [sp0/rust-style][1]. Functionality is currently in limited, see issues section below for more details.

## Requirements
1. The project [sp0/rust-style][1] must be compiled.
2. Compiled [sp0/rust-style][1] executable should be located in your search path. Or the plugin can be directed to use the absolute path to the command (see below Setup -> 3).

## Setup
1. Clone this project to {sublime data}/Data/Packages/RustCodeFormatter. Can be found quickly by opening menu ```Preferences -> Browse Packages...```.
2. (Optional, default key binding is "ctrl + \") To change the key binding, open menu ```Preferences -> Key Bindings - User``` and add the following and substitute your own key preference. (Note: if there already exists other user key bindings, insert they key binding without replacing everything):
````
[
    { "keys": ["ctrl+\\"], "command": "rust_code_formatter" }
]
```
3. (Optional) To set the absolute path to your rust-style installation, open menu ```Preferences -> Package Settings -> Rust Code Formatter -> Settings – User``` and add the following (substituting rust-style with your absolute path to rust-style):
```
{
    "rust_style_bin": "rust-style"
}
```
Note: Windows users should remember to escape your \ characters. (ie "C:\\\\directory\\\\rust-style.exe").

## Issues
* Custom preferences/styles are not currently implemented.
* Currently only allows the formating of the whole file.
* [sp0/rust-style][1] is a work in progress and still has issues which limits the usefulness of this plugin.

[1]: https://github.com/sp0/rust-style