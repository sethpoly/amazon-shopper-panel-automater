# amazon-shopper-panel-automater
Fully automate the monthly **Amazon Shopper Panel** tasks by detecting ten email receipts per month &amp; uploading them to Amazon Shopper Panel.

**What is Amazon Shopper Panel?**<br>
Essentially a survey program that rewards you when you share email or paper receipts. 
<br>
<br>
*"Earning rewards is easy. Simply upload 10 eligible receipts per month by using the Amazon Shopper Panel app to take pictures of paper receipts or by forwarding email receipts to receipts@panel.amazon.com and you’ll earn $10 towards either an Amazon Balance or a charitable donation."*

## How it works
- Check the *100* most recent emails I've received from a specified *Gmail* account
- For each email, predict if the email belongs to the **receipt** or **not_receipt** category
- If the resulting prediction is **receipt**, forward the email to *receipts@panel.amazon.com*
- Organize all checked and forwarded emails into separate inboxes to ensure no duplicate entries are made
- Continue until we forward at least *10* emails, and then either a $10 Amazon Balance or a charitable donation will be rewarded to your Amazon account

### **The problem**
I created this because it's too time consuming to manually look through my past emails, and one-by-one forward each receipt-related email to the Amazon Shopper Panel address.
<br>

### **The classifier**
I used a Naive Bayes classifier to determine whether a specific email is a **receipt** or **not_receipt**. This classifier is trained on a simple **Google Sheet** spreadsheet that I update semi-frequently in order to gain a more accurate prediction.

*An example of the spreadsheet that is used to train the classifier. The data set should consist of a multitude of emails that are either a **receipt or not_receipt***
<br>
<img src="https://github.com/sethpoly/amazon-shopper-panel-automater/raw/main/demo/images/spreadsheet.png">
<br>

### **The results**
After parsing, predicting, and forwarding all relevant emails, the emails will be categorized in their own respective inboxes in *Gmail*. This ensures no duplicate entries could ever be classified.
<br>
<br>
In the **Amazon Shopper Panel** app, track the status of the *receipt* emails that were forwarded. If `Not eligible` is next to any of the emails, it just means your classifier made an incorrect prediction. Simply add more entries to the original spreadsheet to gain higher accuracy when predicting.
<br>
<img src="https://github.com/sethpoly/amazon-shopper-panel-automater/raw/main/demo/images/panel.jpg" width=35% height=35%>
<br>

## Quick start
### Configure a new project in *Google Cloud Console* that will be used to access the Google Sheets API
1. Make sure API is enabled, and also enable the **Sheets API** and **Google Drive API**.
2. Add *Service Account Credentials* to your project using `JSON` as the key type. Note down the `Service account ID`, you will need this in order to read/write to your *Google Sheets*. Set the permissions however you'd like, but you really only need *view*.
3. Now a JSON file `google_key.json` should have downloaded from the previous step. This is an important file that is needed to use the *Sheets API* within the project. **This file must be at the root level of the project directory, but it should not be tracked**.
4. Share access to the **Google Sheet that the classifier will train on** using the `Service account ID` you noted down before.
<br>
<img src="https://github.com/sethpoly/amazon-shopper-panel-automater/raw/main/demo/images/sheet_access.png" width=50% height=50%>
<br>
### Configure your Gmail accounts for IMAP and SMTP



## Technology Used
- Python3, Google Sheets API, pandas, sklearn, imap, smtp

### Notes
- There are many other solutions to this problem, but I wanted to go with a legitimate way.
- I now save *20* minutes per month, which I can spend developing other semi-useful programs.

