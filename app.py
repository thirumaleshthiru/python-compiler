import sys
import queue
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_code_with_input(code, input_queue, output_queue):
    try:
        # Redirect stdout
        sys.stdout = result_output = StringIO()

        # Compile and execute the code
        compiled_output = compile(code, '<string>', 'exec')
        exec(compiled_output, {'__builtins__': {'input': lambda prompt='': input_queue.get()}})
        
        # Put the captured output into the output queue
        output_queue.put(result_output.getvalue())
    except Exception as e:
        # If any error occurs during compilation or execution, put the error message into the output queue
        output_queue.put(str(e))
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__

@app.route('/compile-run', methods=['POST'])
def compile_run():
    data = request.json
    code = data.get('code')
    inputs = data.get('inputs')

    if code:
        # Initialize input and output queues
        input_queue = queue.Queue()
        output_queue = queue.Queue()

        # Start a thread to run the code
        execution_thread = threading.Thread(target=run_code_with_input, args=(code, input_queue, output_queue))
        execution_thread.start()

        # Provide inputs to the input queue
        if inputs:
            for key, value in inputs.items():
                input_queue.put(value)

        # Wait for the execution thread to finish
        execution_thread.join()

        # Get the output from the output queue
        output_text = output_queue.get()
        return jsonify({'success': True, 'output': output_text})
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
