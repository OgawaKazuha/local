import json
import flet as ft
import requests

URL = 'https://www.jma.go.jp/bosai/common/const/area.json'

def main(page: ft.Page):
    page.title = "天気予報"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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

    # Prefecture to code mapping (you may need to manually create this or get it from a reliable source)
    prefecture_codes = {
        "北海道": "016000",  # この値は正確な値に置き換えてください
        "青森県": "020000",
        "岩手県": "030000",
        # 他の県のコードも追加
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

ft.app(main)