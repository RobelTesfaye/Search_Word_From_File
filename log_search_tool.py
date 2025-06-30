from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Function to search for a string in a file and return matching lines
def search_in_file(file_path, search_string):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if search_string in line:
                    filename = os.path.basename(file_path)
                    results.append(f"<div class='result'>"
                                   f"<strong>File:</strong> {filename}<br>"
                                   f"<strong>Line:</strong> {line_number}<br>"
                                   f"<strong>Content:</strong> {line.strip()}<br>"
                                   f"<hr></div>")
    except Exception as e:
        results.append(f"Error reading file {file_path}: {e}")
    return results

# Function to traverse a directory and search in all files with .log extension
def search_logs_in_directory(directory_path, search_string):
    search_results = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                search_results.extend(search_in_file(file_path, search_string))
    return search_results

@app.route('/', methods=['GET'])
def index():
    directory_path = request.args.get('directory_path')
    search_string = request.args.get('search_string')
    if directory_path and search_string:
        if os.path.exists(directory_path):
            results = search_logs_in_directory(directory_path, search_string)
            return render_template('results.html', search_string=search_string, results=results)
        else:
            return "The provided directory path does not exist.", 400
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
