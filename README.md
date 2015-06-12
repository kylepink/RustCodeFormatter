# RustCodeFormatter
RustCodeFromatter is a plugin for Sublime Text 3 which allows the formatting of rust code. This plugin is a binding for [rust-style][1]. The default key to format selected lines is ```ctrl+k, ctrl+f```. See issues section below for limitations.

## Requirements
1. Install the [Rust syntax highlighting][2] sublime package.
2. Clone and compile [rust-style][1]. Place the executable in your search path; or direct the plugin to use the absolute path of the executable (see below Setup -> 2).

## Setup
1. Install the [RustCodeFormatter package][3] through package control or clone this project to ```{sublime data}/Data/Packages/RustCodeFormatter```.
2. (Optional) To set the absolute path to your rust-style installation:
    1. Open the command pallete by pressing ```Ctrl+Shift+P``` or through the menu ```Tools -> Command Pallete```.
    2. Enter/select ```Rust Code Formatter: Set Path```.
    3. An input field will appear with the default content ```rust-style```. Replace with an absolute path, ie ```C:\directory\rust-style.exe``` and press enter.
3. (Optional) To setup custom style preferences:
    1. Open the command pallete by pressing ```Ctrl+Shift+P``` or through the menu ```Tools -> Command Pallete```.
    2. Enter/select ```Rust Code Formatter: Add New Style```.
    3. Select one of the opened directories listed or select ```Other...``` and insert custom directory.
4. (Optional) To change the key binding, open menu ```Preferences -> Key Bindings - User``` and add the following, substituting with your own key preference:
```
[
    {
        "keys": ["ctrl+k", "ctrl+f"], "command": "rust_code_formatter_format",
        "context":
        [
            {"key": "selector", "operator": "equal", "operand": "source.rust"}
        ]
    }
]
```
Note: If there already exists other user key bindings, insert the key binding without replacing everything.

## Issues
* [rust-style][1] is a work in progress and still has formatting issues and bugs.

[1]: https://github.com/sp0/rust-style
[2]: https://sublime.wbond.net/packages/Rust
[3]: https://packagecontrol.io/packages/RustCodeFormatter
