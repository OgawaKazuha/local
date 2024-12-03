import tkinter as tk
import json

# 次のデータを使います：
weather_data = """
... /Users/ash/Lecture/DSprog2/local/jma/areas.json ...
"""

weather_dict = json.loads(weather_data)


def show_weather(area_code):
    # この関数はarea_codeに対応する天気予報を取得し、それを表示します
    for item in weather_dict[0]["timeSeries"]:
        for area in item["areas"]:
            if area["area"]["code"] == area_code:
                print(f"Weather for selected region: {area['weatherCodes']}")  # ここではprintを使用しましたが、実際にはGUI上に表示します

def main():
    root = tk.Tk()

    # 「北海道地方」ボタン
    button_hokkaido = tk.Button(root, text="北海道地方", command=lambda: create_region_buttons("011000"))
    button_hokkaido.pack()

    def create_region_buttons(region_code):
        # TODO: region_codeに基づいて新たな地域のボタンを生成します
        button_region = tk.Button(root, text="宗谷地方", command=lambda: show_weather("011000"))
        button_region.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
