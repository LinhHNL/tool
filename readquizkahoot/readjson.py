from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
service = Service("D:\Driver\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update this to your chromedriver path

# Path to chromedriver (ensure it's installed on your system)

def get_title(driver):
    try:
        title_element = driver.find_element(By.CLASS_NAME, 'sidebar__Title-sc-2fposs-2')[0]
        title_text = title_element.text
        print(title_text)
        return title_text
    except Exception as e:
        print(f"Error while getting title: {e}")
        return None
# Function to parse the questions using Selenium
def extract_questions(driver):
    questions = []
    # Find the elements that contain the questions
    question_items = driver.find_elements(By.CLASS_NAME, 'question-item__QuestionListItem-sc-1evx9zu-0')
    
    if not question_items:
        print("No question items found.")
        return questions

    for item in question_items:
        try:
            # Try to find the question element
            question_element = item.find_element(By.CLASS_NAME, 'styles__QuestionBlock-sc-19vxqaz-0')
            question_text = question_element.text

            # Click on the question to reveal choices
            question_element.click()
            time.sleep(1)  # Add a small delay to allow choices to load

            # After clicking, get the choices
            choices = item.find_elements(By.CLASS_NAME, 'styles__Choice-sc-19vxqaz-17')

            # Prepare the JSON structure
            options = []

            # Loop through choices and extract text and correctness
            for choice in choices:
                label = choice.get_attribute('aria-label')  # Use get_attribute to access aria-label
                option_text_element = choice.find_element(By.CLASS_NAME, 'styles__Answer-sc-19vxqaz-20')
                option_text = option_text_element.text if option_text_element else ""  # Handle if element is not found
                is_correct = 'incorrect' not in label
                options.append({
                    'option': option_text,
                    'is_correct': is_correct
                })
            
            # Store the question and choices
            question_data = {
                'question': question_text,
                'options': options
            }
            questions.append(question_data)

        except Exception as e:
            print(f"Error while processing a question: {e}")

    return questions

# Function to save questions as JSON
def save_as_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Main function
def main():
    urls = ['https://create.kahoot.it/details/a6e1768e-3574-47ab-9df3-e423ce8d4ea7',
           'https://create.kahoot.it/details/f64db8e9-1d1a-4a52-8e01-1aa0593220c8',
           'https://create.kahoot.it/details/9dc53672-cd55-42ed-bcec-4a5167634d6f',
           'https://create.kahoot.it/details/0c841177-2140-4093-b79c-1074c7737eb6',
           'https://create.kahoot.it/details/b40ec135-46de-48d3-a4a7-05fc12c53537',
           'https://create.kahoot.it/details/b65ae384-f303-406c-bffa-2e1cf9f449d1',
           'https://create.kahoot.it/details/e797801c-1d5f-45fe-9a5c-6ebebb9f99df'

           ]  # Replace with the actual URL
    results = []
    for url in urls:
        driver = webdriver.Chrome(service=service)

        driver.get(url)
        
        # Add delay to allow the page to load fully
        time.sleep(5)
        try:
            # Wait for the button to be clickable, then click it
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_button.click()
            print("Button clicked successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        title = get_title(driver)
        if title:
            print(f"Title: {title}")
        # Extract questions
        questions = extract_questions(driver)
        driver.quit()

        data = {
            'title':title,
            'questions': questions
        }
        results.append(data)
    if results:
        save_as_json(results, 'questions.json')
        print("Questions saved as questions.json")
    else:
        print("No questions found.")

if __name__ == "__main__":
    main()
