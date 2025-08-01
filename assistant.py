
import difflib

qa_pairs = {
    "what is energy forecasting?": "Energy forecasting is the process of predicting future energy consumption based on historical usage data.",
    "how to detect inefficiencies in energy use?": "You can detect inefficiencies by analyzing usage trends and identifying abnormal spikes or patterns.",
    "what is a kwh?": "A kilowatt-hour (kWh) is a measure of energy consumption. It represents one kilowatt of power used for one hour.",
    "how to reduce energy usage?": "Turn off unused devices, use energy-efficient appliances, and monitor your consumption regularly."
}

def get_response(user_input):
    questions = list(qa_pairs.keys())
    match = difflib.get_close_matches(user_input.lower(), questions, n=1, cutoff=0.5)
    if match:
        return qa_pairs[match[0]]
    return "Sorry, I don't know the answer to that. Try asking something else about energy analytics."
