import argparse
import asyncio
from pyppeteer import launch
from os.path import exists
from websockets import client


async def main():
    with open(input_file, "r") as myfile:
        content = myfile.readlines()
        browser = await launch({"ignoreHTTPSErrors": True})
        page = await browser.newPage()
        counter = 0
        for url in content:
            counter = counter + 1
            if exists(output_folder + str(counter) + ".png"):
                continue
            
            # only use url and not banner
            if "," in url:
                url_array = url.split(",")
                url = url_array[0]

            try:
                await page.goto(url)
                await page.addStyleTag(
                    content="html::before { content: '" + url.strip() + "'}"
                )
            except Exception as e:
                continue
            try:
                await page.waitForNavigation(timeout=3)
            except Exception as e:
                pass
            await page.screenshot({"path": output_folder + str(counter) + ".png"})
            print(f"{url.strip()}, {str(counter)}.png")
            with open(output_file, "a") as my_file:
                my_file.write(f"{url.strip()}, {str(counter)}.png\n")
        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take screenshots of URLs")
    parser.add_argument(
        "-i", type=str, default="./input.txt", help="Path to input file"
    )
    parser.add_argument(
        "-o",
        type=str,
        default="./screenshots/screenshot_log.txt",
        help="Path to screenshot log file",
    )
    parser.add_argument(
        "-folder", type=str, default="./screenshots/", help="Path to output folder"
    )
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    output_folder = args.folder
    asyncio.get_event_loop().run_until_complete(main())