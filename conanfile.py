from conans import ConanFile, tools, AutoToolsBuildEnvironment

class PjprojectConan(ConanFile):
    name = "pjproject"
    version = "2.10-dev"
    settings = "os", "compiler", "build_type", "arch", "arch_build"
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

    def is_apple_silicon(self):
        return self.settings.arch == "arm64" and self.settings.os == "Macos"

    def build_env(self):
        abe = AutoToolsBuildEnvironment(self)
        args = []

        enabled_disabled_args = map(lambda x: f"""--{"dis" if x[1] == "False" else "en"}able-{x[0]}""", self.options.items())
        args.extend(enabled_disabled_args)

        args.extend(["--enable-darwin-ssl"] if self.is_apple_silicon() else [])
        
        build = "arm-apple-darwin" if self.is_apple_silicon() else None

        defines = [
            "ARM",
            "PJ_IS_LITTLE_ENDIAN=1",
            "PJ_IS_BIG_ENDIAN=0",
            "PJ_HAS_SSL_SOCK=1",
            "PJ_SSL_SOCK_IMP=PJ_SSL_SOCK_IMP_APPLE",
            "PJSIP_HAS_TLS_TRANSPORT=1",
            "PJMEDIA_ILBC_CODEC_USE_COREAUDIO=1",
            "PJMEDIA_HAS_ILBC_CODEC=1",
            "PJMEDIA_AUDIO_DEV_HAS_COREAUDIO=1",
            "PJMEDIA_AUDIO_DEV_HAS_WMME=0",
            "PJMEDIA_AUDIO_DEV_HAS_PORTAUDIO=0",
            "PJ_HAS_FLOATING_POINT=1",
            "PJMEDIA_HAS_SPEEX_AEC=0"
        ] if self.is_apple_silicon() else []

        abe.defines.extend(defines)

        abe.configure(args=args, build=build)


        # command = f"""CFLAGS="{flags}" CXXFLAGS="{flags}" LDFLAGS="{flags}" ./configure {build} {" ".join(args)}"""
        
        # self.output.info(command)

        # with tools.environment_append(abe.vars):
        #     self.run(command)
        return abe

    def build(self):
        self.build_env().make(target="dep")
        self.build_env().make(target="lib")

    def package(self):
        self.build_env().make(target="install")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        defines = []
        defines.extend(
            [
                "ARM",
                "PJ_IS_LITTLE_ENDIAN=1",
                "PJ_IS_BIG_ENDIAN=0",
                "PJ_HAS_SSL_SOCK=1",
                "PJ_SSL_SOCK_IMP=PJ_SSL_SOCK_IMP_APPLE",
                "PJSIP_HAS_TLS_TRANSPORT=1",
                "PJMEDIA_ILBC_CODEC_USE_COREAUDIO=1",
                "PJMEDIA_HAS_ILBC_CODEC=1",
                "PJMEDIA_AUDIO_DEV_HAS_COREAUDIO=1",
                "PJMEDIA_AUDIO_DEV_HAS_WMME=0",
                "PJMEDIA_AUDIO_DEV_HAS_PORTAUDIO=0",
                "PJ_HAS_FLOATING_POINT=1",
                "PJMEDIA_HAS_SPEEX_AEC=0"
            ]
        )

        self.cpp_info.defines.extend(defines)
        
