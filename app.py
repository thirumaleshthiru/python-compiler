import sys
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_python_code(code):
    try:
        # Redirect stdout to capture the output
        sys.stdout = result_output = StringIO()
        
        # Compile and execute the code
        compiled_output = compile(code, '<string>', 'exec')
        exec(compiled_output)
        
        # Get the captured output
        output_text = result_output.getvalue()
        return {'success': True, 'output': output_text}
    except Exception as e:
        # If any error occurs during compilation or execution, return the error message
        return {'success': False, 'error': str(e)}
    finally:
        # Reset stdout to its default value
        sys.stdout = sys.__stdout__

@app.route('/compile-run', methods=['POST'])
def compile_run():
    data = request.json
    code = data.get('code')

    if code:
        # Call the function to compile and run the provided Python code
        result = compile_and_run_python_code(code)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})
if __name__ == '__main__':
    app.run(debug=True, port=8080)
