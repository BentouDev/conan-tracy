newoption {
    trigger = "arch",
    description = "Build for the given architecture",
    value = "ARCH"
}

workspace "tracy"
    configurations { "Debug", "Release" }
    debugformat "C7"

    architecture(_OPTIONS.arch)

    filter { "Debug" }
        symbols "On"

    filter { "Release" }
        optimize "On"

    project "tracy"
        kind("StaticLib")

        defines { "TRACY_ENABLE" }

        includedirs {
            "common",
            "client",
            "."
        }

        files {
            "TracyClient.cpp"
        }
