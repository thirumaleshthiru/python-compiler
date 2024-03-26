import sys
from io import StringIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def compile_and_run_python_code(code, inputs=None):
    try:
        # Redirect stdout
        sys.stdout = result_output = StringIO()

        # Define a function to read inputs from a list
        def custom_input(prompt):
            if inputs and len(inputs) > 0:
                return str(inputs.pop(0))
            else:
                return ''

        # Replace input() calls with custom_input() calls
        code = code.replace('input(', 'custom_input(')

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
    inputs = data.get('inputs')

    if code:
        result = compile_and_run_python_code(code, inputs)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
