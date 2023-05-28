You can find the code used for the UI in the folder Ui-Code. To debug it, you can download the Visual Studio 2022 Community at the URL https://visualstudio.microsoft.com/vs/community/.

The folder Ui-Code-Compiled-for-Windows contains the UI code compiled for windows to run it. It is necessary to have net 6.0 installed on your machine.

You can find the UI at the URL: https://nba.inovagenetica.com/

If running the UI code is not an option, run the python API localhost and use the following JSON as base for your tests.

{"age":"31","g":"55","gs":"36","mp":"25.6","fga":"2.6","threep":"5.0","twopa":"1.0","efgpercentage":"4%","trb":"8.6","ast":"13.5","stl":"3.8","blk":"9.0","pf":"0.8","pts":"8.8"}

With this json make a Post Request.

I used insomnia for my tests. You can find it in the link below:

https://insomnia.rest/download

If you would like to use the Online version of the API pls uses the URL:

https://inovapythonapis.azurewebsites.net/api/predict

For locally:

http://localhost:7373/api/predict

