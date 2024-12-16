import json
import flet as ft
import requests

URL = 'https://www.jma.go.jp/bosai/common/const/area.json'

def main(page: ft.Page):
    page.title = "天気予報"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 地方と県の辞書を作成（修正版）
    areas = {
        "北海道地方": ["北海道"],
        "東北地方": ["青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
        "関東甲信越地方": ["茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "山梨県", "長野県", "新潟県"],
        "東海地方": ["静岡県", "愛知県", "岐阜県", "三重県"],
        "北陸地方": ["富山県", "石川県", "福井県"],
        "近畿地方": ["滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県"],
        "中国地方": ["鳥取県", "島根県", "岡山県", "広島県", "山口県"],
        "四国地方": ["徳島県", "香川県", "愛媛県", "高知県"],
        "九州地方": ["福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県"],
        "沖縄地方": ["沖縄県"],
    }

    # 県コードのマッピング（できる限り正確に）
    prefecture_codes = {
        "北海道": "016000",
        "青森県": "020000",
        "岩手県": "030000",
        "宮城県": "040000",
        "秋田県": "050000",
        "山形県": "060000",
        "福島県": "070000",
        "茨城県": "080000",
        "栃木県": "090000",
        "群馬県": "100000",
        "埼玉県": "110000",
        "千葉県": "120000",
        "東京都": "130000",
        "神奈川県": "140000",
        "新潟県": "150000",
        "富山県": "160000",
        "石川県": "170000",
        "福井県": "180000",
        "山梨県": "190000",
        "長野県": "200000",
        "岐阜県": "210000",
        "静岡県": "220000",
        "愛知県": "230000",
        "三重県": "240000",
        "滋賀県": "250000",
        "京都府": "260000",
        "大阪府": "270000",
        "兵庫県": "280000",
        "奈良県": "290000",
        "和歌山県": "300000",
        "鳥取県": "310000",
        "島根県": "320000",
        "岡山県": "330000",
        "広島県": "340000",
        "山口県": "350000",
        "徳島県": "360000",
        "香川県": "370000",
        "愛媛県": "380000",
        "高知県": "390000",
        "福岡県": "400000",
        "佐賀県": "410000",
        "長崎県": "420000",
        "熊本県": "430000",
        "大分県": "440000",
        "宮崎県": "450000",
        "鹿児島県": "460000",
        "沖縄県": "470000",
    }

    selected_area = None
    selected_prefecture = None
    weather_report = ft.Text(value="県を選択してください")

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
            # 県コードを取得
            prefecture_code = prefecture_codes.get(selected_prefecture)
            
            if prefecture_code:
                try:
                    # 天気予報APIを使用
                    weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefecture_code}.json"
                    response = requests.get(weather_url)
                    
                    if response.status_code == 200:
                        weather_data = response.json()
                        
                        # 天気予報のテキストを抽出（この部分は気象庁のJSONの構造に依存）
                        weather_text = weather_data[0]['timeSeries'][0]['areas'][0]['weathers'][0]
                        weather_report.value = f"{selected_prefecture}の天気予報: {weather_text}"
                    else:
                        weather_report.value = f"エラー: {response.status_code}"
                except Exception as e:
                    weather_report.value = f"エラー: {str(e)}"
            else:
                weather_report.value = f"{selected_prefecture}の県コードが見つかりません"
            
            page.update()

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

ft.app(target=main)