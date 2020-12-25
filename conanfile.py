from conans import ConanFile, MSBuild, tools
from shutil import copyfile
import os

class TracyProfilerConan(ConanFile):
    name = "tracy"
    version = "0.7.4"
    license = "https://github.com/wolfpld/tracy/blob/master/LICENSE"
    description = "A real time, nanosecond resolution, remote telemetry, hybrid frame and sampling profiler for games and other applications."
    url = "https://github.com/wolfpld/tracy"

    settings = "os", "compiler", "arch"
    exports_sources = ["premake5.lua"]

    build_requires = "premake_installer/5.0.0-alpha14@bincrafters/stable"

    folder_name = "tracy-{}".format(version)

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    # The the source from github
    def source(self):
        zip_name = "v{}.zip".format(self.version)
        tools.download("https://github.com/wolfpld/tracy/archive/{}".format(zip_name), zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    # Build both the debug and release builds
    def build(self):
        _premake_action = "gmake"

        if self.settings.compiler == "Visual Studio":
            _visuals = {
                "11": "vs2012",
                "12": "vs2013",
                "14": "vs2015",
                "15": "vs2017",
                "16": "vs2019",
            }
            _premake_action = "{}".format(_visuals.get(str(self.settings.compiler.version), "vs2019"))

        with tools.chdir(os.path.join(self.source_folder, self.folder_name)):

            copyfile("../premake5.lua", "premake5.lua")

            self.run("premake5 {} --arch={}".format(_premake_action, self.settings.arch))

            if self.settings.compiler == "Visual Studio":
                msbuild = MSBuild(self)
                msbuild.build("tracy.sln", build_type="Debug")
                msbuild.build("tracy.sln", build_type="Release")

            if self.settings.compiler == "clang":
                self.run("make config=debug")
                self.run("make config=release")

    def package(self):
        # Copy the license file
        self.copy("LICENSE", src=self.folder_name, dst="LICENSE")

        _headerexts = [
            "*.hpp",
            "*.h"
        ]

        _subdirs = [
            "common",
            "client"
        ]

        for subdir in _subdirs:
            for ext in _headerexts:
                self.copy(ext, "include/%s" % subdir, "%s/%s" % (self.folder_name, subdir), keep_path=True)

        self.copy("Tracy.hpp", "include", self.folder_name)
        self.copy("TracyOpenGL.hpp", "include", self.folder_name)

        build_dir = os.path.join(self.folder_name, "bin")

        if self.settings.os == "Windows":
            self.copy("*.pdb", "lib", build_dir, keep_path=True)
            self.copy("*.lib", "lib", build_dir, keep_path=True)

        if self.settings.os == "Linux":
            self.copy("*.a", "lib", build_dir, keep_path=True)

    def package_info(self):
        self.cpp_info.debug.libdirs = [ "lib/Debug" ]
        self.cpp_info.release.libdirs = [ "lib/Release" ]
        self.cpp_info.libdirs = []
        self.cpp_info.libs = ["tracy"]

