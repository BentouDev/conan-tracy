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

        includedirs {
            "common",
            "client"
        }

        files {
            "client/**.cpp",
            "TracyClient.cpp"
        }
