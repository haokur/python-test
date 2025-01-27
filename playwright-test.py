from playwright.async_api import async_playwright
import asyncio

cookies = []
async def main():
    # 启动 Playwright
    async with async_playwright() as p:
        # 启动浏览器（非无头模式）
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # 打开一个标签页
        page = await context.new_page()
        await page.goto("https://baidu.com")

        # 定义页面关闭的事件处理函数
        future = asyncio.get_running_loop().create_future()

        # 用于控制轮询的标志位
        stop_polling = False

        # 定义轮询获取 Cookie 的任务
        async def poll_cookies():
            global cookies
            while not stop_polling:
                cookies = await context.cookies()
                await asyncio.sleep(1)  # 每秒轮询一次

        asyncio.create_task(poll_cookies())

        async def on_page_close():
            await browser.close()  # 关闭浏览器
            print("监听到页面关闭，获取到的Cookie是:", cookies)
            future.set_result(None)  # 完成 Future，允许程序退出

        # 注册关闭事件监听器
        page.on("close", lambda: asyncio.create_task(on_page_close()))

        # 等待页面关闭事件完成
        await future

# 运行异步主函数
asyncio.run(main())
