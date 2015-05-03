import sublime, sublime_plugin, json, os, subprocess
from subprocess import PIPE, Popen

settings = None
rust_style_bin = None

def plugin_loaded():
    load_settings()

def plugin_unloaded():
    unload_settings()

def load_settings():
    global settings
    global rust_style_bin

    settings = sublime.load_settings("RustCodeFormatter.sublime-settings")
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

class RustCodeFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if settings == None:
            load_settings()

        # constructs command
        cmd = list()
        cmd.append(rust_style_bin)
        cmd.append("--output-replacements-json")

        # cmd display fix for windows
        start_info = None
        if os.name == 'nt':
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
            sublime.status_message("Rust formatter: rust-style process call failed. See log for details.")
            return

        json_data = json.loads(data.decode("utf-8"))

        for replacement in reversed(json_data):
            region = sublime.Region(replacement["start_character"], replacement["end_character"])
            text = replacement["text"]
            self.view.replace(edit, region, text)

        sublime.status_message("Rust formatter has performed " + str(len(json_data)) + " replacements.")
