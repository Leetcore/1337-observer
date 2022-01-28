import json
import argparse

def main(input_file, output_file):
            with open(input_file, "r") as myfile:
                content = myfile.read()
            json_obj = json.loads(content)

            results = []
            counter = 0
            for program in json_obj["programs"]:
                for domains in program["domains"]:
                    counter = counter + 1
                    results.append(domains)

            result_string = "\n".join(results)
            print(f"BB Programs: {str(len(json_obj['programs']))}, domains: {str(counter)}")
            with open(output_file, "w") as out:
                out.write(result_string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatting a JSON-list to TXT.")
    parser.add_argument("-i", type=str, default="no", help="Path to input file")
    parser.add_argument("-o", type=str, default="bblist.txt", help="Output of BB list.")
    args = parser.parse_args()
    main(args.i, args.o)