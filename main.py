from sanic import Sanic, response
from pyppeteer import launch


app = Sanic(__name__)
class Browser:
    async def __aenter__(self):
        self.browser = await launch()
        self.page = await self.browser.newPage()
        return self.page

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()


@app.get('/')
async def index(request):
    return response.text('Hello World!')

@app.post('/api')
async def api(request):
    async with Browser() as page:
        await page.goto(request.json['url'])
        await page.screenshot({'path': 'screenshot.png'})
    return await response.file("screenshot.png")

app.run(host='0.0.0.0', port=8080)