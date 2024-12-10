import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()


def send_email(tracking_info: str) -> None:
    # Email configuration
    sender_email = os.getenv("EMAIL") # Replace with your iCloud email
    app_specific_password = os.getenv("APP_PASSWORD") # Generate this in your Apple ID settings
    receiver_email = sender_email  # Sending to yourself
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"TNT Tracking Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    body = f"Latest tracking information:\n\n{tracking_info}"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.mail.me.com', 587)
        server.starttls()
        server.login(sender_email, app_specific_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        page.goto("https://radar.tntbrasil.com.br/radar/public/localizacaoSimplificada.do")
        page.get_by_text("Remetente").click()
        page.get_by_label("Destinatário").click()
        page.locator("#nrIdentificacao").click()
        page.locator("#nrIdentificacao").fill(os.getenv("CPF"))
        page.get_by_text("Doc. Serviço").click()
        page.get_by_text("Nota Fiscal").click()
        page.locator("#nrDocumento").click()
        page.locator("#nrDocumento").fill(os.getenv("NOTA"))
        page.get_by_role("button", name="Buscar").click()
        page.get_by_text("215185").click()
        
        # Aguarda a página carregar completamente
        time.sleep(5)
        
        # Espera pela tabela e extrai os dados
        first_row = page.evaluate('''() => {
            const tables = document.getElementsByTagName('table');
            if (tables.length > 0) {
                const rows = tables[0].rows;
                if (rows.length > 0) {
                    const cells = rows[1].cells;
                    if (cells.length >= 3) {
                        return {
                            date: cells[0].innerText.trim(),
                            status: cells[1].innerText.trim(),
                            location: cells[2].innerText.trim()
                        };
                    }
                }
            }
            return null;
        }''')
        
        if first_row:
            tracking_info = f"Data: {first_row['date']}\nStatus: {first_row['status']}\nLocal: {first_row['location']}"
            print("Informações capturadas:")
            print(tracking_info)  # Para debug
            send_email(tracking_info)
        else:
            print("Não foi possível encontrar as informações na tabela")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run(playwright)