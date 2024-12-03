import json
import flet as ft
import requests

URL= 'https://www.jma.go.jp/bosai/common/const/area.json'
data_json = requests.get(URL).json() 

def main(page: ft.Page):
    page.title = "天気予報"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=150,
        min_extended_width=400,
        leading=ft.Text("天気予報", size=30 ,width=150),  # Replace FloatingActionButton with Text
        group_alignment=-0.9,
    )


        # 地方と県の辞書を作成
    areas = {
            "北海道地方": ["空知地域", "後志地域", "石狩地域", "渡島地域", "檜山地域", "上川地域", "留萌地域", "宗谷地域", "オホーツク地域", "胆振地域", "日高地域", "十勝地域", "釧路地域", "根室地域", "千島列島"],
            "東北地方": ["青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
            "関東甲信越地方": ["茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "山梨県", "長野県"],
            "東海地方": ["新潟県", "富山県", "石川県", "福井県", "静岡県", "愛知県", "岐阜県", "三重県"],
            "北陸地方": ["新潟県", "富山県", "石川県", "福井県"],
            "近畿地方": ["滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県"],
            "中国地方（山口県を除く）": ["鳥取県", "島根県", "岡山県", "広島県"],
            "四国地方": ["徳島県", "香川県", "愛媛県", "高知県"],
            "九州地方（山口県を含む）": ["山口県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県"],
            "沖縄地方": ["沖縄県"],
    }

    selected_area = None
    selected_prefecture = None
    weather_report = ft.Text()

    def on_destination_change(e):
        nonlocal selected_area, selected_prefecture
        selected_index = e.control.selected_index
        selected_area = list(areas.keys())[selected_index]
        selected_prefecture = None
        update_prefectures()

    def on_prefecture_click(e):
        nonlocal selected_prefecture
        selected_prefecture = e.control.content.data
        fetch_weather_report()

    def update_prefectures():
        prefectures_column.controls.clear()
        for prefecture in areas[selected_area]:
            prefecture_button = ft.ElevatedButton(
                content=ft.Text(prefecture, data=prefecture),
                on_click=on_prefecture_click,
            )
            prefectures_column.controls.append(prefecture_button)
        page.update()

    def fetch_weather_report():
        if selected_prefecture is None:
            weather_report.value = "県を選択してください"
        else:
        # 県コードを取得する
            prefecture_code = get_prefecture_code(selected_prefecture)
        if prefecture_code:
            # 天気予報APIを使って、selected_prefectureの天気予報を取得する
            weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefecture_code}.json"
            response = requests.get(weather_url)
            if response.status_code == 200:
                weather_data = areas.json()
                # 取得した天気予報をweather_report.valueに設定する
                weather_report.value = f"{selected_prefecture}の天気予報: {weather_data['text']}"
            else:
                weather_report.value = f"エラー: {response.status_code}"
        else:
            weather_report.value = f"{selected_prefecture}の県コードが見つかりません"
            page.update()

    def get_prefecture_code(prefecture_name):
        for center_code, center_data in data_json["centers"].items():
            if prefecture_name in center_data["children"]:
                return prefecture_name
        for child_code in center_data["children"]:
            if data_json["offices"][child_code]["name"] == prefecture_name:
                return child_code
        return None
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.LOCATION_ON, label=area)
            for area in areas.keys()
        ],
        on_change=on_destination_change,
    )

    prefectures_column = ft.Column()

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        prefectures_column,
                        weather_report,
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

ft.app(main)