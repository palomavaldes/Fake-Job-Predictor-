from flask import Flask, request, jsonify, render_template
from job_predictor import predict_job_fraud 

app = Flask(__name__)

# html form
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Fraud Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .glass-card {
            backdrop-filter: blur(20px);
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .pulse-animation {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .floating-shapes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
        }
        
        .shape {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }
        
        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .custom-textarea {
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
        }
        
        .custom-textarea:focus {
            background: rgba(255, 255, 255, 1);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        .custom-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .custom-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .custom-button:hover::before {
            left: 100%;
        }
        
        .custom-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }
        
        .result-animation {
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .shield-icon {
            display: inline-block;
            margin-right: 8px;
            font-size: 1.5em;
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center relative overflow-hidden">
    <!-- Floating Background Shapes -->
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    
    <div class="glass-card p-10 rounded-3xl w-full max-w-lg relative z-10">
        <div class="text-center mb-8">
            <div class="shield-icon pulse-animation">🛡️</div>
            <h1 class="text-4xl font-bold gradient-text mb-2">Job Fraud Predictor</h1>
            <p class="text-gray-600 font-medium">Analyze job postings for potential fraud indicators</p>
        </div>
        
        <form action="/predict" method="post" class="space-y-6">
            <div class="space-y-3">
                <label for="job_description" class="block text-gray-700 text-sm font-semibold mb-2 flex items-center">
                    <span class="mr-2">📝</span>
                    Job Description
                </label>
                <textarea id="job_description" name="job_description" rows="8"
                          class="w-full p-4 border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500
                                 resize-y text-gray-800 custom-textarea placeholder-gray-400"
                          placeholder="Paste the job description here to process it for potential fraud indicators..."></textarea>
            </div>
            
            <button type="submit"
                    class="w-full custom-button text-white py-4 px-6 rounded-2xl
                           focus:outline-none focus:ring-4 focus:ring-purple-300 focus:ring-opacity-50
                           font-semibold text-lg relative z-10">
                <span class="flex items-center justify-center">
                    <span class="mr-2">🔍</span>
                    Analyze Job Posting
                </span>
            </button>
        </form>
        
        <div id="prediction_result" class="mt-8 p-6 rounded-2xl text-center text-lg font-semibold hidden result-animation">
            <!-- Prediction result will be displayed here -->
        </div>
    </div>

    <script>
        document.querySelector('form').addEventListener('submit', async function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const jobDescription = formData.get('job_description');
            const resultDiv = document.getElementById('prediction_result');
            const submitButton = event.target.querySelector('button[type="submit"]');
            
            // Show loading state
            submitButton.innerHTML = '<span class="flex items-center justify-center"><span class="mr-2">⏳</span>Analyzing...</span>';
            submitButton.disabled = true;

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ job_description: jobDescription }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                // Reset button
                submitButton.innerHTML = '<span class="flex items-center justify-center"><span class="mr-2">🔍</span>Analyze Job Posting</span>';
                submitButton.disabled = false;
                
                // Show result with appropriate styling
                resultDiv.classList.remove('hidden');
                resultDiv.classList.add('result-animation');
                
                if (data.prediction === 'Fraudulent Job') {
                    resultDiv.innerHTML = '<span class="text-2xl mr-2">⚠️</span>Prediction: <strong>Fraudulent Job</strong><br><small class="text-sm mt-2 block">This job posting shows potential fraud indicators</small>';
                    resultDiv.classList.remove('bg-green-100', 'text-green-800', 'bg-gray-100', 'text-gray-800');
                    resultDiv.classList.add('bg-red-50', 'text-red-700', 'border-2', 'border-red-200');
                } else if (data.prediction === 'Real Job') {
                    resultDiv.innerHTML = '<span class="text-2xl mr-2">✅</span>Prediction: <strong>Legitimate Job</strong><br><small class="text-sm mt-2 block">This job posting appears to be genuine</small>';
                    resultDiv.classList.remove('bg-red-50', 'text-red-700', 'bg-gray-100', 'text-gray-800', 'border-red-200');
                    resultDiv.classList.add('bg-green-50', 'text-green-700', 'border-2', 'border-green-200');
                } else {
                    resultDiv.innerHTML = '<span class="text-2xl mr-2">❓</span>Unable to determine<br><small class="text-sm mt-2 block">Please try again with a different job description</small>';
                    resultDiv.classList.remove('bg-green-50', 'bg-red-50', 'text-green-700', 'text-red-700', 'border-green-200', 'border-red-200');
                    resultDiv.classList.add('bg-gray-50', 'text-gray-700', 'border-2', 'border-gray-200');
                }

            } catch (error) {
                console.error('Error:', error);
                
                // Reset button
                submitButton.innerHTML = '<span class="flex items-center justify-center"><span class="mr-2">🔍</span>Analyze Job Posting</span>';
                submitButton.disabled = false;
                
                resultDiv.innerHTML = '<span class="text-2xl mr-2">❌</span>Error: Could not get prediction<br><small class="text-sm mt-2 block">Please check your connection and try again</small>';
                resultDiv.classList.remove('hidden');
                resultDiv.classList.add('result-animation');
                resultDiv.classList.remove('bg-green-50', 'bg-red-50', 'text-green-700', 'text-red-700', 'border-green-200', 'border-red-200');
                resultDiv.classList.add('bg-yellow-50', 'text-yellow-700', 'border-2', 'border-yellow-200');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Renders the HTML form for job description input."""
    return HTML_FORM

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives job details via POST request,
    uses the job_predictor to make a prediction,
    and returns the result as JSON.
    """
    data = request.get_json(silent=True) # Try to get JSON data
    if not data:
        # If not JSON, try form data (for direct form submission)
        job_description = request.form.get('job_description')
    else:
        job_description = data.get('job_description')

    if not job_description:
        return jsonify({"error": "No job description provided"}), 400

    # Call the prediction function (which now expects to return more details)
    # NOTE: The predict_job_fraud function in job_predictor.py needs to be updated
    # to return a dictionary with 'prediction', 'confidence', 'probability_real', 'probability_fake'.
    prediction_results = predict_job_fraud(job_description) # Pass the combined text

    # Ensure prediction_results is a dictionary with expected keys
    if isinstance(prediction_results, dict) and 'prediction' in prediction_results:
        return jsonify(prediction_results)
    else:
        # Fallback for old predict_job_fraud or error in job_predictor
        return jsonify({"prediction": prediction_results, "confidence": 0, "probability_real": 0, "probability_fake": 0})


if __name__ == '__main__':
    app.run(debug=True) 
