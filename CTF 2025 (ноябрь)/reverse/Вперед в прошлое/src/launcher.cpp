#include <iostream>
#include <string>
#include <cstdint>
#include <array>
#include <cctype>
#include <limits>
using namespace std;

//"whereisyourlicense"
static constexpr array<uint8_t, 18> ENC = {
    0x40, 0x45, 0x52, 0x3B, 0x52, 0x46, 0x3C, 0x36,
    0x48, 0x42, 0x3B, 0x49, 0x46, 0x4C, 0x52, 0x47,
    0x3C, 0x52
};
static constexpr uint8_t XOR_KEY = 0x5A;
static constexpr uint8_t ADD = 0x13;

static inline string trim(const string& s) {
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a == string::npos) return "";
    size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b - a + 1);
}

string recover_secret() {
    string out;
    out.reserve(ENC.size());
    for (size_t i = 0; i < ENC.size(); ++i) {
        uint8_t e = ENC[i];
        uint8_t tmp = static_cast<uint8_t>((e - ADD) & 0xFF);
        uint8_t orig = static_cast<uint8_t>(tmp ^ XOR_KEY);
        out.push_back(static_cast<char>(orig));
    }
    return out;
}

int main() {
    string keystr;
    cout << "Enter key: ";
    if (!getline(cin, keystr)) return 1;

    keystr = trim(keystr);
    const string expected = recover_secret();

    if (keystr == expected) {
        cout << "OK\n";
        return 0;
    }
    else {
        cout << "INVALID\n";
        return 1;
    }


    cout << "Press Enter to exit...";
    cin.ignore(numeric_limits<streamsize>::max(), ' ');
    cin.get();

    return 0;
}
