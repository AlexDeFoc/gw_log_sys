#pragma once

// gw_log_sys --- Logging library used by gameWatch
// Copyright 2025 - Sava Alexandru-Andrei
// Licensed under the MIT Licence. See LICENSE.md file in project root.

#if defined(_WIN32)
    // on windows
    #if defined(DONT_BUILD_DLL__GW_LOG_SYS)
        // building/using static lib
        #define GW_LOG_SYS_API
    #elif defined(BUILD_DLL__GW_LOG_SYS)
        // building shared lib
        #define GW_LOG_SYS_API __declspec(dllexport)
    #else
        // using shared lib
        #define GW_LOG_SYS_API __declspec(dllimport)
    #endif
#else
    // on other os then windows
    #define GW_LOG_SYS_API
#endif
