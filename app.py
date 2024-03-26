import sys
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_python_code(code, inputs=None):
    try:
        # Redirect stdout and stdin
        sys.stdout = result_output = StringIO()
        sys.stdin = StringIO()  # Create a StringIO object to simulate stdin

        if inputs:
            # Set up the simulated stdin for multiple inputs
            input_values = inputs.values()
            input_values.reverse()  # Reverse the input values to simulate FIFO order
            sys.stdin.write('\n'.join(input_values))
            sys.stdin.seek(0)  # Reset the position to the beginning of the simulated stdin

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
    inputs = data.get('inputs')

    if code:
        result = compile_and_run_python_code(code, inputs)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
