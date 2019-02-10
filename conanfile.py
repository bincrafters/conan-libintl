#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, Meson
import os


class ProxyLibintlConan(ConanFile):
    name = "proxy-libintl"
    version = "0.1"
    description = "This is a trivial minimal library intended to act as a proxy for a dynamically loaded optional libintl"
    topics = ("conan", "libintl")
    url = "https://github.com/bincrafters/conan-proxy-libintl"
    homepage = "https://github.com/frida/proxy-libintl"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0-only"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build_requirements(self):
        if not tools.which("meson"):
            self.build_requires("meson_installer/0.49.0@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/frida/proxy-libintl/archive/%s.tar.gz" % self.version
        tools.get(source_url,
                  sha256="202d90855943091b11ac91863ff5884f0eaf80318a32dc8504fcfdafc65992ed")
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def _configure_meson(self):
        meson = Meson(self)
        defs = dict()
        if self.settings.os == "Linux":
            defs["libdir"] = "lib"
        if str(self.settings.compiler) in ["gcc", "clang"]:
            if self.settings.arch == "x86":
                defs["c_args"] = "-m32"
                defs["cpp_args"] = "-m32"
                defs["c_link_args"] = "-m32"
                defs["cpp_link_args"] = "-m32"
            elif self.settings.arch == "x86_64":
                defs["c_args"] = "-m64"
                defs["cpp_args"] = "-m64"
                defs["c_link_args"] = "-m64"
                defs["cpp_link_args"] = "-m64"
        meson.configure(source_folder=self._source_subfolder,
                        build_folder=self._build_subfolder, defs=defs)
        return meson

    def build(self):
        meson = self._configure_meson()
        meson.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        meson = self._configure_meson()
        meson.install()

    def package_info(self):
        self.cpp_info.libs = ["intl"]
