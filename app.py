from flask import Flask, request, jsonify, render_template, redirect, url_for
import openai
from flask_cors import CORS
import re
from models.user import User
import string
history = []
current_user = None

app = Flask(__name__, static_folder='.', static_url_path='')

# Enable CORS
CORS(app)

# Configure OpenAI API Key
openai.api_key = 'put your Api key'


@app.route('/', methods=['GET', 'POST'])
def landing():
    global current_user  # Declare that you're using the global variable
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        interests = request.form['interests']
        current_topic = request.form['currentTopic']
        # Create the user object
        user_instance = User(name, gender, age, interests, current_topic)
        # Set the global variable
        current_user = user_instance
        # Redirect to the chat page
        return redirect(url_for('chat_page'))
    return render_template('landing.html')

@app.route('/chat')
def chat_page():
    return render_template('index.html', user_name=current_user.name)


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message','')
    user_message = []
    get_suggestions = request.json.get('get_suggestions', False)
    refresh_clicked = request.json.get('refresh_clicked', False)  
    

    test_mode = request.json.get('test_mode', False)  # Check if test_mode is active
    # If test_mode is active, return a dummy response and suggestions
    if test_mode:
        return jsonify({
            "response": "This is a test response This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.This is a test response.",
            "suggestions": ["Test suggestion 1 Test suggestion 1 This is a test response", "Test suggestioTest suggestion 1n 2 Test suggestion 1 Test suggestion 1", "Test suggestion 3Test suggestion 3Test suggestion 3Test suggestion 3"]
        })
    
    # Construct the message for the OpenAI API
    if isinstance(user_input, list) and user_input:
        message_payload = {
            "role": "system",
            "content": f"You are a professional teacher specializing in {current_user.current_topic}. have a talent for explaining complex topics in a simple and engaging manner. this is you student persona, {current_user.persona}. base on that give him answer that will be special for him."
        }

        user_message.insert(0, message_payload)
        messages = user_message
    
    # If get_suggestions flag is True, generate suggestions based on user_message
    if get_suggestions or refresh_clicked:
        prompt_for_suggestions = (f"We under the topic \"{current_user.current_topic}\"," 
                          f"before i asked you about \"{current_user.search_history[-1]}\" and this is the summary of your respond \"{current_user.summaries[-1]}\"."        
                          "i want to get dipper in the learning, provide a list of three suggestions for further learning, please make them shourt as possible, no more then 6 word each:")
        if refresh_clicked:
            previous_suggestions = request.json.get('previous_suggestions', [])
            prompt_for_suggestions = (f"this is the previus suggestions{previous_suggestions}, i dont like the give me differents one.") + prompt_for_suggestions
        messages = [
            {"role": "user", "content": prompt_for_suggestions}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            suggestions_text = response.choices[0].message['content']
            suggestion_lines = suggestions_text.split('\n')
            suggestions = [re.sub(r'^\d+\.\s*', '', line).strip(string.punctuation).strip() 
               for line in suggestion_lines if re.match(r'^\d+\.', line)]
            
            return jsonify({"suggestions": suggestions})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    # Otherwise, get the main response
    try:
        if (user_input[-1]):
            current_user.search_history.append(user_input[-1])
        teacher_prompt = (f"at the end give Summary:. please give a short answer. {current_user.name} wants to know about {current_user.search_history[-1]}. "
                          f"First, provide a brief, short, concise, and engaging exaplnation about that"
                          f" you can Include simple details and a fun analogy base on {current_user.name} persona. \n\n new line.  ""Summary"": describe in 6 words only the topic we covered.")
        if (current_user.summaries):
            teacher_prompt = current_user.summaries[-1] + teacher_prompt
        messages=messages + [{"role": "user", "content": teacher_prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        main_response = response.choices[0].message['content']
        summary_pattern = re.compile(r'(?:summary|summarize|to summarize in 6 words:|to summarize|six words)[,:]\s*(.*)', re.IGNORECASE)
        match = summary_pattern.search(main_response)
        if match:
            summary = match.group(1).strip()
            current_user.add_summary(summary)
            message_without_summary = main_response.replace(match.group(0), '').strip()
        else:
            message_without_summary = main_response

        return jsonify({"response": message_without_summary})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
