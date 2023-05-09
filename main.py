import os
import openai
import base64
import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static")

app.debug=True

# Set up OpenAI API key
openai.api_key = os.environ[
  'CHATGPT_API_KEY']



@app.route("/")
def home():
  return render_template("index.html")

@app.route("/picture")
def picture():
  return render_template("picture.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")


@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['image']
  plant_name = get_plant_name(file)
  tips = generate_plant_tips(plant_name)
  return render_template("tips.html", plant_name=plant_name, tips=tips)


def get_plant_name(file):
  images = [base64.b64encode(file.read()).decode("ascii")]
  response = requests.post(
    "https://api.plant.id/v2/identify",
    json={
      "images": images,
      "modifiers": ["similar_images"],
      "plant_details": ["common_names", "url"],
    },
    headers={
      "Content-Type": "application/json",
      "Api-Key": "JuLq8YgkdAcwtNOZGH7gsWgQdICvRdvs9fsMaaRSX7sRHAdu6d",
    }).json()

  return response["suggestions"][0]["plant_name"]


def generate_plant_tips(plant_name):
  # Set up the prompt for the GPT-3 API
  prompt = f"Give me tips for taking care of {plant_name}."

  # Generate tips using the GPT-3 API
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
  )

  # Extract the generated tips from the API response
  tips = response.choices[0].text.strip()

  return tips


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
