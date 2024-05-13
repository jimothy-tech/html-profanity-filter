from bs4 import BeautifulSoup
from profanity_check import predict
import pandas as pd

HTML_PATH = "test.html"

def replace_swear_in_content(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    prose_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a']  # Add more if needed
    for tag in soup.find_all(prose_tags):
        content = tag.string
        if content:
            words = content.split(" ")
            swear_pred_map = pd.DataFrame(
                {
                    "prediction": predict(words),
                    "words" : words
                }
            )
            swear_pred_map['words'] = swear_pred_map.apply(
                lambda row: '****' if row['prediction'] == 1 else row['words'], axis=1
                )
            tag.string = " ".join(swear_pred_map["words"])
    return str(soup)

def main():
    with open("test.html", "r") as f:
        html = f.read()
        censored_html = replace_swear_in_content(html)
        print(censored_html)


if __name__ == "__main__":
    main()