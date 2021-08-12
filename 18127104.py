#LIB
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import csv

#Parameters
testURL = 'https://testsheepnz.github.io/BasicCalculator.html?fbclid=IwAR0FZv41zYTJOTXZWQ6ERJn6dSmXazRMnvIH4PY2jT0h5XGQU1sk8z6twIQ'
ChromePath = './Driver/chromedriver.exe' #Version 82
FirefoxPath = './Driver/geckodriver.exe' #Version 90
EdgePath= './Driver/msedgedriver.exe'  #Version 92

#Statistics
ChromePass = 0
ChromeFail = 0
EdgePass = 0
EdgeFail = 0
FirefoxPass = 0
FirefoxFail = 0
totalTestCase = 0

def PrintTestCaseStatistics():
    with open('result.txt', mode='w', newline='') as result_file:
        result_file.write(f'Total test case: {int(totalTestCase/3)} \n')
        result_file.write(f'Google Chrome: {ChromePass} PASS, {ChromeFail} FAIL \n')
        result_file.write(f'FireFox: {FirefoxPass} PASS, {FirefoxFail} FAIL \n')
        result_file.write(f'Microsoft Edge: {EdgePass} PASS, {EdgeFail} FAIL \n')
        result_file.write(f'{totalTestCase} test cases were accomplished during the test for three browsers \n')
        result_file.close()


def PrintTestCaseResult(row, actualResult, status, BrowserName):
    if BrowserName=="Firefox":
        if status == "PASS":
            global FirefoxPass
            FirefoxPass+=1
        else:
            global FirefoxFail
            FirefoxFail+=1
    elif BrowserName=="Google Chrome":
        if status == "PASS":
            global ChromePass
            ChromePass+=1
        else:
            global ChromeFail
            ChromeFail+=1
    elif BrowserName=="Microsoft Edge":
        if status == "PASS":
            global EdgePass
            EdgePass+=1
        else:
            global EdgeFail
            EdgeFail+=1
    global totalTestCase
    totalTestCase+=1
    with open('result.csv', mode='a', newline='') as result_file:
        writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([row[0],row[1],str(row[6]), str(actualResult), status, BrowserName])
        
def ExecuteTestCase(row, driver, BrowserName):
    testCaseId = row[0]
    build = row[1]
    firstNumber = row[2]
    operator = row[3]
    secondNumber = row[4]
    isIntOnly = row[5]
    expectedResult = row[6]
    #Build version
    try:
        version = Select(driver.find_element_by_id("selectBuild"))
        version.select_by_visible_text(str(build))
        #First number
        num1 = driver.find_element_by_id("number1Field")
        num1.send_keys(firstNumber)
        # Second number
        num2 = driver.find_element_by_id("number2Field")
        num2.send_keys(secondNumber)
        #Operation
        operation = Select(driver.find_element_by_id("selectOperationDropdown"))
        operation.select_by_visible_text(str(operator))

        # IsInteger check box
        if operator != "Concatenate":
            checkBox = driver.find_element_by_id("integerSelect")
            isChecked = checkBox.is_selected()
            if (isIntOnly=='TRUE' and isChecked==False):
                checkBox.click()
        
        # Calculate button
        calculateButton = driver.find_element_by_id("calculateButton")
        calculateButton.click()
        time.sleep(0.5)

        #Answer
        result = driver.find_element_by_name("numberAnswer")
        actualResult = result.get_attribute('value')
        status = 'FAIL'

        if actualResult=='' or actualResult=='NaN':
            actualResult = 'NONE'

        if actualResult == expectedResult:
            status = 'PASS'
        
        PrintTestCaseResult(row,actualResult, status, BrowserName)
        
        driver.refresh()

    except:
        PrintTestCaseResult(row,'NONE','FAIL', BrowserName)


if __name__ == '__main__':

    #Clean the result file
    with open('result.csv', mode='w', newline='') as writer_file:
        writer = csv.writer(writer_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ID','Build Version', 'Expected Result', 'Actual Result', 'Test Status','Browser Name'])

    with open('input.csv','r') as csv_input:
        reader = csv.reader(csv_input, delimiter = ',')
        next(reader)
        #Define Browser
        driverChrome = webdriver.Chrome(ChromePath)
        driverEdge = webdriver.Edge(executable_path=EdgePath)
        driverFirefox = webdriver.Firefox(executable_path=FirefoxPath)
        for row in reader:
            if(row[0]==''):
                break
            
            driverChrome.get(testURL)
            ExecuteTestCase(row, driverChrome, "Google Chrome")
            
            driverFirefox.get(testURL)
            ExecuteTestCase(row, driverFirefox,"Firefox")
            
            driverEdge.get(testURL)
            ExecuteTestCase(row, driverEdge,"Microsoft Edge")

            PrintTestCaseStatistics()

        driverChrome.close()
        driverFirefox.close()
        driverEdge.close()
        print("ALL TEST CASE HAS BEEN ACCOMPLISHED")
        print("DONE!")