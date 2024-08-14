import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = ''

def analyze_with_chatgpt(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Anda bisa mengganti dengan "gpt-3.5-turbo" jika diperlukan
            messages=[
                {"role": "system", "content": "Buatkan berita baru dari berita ini menjadi berita yang lebih bagus. Setiap kutipan harus diletakkan pada paragraf yang terpisah, dan narasi sebelum kutipan harus dibuat semenarik mungkin sesuai dengan isi dari kutipan berikutnya. Juga, buatkan 10 hashtag yang relevan di bawah berita."},
                {"role": "user", "content": text}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    title = None
    article = None
    improved_article = None
    
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text() if soup.find('title') else "Title not found"
            
            # Find the main article content
            article_content = soup.find('article') or soup.find('div', {'class': 'content'}) or soup.find('div', {'class': 'post-content'})
            article = article_content.get_text() if article_content else "Article content not found"
            
            # Analyze and improve article with ChatGPT
            improved_article = analyze_with_chatgpt(article)
            
        except Exception as e:
            title = f"Error: {str(e)}"
            article = ""
            improved_article = ""
    
    return render_template('index.html', title=title, article=article, improved_article=improved_article)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
