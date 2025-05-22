cmake_minimum_required(VERSION 3.28)
project(monkeytype)

set(CMAKE_CXX_STANDARD 20)

include(FetchContent)

FetchContent_Declare(
        fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt
        GIT_TAG 10.2.1
)

FetchContent_Declare(
        sfml
        GIT_REPOSITORY https://github.com/sfml/sfml
        GIT_TAG 2.6.1
)

FetchContent_MakeAvailable(fmt)
FetchContent_MakeAvailable(sfml)

add_executable(monkeytype main.cpp
        MainMenu.h
        MainMenu.cpp
        Game.h
        Game.cpp
        Options.h
        Options.cpp
)
target_link_libraries(monkeytype fmt sfml-graphics)
