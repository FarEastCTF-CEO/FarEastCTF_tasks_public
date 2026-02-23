
#include <windows.h>
#include <iostream>
#include <string>
#include <limits>
#include <vector>


static constexpr unsigned char ENC[] = {
   0x4B, 0x81, 0x4C, 0x44, 0x18, 0x41, 0x7D, 0x18, 0x33, 0x52, 0x3B, 0x48, 0x52, 0x3C
};

static constexpr unsigned char XOR1 = 0x5A;
static constexpr unsigned char ADD1 = 0x13;

std::string recover_flag() {
    size_t n = sizeof(ENC) / sizeof(ENC[0]);
    std::string out;
    out.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        unsigned char e = ENC[i];
        unsigned char tmp = static_cast<unsigned char>((e - ADD1) & 0xFF);
        unsigned char orig = static_cast<unsigned char>(tmp ^ XOR1);
        out.push_back(static_cast<char>(orig));
    }
    return out;
}
static std::string GetLastErrorAsString(DWORD code = 0) {
    if (code == 0) code = GetLastError();
    LPSTR msg = nullptr;
    size_t size = FormatMessageA(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL, code, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPSTR)&msg, 0, NULL);
    std::string res;
    if (size && msg) {
        res.assign(msg, size);
        LocalFree(msg);
    }
    else {
        res = "Unknown error " + std::to_string(code);
    }
    return res;
}

int main(int argc, char** argv) {
    std::string launcher = "launcher.exe"; 
    if (argc > 1) launcher = argv[1];


    std::string cmdline = "\"" + launcher + "\"";
    std::vector<char> cmdbuf(cmdline.begin(), cmdline.end());
    cmdbuf.push_back('\0');

    STARTUPINFOA si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

  
    BOOL ok = CreateProcessA(
        NULL,
        cmdbuf.data(),
        NULL, NULL,
        FALSE,
        0,
        NULL,
        NULL,
        &si,
        &pi
    );

    if (!ok) {
        std::cerr << "CreateProcess failed: " << GetLastErrorAsString() << "\n";
        return 1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);

    DWORD exitCode = 0;
    if (!GetExitCodeProcess(pi.hProcess, &exitCode)) {
        std::cerr << "GetExitCodeProcess failed: " << GetLastErrorAsString() << "\n";
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return 1;
    }

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    if (exitCode == 0) {
        std::cout << "Access granted. Here is the flag:\n";
        std::string flag = recover_flag();
        std::cout << "FECTF{" << flag << "}" << std::endl;
    }
    else {
        std::cout << "Access denied. Launcher did not authorize (exit code = " << exitCode << ").\n";
    }

    Sleep(20000);

    return 0;
}
