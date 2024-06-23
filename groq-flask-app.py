import requests
import os
from groq import Groq
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def data_receiver():
    data = request.json  # Assuming JSON data
    # Here you can process your data or call another function
    response = process_data(data)
    return jsonify(response)


def process_data(data):
    # Your data processing logic here
    paper_1_info = data['paper_1_info']
    paper_2_info = data['paper_2_info']
    
    client = Groq(
        # This is the default and can be omitted
        api_key=os.getenv('GROQ_API_KEY'),
    )
    chat_completion = client.chat.completions.create(

    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Compare these two papers and summarise the similarities and differences in {} lines. Paper 1: {} Paper 2: {}".format(3, paper_1_info, paper_2_info)
            }
        ],

        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    print(chat_completion.choices[0].message.content)
    return {"status": "Processed", "data": chat_completion.choices[0].message.content}

if __name__ == '__main__':
    app.run(debug=True)
