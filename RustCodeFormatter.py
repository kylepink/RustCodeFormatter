import sublime, sublime_plugin, json, os, subprocess
from subprocess import PIPE, Popen

settings_file = "RustCodeFormatter.sublime-settings"
settings = None
rust_style_bin = None

def plugin_loaded():
    load_settings()

def plugin_unloaded():
    unload_settings()

def load_settings():
    global settings
    global rust_style_bin

    settings = sublime.load_settings(settings_file)
    rust_style_bin = settings.get("rust_style_bin", "rust-style")
    settings.add_on_change("rust_style_bin", settings_changed)

def unload_settings():
    global settings
    global rust_style_bin

    if settings != None:
        settings.clear_on_change("rust_style_bin")
        settings = None
        rust_style_bin = None

def settings_changed():
    unload_settings()
    load_settings()

class RustCodeFormatterSetPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        if settings == None:
            load_settings()
        window = sublime.active_window()
        window.show_input_panel(
            "Path to rust-style: ",
            rust_style_bin,
            set_binary_path,
            None,
            None
        )

def set_binary_path(path):
    global rust_style_bin

    if settings == None:
        load_settings()

    rust_style_bin = path
    settings.set("rust_style_bin", path)
    sublime.save_settings(settings_file)

class RustCodeFormatterAddNewStyleCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = sublime.active_window()
        folders = window.folders()
        if len(folders) > 0:
            pick_directory()
        else:
            get_custom_directory()
        
def pick_directory():
    window = sublime.active_window()
    folders = window.folders()
    folders.append("Other...")

    window.show_quick_panel(
        folders,
        process_pick,
        0,
        0,
        None
    )

def process_pick(index):
    if index == -1:
        return

    window = sublime.active_window()
    folders = window.folders()
    if index >= len(folders):
        get_custom_directory()
    else:
        add_new_style_file(folders[index])

def get_custom_directory():
    window = sublime.active_window()
    default_text = ""
    folders = window.folders()
    if len(folders) > 0:
        default_text = folders[0]

    window.show_input_panel(
        "Directory for new style file: ",
        default_text,
        add_new_style_file,
        None,
        None
    )

def add_new_style_file(directory):
    file_name = directory
    if file_name[-1] != "/" and file_name[-1] != "\\":
        file_name += os.sep
    file_name += ".rust-style.toml"

    # constructs command
    cmd = list()
    cmd.append(rust_style_bin)
    cmd.append("--dump-style")

    # cmd display fix for windows
    start_info = None
    if os.name == "nt":
        start_info = subprocess.STARTUPINFO()
        start_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # starts process
    proc = Popen(cmd, stdout=PIPE, stdin=None, stderr=PIPE, startupinfo=start_info)
    (data, errdata) = proc.communicate()
    return_code = proc.wait()

    if return_code != 0:
        print("Error occurred while obtaining default style:")
        print(errdata)
        sublime.error_message("Rust formatter: rust-style process call failed. See log for details.")
        return

    # writes style file
    try:
        file = open(file_name, "w")
    except FileNotFoundError:
        sublime.error_message("Rust formatter: directory specified does not exist.")
    except PermissionError:
        sublime.error_message("Rust formatter: dnsufficient permissions to write style file.")
    except:
        sublime.error_message("Rust formatter: the new style file could not be created.")
    else:
        try:
            file.write(data.decode("utf-8"))
            file.flush()
        except:
            sublime.error_message("Rust formatter: an error was encountered while writing the style file.")
        finally:
            file.close()

class RustCodeFormatterFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if settings == None:
            load_settings()

        # constructs command
        cmd = list()
        cmd.append(rust_style_bin)
        cmd.append("--output-replacements-json")

        # adds line ranges to command
        for selection in self.view.sel():
            (line_start, _) = self.view.rowcol(selection.begin())
            (line_end, _) = self.view.rowcol(selection.end())
            # adds lines ranges to command as 1-based ranges
            cmd.append("--lines={0}:{1}".format(line_start + 1, line_end + 1))

        # appends file location to command, this is where it will start style search
        file_location = self.view.file_name()
        if file_location != None:
            cmd.append("--file-location")
            cmd.append(file_location)

        # cmd display fix for windows
        start_info = None
        if os.name == "nt":
            start_info = subprocess.STARTUPINFO()
            start_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # starts process
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, startupinfo=start_info)

        # sends all view lines to process stdin
        cursor = 0
        while cursor < self.view.size():
            region = self.view.full_line(cursor)
            line = self.view.substr(region)
            cursor += len(line)
            proc.stdin.write(line.encode("utf8"))

        (data, errdata) = proc.communicate()
        return_code = proc.wait()

        if return_code != 0:
            print("Rust Formatter error data:\n")
            print(errdata)
            sublime.error_message("Rust formatter: rust-style process call failed. See log (ctrl + `) for details.")
            return

        json_data = json.loads(data.decode("utf-8"))

        for replacement in reversed(json_data):
            region = sublime.Region(replacement["start_character"], replacement["end_character"])
            text = replacement["text"]
            self.view.replace(edit, region, text)

        sublime.status_message("Rust formatter has performed " + str(len(json_data)) + " replacements.")
