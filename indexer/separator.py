import json
import sys


def separate_json(inp, out):
    with open(inp, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(out, 'w', encoding='utf-8') as f:
        for item in data:
            json_str = json.dumps({"index": {}})
            f.write(json_str + '\n')
            json_str = json.dumps(item, ensure_ascii=False)
            f.write(json_str + '\n')

    print(f"Separation completed. Output file: {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        separate_json(input_file, output_file)
