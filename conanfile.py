from conans import ConanFile, tools, AutoToolsBuildEnvironment

class PjprojectConan(ConanFile):
    name = "pjproject"
    version = "2.10-dev"
    settings = "os", "compiler", "build_type", "arch"
    license = "GPL"
    author = "Chrystian Guth"
    exports_sources = "*"
    options = {
        "floating-point" : [True, False],
        "resample" : [True, False],
        "sound" : [True, False],
        "video" : [True, False],
        "small-filter" : [True, False],
        "large-filter" : [True, False],
        "speex-aec" : [True, False],
        "g711-codec" : [True, False],
        "l16-codec" : [True, False],
        "gsm-codec" : [True, False],
        "g722-codec" : [True, False],
        "g7221-codec" : [True, False],
        "speex-codec" : [True, False],
        "ilbc-codec" : [True, False],
        "sdl" : [True, False],
        "ffmpeg" : [True, False],
        "v4l2" : [True, False],
        "openh264" : [True, False],
        "vpx" : [True, False],
        "darwin-ssl" : [True, False],
        "ssl" : [True, False],
        "opencore-amr" : [True, False],
        "silk" : [True, False],
        "opus" : [True, False],
        "bcg729" : [True, False],
        "libyuv" : [True, False],
        "libwebrtc" : [True, False]
    }

    default_options = {
        "floating-point" : True,
        "resample" : True,
        "sound" : True,
        "video" : True,
        "small-filter" : True,
        "large-filter" : True,
        "speex-aec" : False,
        "g711-codec" : False,
        "l16-codec" : False,
        "gsm-codec" : False,
        "g722-codec" : False,
        "g7221-codec" : False,
        "speex-codec" : False,
        "ilbc-codec" : True,
        "sdl" : False,
        "ffmpeg" : False,
        "v4l2" : False,
        "openh264" : False,
        "vpx" : False,
        "darwin-ssl" : True,
        "ssl" : True,
        "opencore-amr" : False,
        "silk" : False,
        "opus" : False,
        "bcg729" : False,
        "libyuv" : False,
        "libwebrtc" : False
    }

    def build_env(self):
        abe = AutoToolsBuildEnvironment(self)
        args = []

        disabled = filter(lambda x: x[1] == 'False', self.options.items())
        disabled = map(lambda x: x[0], disabled)
        disabled_args = map(lambda x: f"--disable-{x}", disabled)
        args.extend(disabled_args)
        
        build = "arm-apple-darwin" if self.settings.arch == "arm64" and self.settings.os == "Macos" else None
        
        abe.configure(args=args, build=build)

        return abe

    def build(self):
        self.build_env().make(target="dep")
        self.build_env().make()

    def package(self):
        self.build_env().make(target="install")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines = ["arm"]
