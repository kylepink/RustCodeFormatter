import sublime, sublime_plugin, json, os, subprocess
from subprocess import PIPE, Popen

settings = None
rustfmt_bin = None

# note: plugin_loaded/plugin_unloaded only called automatically in ST3
def plugin_loaded():
    load_settings()

def plugin_unloaded():
    unload_settings()

def load_settings():
    global settings
    global rustfmt_bin

    settings = sublime.load_settings("RustFormatter.sublime-settings")
    rustfmt_bin = settings.get("rustfmt_bin", "rustfmt")
    settings.add_on_change("rustfmt_bin", settings_changed)

def unload_settings():
    global settings
    global rustfmt_bin
    
    if settings != None:
        settings.clear_on_change("rustfmt_bin")
        settings = None
        rustfmt_bin = None

def settings_changed():
    unload_settings()
    load_settings()

class RustCodeFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if settings == None:
            load_settings()
        # TODO: SHOULD BE IMPLEMENTED THROUGH SUBLIME?
        # only allows formatting if .rs extension
        file_name = self.view.file_name()
        if file_name == None or file_name[-3:] != ".rs":
            sublime.status_message("Cannot rust format non .rs files.")
            return

        # constructs command
        cmd = list()
        cmd.append(rustfmt_bin)
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
        proc.stdin.close()

        (data, errdata) = proc.communicate()
        return_code = proc.wait()

        if return_code != 0:
            print("Rust Formatter error data:\n")
            print(errdata)
            sublime.status_message("Rust formatter: rustfmt process call failed. See log for details.")
            return

        json_data = json.loads(data)

        for replacement in reversed(json_data):
            region = sublime.Region(replacement["start_character"], replacement["end_character"])
            text = replacement["text"]
            self.view.replace(edit, region, text)

        sublime.status_message("Rust formatter has performed " + str(len(json_data)) + " replacements.")
