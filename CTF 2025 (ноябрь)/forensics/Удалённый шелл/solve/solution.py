import base64


with open('output_for_solution', 'r') as f:
    lines = f.readlines()

text = []

for line in lines:
    line = line.strip()
    decoded = base64.b64decode(line).decode('utf-8')
    print(decoded)
    text.append(decoded)

print(base64.b64decode(text[-3]).decode('utf-8'))