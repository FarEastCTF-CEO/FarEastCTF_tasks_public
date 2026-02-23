#include<iostream>
#include<cstdlib>
#include<string>
#include<array>
using namespace std;
static constexpr array<uint8_t, 19> ENC = { 0x2F, 0x32, 0x2C, 0x21, 0x2F,
											0x34, 0x4A, 0x48, 0x4B, 0x46,
											0x42, 0x3C, 0x18, 0x3C, 0x41,
											0x3B, 0x46, 0x3D, 0x3A};
static constexpr uint8_t XOR_KEY = 0x5A;
static constexpr uint8_t ADD = 0x13;
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

void still_waiting() {
	while (true);
}
void first_path(){
	still_waiting();
	cout << "FECTF{f4k3_fl4g}";
}
void second_path(){
	still_waiting();
	cout << "FECTF{4n07h3r_f4k3_fl4g}";
}
void third_path(int sum) {
	still_waiting();
	int i = sum;
	while (i < 8888) {
		i++;
		if (i < 4141) i = 0;
	}
	string flag = recover_secret();
	cout << "Here is the flag! " << flag << endl;
}


int main() {
	string input;
	cout << "1 - some kind of function\n2 - some other function\n Your choice?\n";
	cin >> input;
	int sum{ 0 };
	for (int i = 0; i < input.length(); i++) sum += (int)input[i];
	still_waiting();
	switch (sum) {
	case 49:
		first_path();
		break;
	case 50:
		second_path();
		break;
	default:
		third_path(sum);
		break;
	}
	system("pause");
	return 0;
}