#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class PDCursesConan(ConanFile):
    name = "pdcurses"
    version = "3.6"
    description = "Public Domain Curses - a curses library for environments that don't fit the termcap/terminfo model. "
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/wmcbrine/PDCurses"
    author = "Bincrafters <someone@gmail.com>"
    # Indicates License type of the packaged library
    license = "Public Domain"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    # Update 2/9/18 - Per conan team, ranges are slow to resolve.
    # So, with libs like zlib, updates are very rare, so we now use static version

    requires = (

    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/wmcbrine/PDCurses"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build_nmake(self):

        with tools.chdir(os.path.join(self.source_subfolder, 'wincon')):
            command = 'nmake -f Makefile.vc'
            with tools.vcvars(self.settings,
                              filter_known_paths=False, force=True):
                self.run(command)

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.build_nmake()

    def package(self):

        self.copy(pattern="*.h", dst="include", src=self.source_subfolder)

        with tools.chdir(os.path.join(self.source_subfolder, 'wincon')):
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
