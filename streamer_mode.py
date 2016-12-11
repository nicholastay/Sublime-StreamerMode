import sublime, sublime_plugin, re, fnmatch, os

class StreamerModeEvents(sublime_plugin.EventListener):
    def on_load(self, view):
        s = sublime.load_settings("StreamerMode.sublime-settings")
        if s.get("streamer_mode_enabled", False) != True:
            return
        global_s = sublime.load_settings("Preferences.sublime-settings")
        self.hide_files = [re.compile(p) for p in [fnmatch.translate(q) for q in global_s.get("streamer_mode_hide_files", [])]] # thanks for inspiration! https://github.com/jonathandelgado/SublimeTodoReview/blob/master/TodoReview.py
        if not any(p.search(view.file_name()) for p in self.hide_files):
            return
        if view.settings().get("streamer_mode_override", False) == False:
            window = view.window()
            window.run_command("close_file")
            newView = window.new_file()
            newView.settings().set("streamer_mode_blocked_file", view.file_name())
            newView.set_scratch(True)
            window.focus_view(newView)
            filename = os.path.basename(view.file_name())
            newView.set_name("Streamer Mode: {}".format(filename))
            newView.run_command("streamer_mode_output_warn", {"fname": filename})
            newView.set_read_only(True)


class StreamerModeOutputWarnCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        self.view.insert(edit, 0, """Streamer Mode Active: {}
======================
This file is currently BLOCKED from view because Streamer Mode is active.

To force-view this file, use the Command Palette on this screen to override and allow the file to open again.
Otherwise, it is SAFE to close this view.""".format(args["fname"]))


class StreamerModeOverride(sublime_plugin.TextCommand):
    def run(self, edit):
        s = sublime.load_settings("StreamerMode.sublime-settings")
        if s.get("streamer_mode_enabled", False) != True:
            return
        s2 = self.view.settings().get("streamer_mode_blocked_file", None)
        if s2 == None:
            return
        window = self.view.window()
        window.run_command("close_file")
        newView = window.open_file(s2)
        newView.settings().set("streamer_mode_override", True)


class StreamerModeToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = sublime.load_settings("StreamerMode.sublime-settings")
        global_s = sublime.load_settings("Preferences.sublime-settings")
        enabled = s.get("streamer_mode_enabled", False)
        if enabled != True:
            s.set("streamer_mode_enabled", True)
            if global_s.get("streamer_mode_hide_files", None) == None: 
                global_s.set("streamer_mode_hide_files", []) # init
            # store old bin stores -- hide the files from the goto anything menu
            binpatterns = global_s.get("binary_file_patterns", [])
            s.set("streamer_mode_binary_backup", binpatterns)
            global_s.set("binary_file_patterns", binpatterns + global_s.get("streamer_mode_hide_files", [])) # concat old ones and our ones
            self.view.window().status_message("Streamer Mode: Enabled")
        else:
            s.set("streamer_mode_enabled", False)
            # restore bin stores
            binpatterns = s.get("streamer_mode_binary_backup", None)
            if binpatterns != None:
                global_s.set("binary_file_patterns", binpatterns)
            self.view.window().status_message("Streamer Mode: Disabled")
        sublime.save_settings("StreamerMode.sublime-settings")
        sublime.save_settings("Preferences.sublime-settings")