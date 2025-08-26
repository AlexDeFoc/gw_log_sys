#pragma once

#if defined(_WIN32)
#if defined(DontBuildDll)
// building/using static lib → nothing special
#define GW_EXPOSE_TO_DLL
#elif defined(BuildDll)
// building DLL
#define GW_EXPOSE_TO_DLL __declspec(dllexport)
#else
// using DLL
#define GW_EXPOSE_TO_DLL __declspec(dllimport)
#endif
#else
#define GW_EXPOSE_TO_DLL
#endif