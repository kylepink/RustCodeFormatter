# RustCodeFormatter
RustCodeFromatter is a plugin for Sublime Text 3 (may also work for ST2) which allows the formatting of rust code. This plugin is a binding for [rust-style][1]. The default key to format selected lines is ```ctrl+\```. See issues section below for limitations.

## Requirements
1. The project [rust-style][1] must be compiled.
2. Compiled [rust-style][1] executable should be located in your search path - or the plugin can be directed to use the absolute path to the command (see below Setup -> 2).

## Setup
1. Clone this project to {sublime data}/Data/Packages/RustCodeFormatter. Can be found quickly by opening menu ```Preferences -> Browse Packages...```.
2. (Optional) To set the absolute path to your rust-style installation:
    1. Open the command pallete by pressing ```Ctrl+Shift+P``` or through the menu ```Tools -> Command Pallete```.
    2. Enter/select ```Rust Code Formatter: Set Path```.
    3. An input field will appear with the default content ```rust-style```. Replace with an absolute path, ie ```C:\directory\rust-style.exe``` and press enter.
3. (Optional) To setup custom style preferences place a customised ```.rust-style.toml``` style file within the root directory of your project. See [rust-style][1] for the details.
4. (Optional) To change the key binding, open menu ```Preferences -> Key Bindings - User``` and add the following, substituting with your own key preference:
````
[
    {
        "keys": ["ctrl+\\"], "command": "rust_code_formatter",
        "context":
        [
            {"key": "selector", "operator": "equal", "operand": "source.rust"}
        ]
    }
]
```
Note: If there already exists other user key bindings, insert the key binding without replacing everything.

## Issues
* [rust-style][1] is a work in progress and still has some formatting issues and a few bugs.

[1]: https://github.com/sp0/rust-style
