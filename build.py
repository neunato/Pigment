import sublime
from sublime_plugin import WindowCommand
# import os
import pathlib

class PigmentScreenshots(WindowCommand):
   """
   ASSUMPTIONS
   - 1920 x 1080 screen resolution of first monitor
   - mss python package installed
   - autopy python package installed
   - generally my settings... for now
   - project files exist... (do a git clone!)
   """

   def set_view_settings(self, settings):
      window = sublime.active_window()
      view = window.active_view()
      for k, v in settings.items():
         view.settings().set(k, v)

   def set_settings(self, settings):
      sets = sublime.load_settings("Preferences.sublime-settings")
      # window = sublime.active_window()
      for k, v in settings.items():
         sets.set(k, v)

   def set_layout(self, layout):
      window = sublime.active_window()
      window.run_command("set_layout", layout)

   def exec(self, command):
      window = sublime.active_window()
      window.run_command(command)

   def wait(self, ms):
      self.delay += ms

   def then(self, f):
      sublime.set_timeout(f, self.delay)

   def execute(self, setups):
      if not setups:
         return

      setup = setups.pop(0)
      project = setup["project"]
      files = setup["files"]
      settings = setup["settings"]
      layout = setup["layout"]
      schemes = setup["schemes"]

      # self.set_settings({"show_panel_on_build": False})

      self.new_window(project=project, files=files, settings=settings)
      self.wait(50)
      self.then(lambda: self.set_layout(layout))
      self.then(lambda: self.set_view_settings(settings))
      for i, (name, scheme) in enumerate(schemes.items()):
         self.then(lambda scheme=scheme: self.set_settings({"color_scheme": scheme}))
         self.then(lambda name=name: self.take_screenshot("screenshot-" + name + ".png"))
         self.wait(200)
      self.then(lambda: self.close_window())

      # window.run_command("toggle_minimap")
      # window.run_command("exec", {"cmd": ["python", "move_to.py"]})    # expand sidebar folder

      self.then(lambda: self.execute(setups))


   def run(self):
      self.delay = 0

      window = self.window

      schemes = {
         "mariana": "Mariana.sublime-color-scheme",
         "sixteen": "Sixteen.sublime-color-scheme",
         "monokai": "Monokai.sublime-color-scheme",
      }

      project_path = "D:/Dev/siteswap.js"
      files_path = [
         project_path + "/src/Siteswap.js",
         project_path + "/src/Siteswap.prototype.equals.js",
         project_path + "/src/misc.js",
      ]

      setups = []

      # SCREENSHOT 1 (sidebar + one column)
      setups.append({
         "project": project_path,
         "files": files_path,
         "layout": {
            "cols": [0.0, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1]],
         },
         "settings": {
            "mini_diff": False,
            "line_numbers": False,
            "font_face": "Fira Code"
         },
         "schemes": schemes
      })

      self.execute(setups)


   def new_window(self, project, files, settings):
      window = sublime.active_window()
      window.run_command("exec", {"cmd": ["subl", "-n", "-a", project, "--command", "toggle_full_screen", *files]})


   def close_window(self):
      window = sublime.active_window()
      window.run_command("close_window")

   def take_screenshot(self, name):
      path = pathlib.Path(__file__).parent.absolute()
      path = str(path) + "/screenshots"

      window = sublime.active_window()
      window.run_command("exec", {"cmd": ["python", "screenshot.py", name], "working_dir": path})
