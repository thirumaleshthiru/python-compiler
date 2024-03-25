 import sys
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_python_code(code, input_data=None):
    try:
        # Redirect stdout and stdin
        sys.stdout = result_output = StringIO()
        if input_data:
            sys.stdin = StringIO(input_data)

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
        # Reset stdout and stdin to their default values
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

@app.route('/compile-run', methods=['POST'])
def compile_run():
    data = request.json
    code = data.get('code')
    input_data = data.get('input')  # assuming input is provided in the request

    if code:
        # Call the function to compile and run the provided Python code
        result = compile_and_run_python_code(code, input_data)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 
