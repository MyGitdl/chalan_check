from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the Challan API! Use /challan/{vehicle_no} to get challan details."}

def get_challan_details(vehicle_no):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.cars24.com/traffic-challan/")
        time.sleep(3)

        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
        )
        input_box.clear()
        input_box.send_keys(vehicle_no)
        time.sleep(1)

        view_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_3qpfi"))
        )
        view_button.click()
        time.sleep(5)

        try:
            challan_container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_2YPNq"))
            )
            challan_data = challan_container.text
        except:
            challan_data = "No challan found"

        return {"vehicle_no": vehicle_no, "challan_details": challan_data}

    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

@app.get("/challan/{vehicle_no}")
def fetch_challan(vehicle_no: str):
    return get_challan_details(vehicle_no)
