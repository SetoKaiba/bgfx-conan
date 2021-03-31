import os
import glob
from conans import ConanFile, tools, MSBuild


class BgfxConan(ConanFile):
    name = "bgfx"
    license = "BSD-2-Clause"
    description = "bgfx"
    topics = ("conan", "bgfx")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False],
               "vs_version": ["2019", "2017"], "with_windows": ["10.0", "8.1"],
               "with_tools": [True, False], "with_combined_examples": [True, False],
               "with_shared_lib": [True, False]}
    default_options = {"shared": False, "fPIC": True,
                       "vs_version": "2019", "with_windows": "10.0",
                       "with_tools": True, "with_combined_examples": True,
                       "with_shared_lib": True}
    generators = "cmake"

    @property
    def _bgfx_subfolder(self):
        return "bgfx"

    @property
    def _bx_subfolder(self):
        return "bx"

    @property
    def _bimg_subfolder(self):
        return "bimg"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["bgfx"][self.version])
        tools.get(**self.conan_data["bx"][self.version])
        tools.get(**self.conan_data["bimg"][self.version])
        os.rename(glob.glob("bgfx-*")[0], self._bgfx_subfolder)
        os.rename(glob.glob("bx-*")[0], self._bx_subfolder)
        os.rename(glob.glob("bimg-*")[0], self._bimg_subfolder)

    def build(self):
        cmd = "cd bgfx && "
        if self.settings.os == "Windows":
            genie_path = os.path.join(
                "..", "bx", "tools", "bin", "windows", "genie")
        if self.settings.os == "Macos":
            genie_path = os.path.join(
                "..", "bx", "tools", "bin", "darwin", "genie")
        cmd += genie_path
        if self.options.with_tools:
            cmd += " --with-tools"
        if self.options.with_combined_examples:
            cmd += " --with-combined-examples"
        if self.options.with_shared_lib:
            cmd += " --with-shared-lib"
        if self.settings.os == "Windows":
            cmd += " --with-windows=" + str(self.options.with_windows)
            cmd += " vs" + str(self.options.vs_version)
        if self.settings.os == "Macos":
            cmd += " --gcc=osx-x64"
            cmd += " gmake"
        self.run(cmd)
        if self.settings.os == "Windows":
            msbuild = MSBuild(self)
            sln_path = os.path.join(
                "bgfx", ".build", "projects", "vs" + str(self.options.vs_version), "bgfx.sln")
            msbuild.build(sln_path, build_type=self.settings.build_type)
        if self.settings.os == "Macos":
            project_path = os.path.join(
                "bgfx", ".build", "projects", "gmake-osx-x64")
            build_cmd = "make -C "
            build_cmd += project_path
            build_cmd += " config=" + str(self.settings.build_type).lower()
            self.run(build_cmd)
            

    def package(self):
        self.copy("*", dst="include",
                  src=os.path.join(self.build_folder, self._bgfx_subfolder, "include"))
        self.copy("*", dst="include",
                  src=os.path.join(self.build_folder, self._bx_subfolder, "include"))
        self.copy("*", dst="include",
                  src=os.path.join(self.build_folder, self._bimg_subfolder, "include"))
        if self.settings.os == "Windows":
            if self.settings.arch == "x86":
                platform = "win32_vs" + str(self.options.vs_version)
            if self.settings.arch == "x86_64":
                platform = "win64_vs" + str(self.options.vs_version)
            self.copy("*.lib", dst="lib",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
            self.copy("*.exe", dst="bin",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
            self.copy("*.dll", dst="bin",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
        if self.settings.os == "Macos":
            platform = "osx-x64"
            self.copy("*.a", dst="lib",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
            self.copy("*" + str(self.settings.build_type), dst="bin",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
            self.copy("example*" + str(self.settings.build_type), dst="bin",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))
            self.copy("*.dylib", dst="bin",
                      src=os.path.join(self.build_folder, self._bgfx_subfolder, ".build", platform, "bin"))

    def package_info(self):
        self.cpp_info.libs = ["bgfx" + str(self.settings.build_type),
                              "bimg" + str(self.settings.build_type),
                              "bx" + str(self.settings.build_type)]
