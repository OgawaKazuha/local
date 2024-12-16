import json
import flet as ft
import requests
from datetime import datetime, timedelta
import base64

URL = 'https://www.jma.go.jp/bosai/common/const/area.json'

def main(page: ft.Page):
    page.title = "週間天気予報履歴"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 地方と県の辞書を作成
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

    # 県コードのマッピング
    prefecture_codes = {
        "北海道": "016000", "青森県": "020000", "岩手県": "030000", "宮城県": "040000",
        "秋田県": "050000", "山形県": "060000", "福島県": "070000", "茨城県": "080000",
        "栃木県": "090000", "群馬県": "100000", "埼玉県": "110000", "千葉県": "120000",
        "東京都": "130000", "神奈川県": "140000", "新潟県": "150000", "富山県": "160000",
        "石川県": "170000", "福井県": "180000", "山梨県": "190000", "長野県": "200000",
        "岐阜県": "210000", "静岡県": "220000", "愛知県": "230000", "三重県": "240000",
        "滋賀県": "250000", "京都府": "260000", "大阪府": "270000", "兵庫県": "280000",
        "奈良県": "290000", "和歌山県": "300000", "鳥取県": "310000", "島根県": "320000",
        "岡山県": "330000", "広島県": "340000", "山口県": "350000", "徳島県": "360000",
        "香川県": "370000", "愛媛県": "380000", "高知県": "390000", "福岡県": "400000",
        "佐賀県": "410000", "長崎県": "420000", "熊本県": "430000", "大分県": "440000",
        "宮崎県": "450000", "鹿児島県": "460000", "沖縄県": "470000",
    }

    selected_area = None
    selected_prefecture = None
    weather_history = ft.ListView(expand=True, spacing=10, padding=20)

    def on_destination_change(e):
        nonlocal selected_area, selected_prefecture
        selected_index = e.control.selected_index
        selected_area = list(areas.keys())[selected_index]
        selected_prefecture = None
        update_prefectures()

    def on_prefecture_click(e):
        nonlocal selected_prefecture
        selected_prefecture = e.control.content.data
        fetch_weather_history()

    def update_prefectures():
        prefectures_column.controls.clear()
        for prefecture in areas[selected_area]:
            prefecture_button = ft.ElevatedButton(
                content=ft.Text(prefecture, data=prefecture),
                on_click=on_prefecture_click,
            )
            prefectures_column.controls.append(prefecture_button)
        page.update()

    def fetch_weather_history():
        if selected_prefecture is None:
            weather_history.controls.clear()
            weather_history.controls.append(ft.Text("県を選択してください"))
        else:
            # 県コードを取得
            prefecture_code = prefecture_codes.get(selected_prefecture)
            
            if prefecture_code:
                try:
                    # 週間天気予報APIを使用（過去7日分を取得）
                    weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefecture_code}.json"
                    response = requests.get(weather_url)
                    
                    # デバッグのために生のJSONデータを出力
                    print("Raw JSON Response:", response.text)
                    
                    if response.status_code == 200:
                        weather_data = response.json()
                        
                        # JSONデータの構造を詳細に出力
                        print("Weather Data Structure:", json.dumps(weather_data, indent=2, ensure_ascii=False))
                        
                        # 天気予報のクリア
                        weather_history.controls.clear()
                        
                        # タイトルの追加
                        weather_history.controls.append(
                            ft.Text(
                                f"{selected_prefecture}の週間天気予報", 
                                size=20, 
                                weight=ft.FontWeight.BOLD
                            )
                        )
                        
                        # 週間天気予報の表示 - より柔軟な構造解析
                        try:
                            # 最初のタイムシリーズを使用（異なるAPIバージョンに対応）
                            time_series = weather_data[0]['timeSeries']
                            
                            # 週間予報のセクションを見つける
                            weekly_forecast_series = None
                            for series in time_series:
                                if 'weeklys' in series or len(series.get('areas', [])) > 0:
                                    weekly_forecast_series = series
                                    break
                            
                            if weekly_forecast_series:
                                for area in weekly_forecast_series.get('areas', []):
                                    if area['area']['name'] == selected_prefecture:
                                        # 週間の天気情報を取得
                                        weathers = area.get('weathers', [])
                                        temps_max = area.get('tempsMax', [])
                                        temps_min = area.get('tempsMin', [])
                                        
                                        # 7日分の天気予報を表示
                                        for j in range(min(len(weathers), 7)):
                                            # 日付の計算
                                            forecast_date = (datetime.now() + timedelta(days=j)).strftime('%Y-%m-%d')
                                            
                                            # 最高気温と最低気温の表示（存在する場合）
                                            temp_info = ""
                                            if j < len(temps_max) and j < len(temps_min):
                                                temp_info = f"(最高: {temps_max[j]}°C / 最低: {temps_min[j]}°C)"
                                            
                                            # 天気情報の追加
                                            forecast_item = ft.Container(
                                                content=ft.Text(
                                                    f"{forecast_date}: {weathers[j]} {temp_info}",
                                                    size=16
                                                ),
                                                padding=10,
                                                border_radius=10,
                                                bgcolor=ft.colors.BLUE_100
                                            )
                                            weather_history.controls.append(forecast_item)
                                        
                                        break
                            else:
                                weather_history.controls.append(
                                    ft.Text("週間予報のデータが見つかりませんでした", color=ft.colors.RED)
                                )
                        
                        except Exception as parse_error:
                            weather_history.controls.clear()
                            weather_history.controls.append(
                                ft.Text(f"データ解析エラー: {str(parse_error)}", color=ft.colors.RED)
                            )
                            print(f"データ解析エラー詳細: {parse_error}")
                    
                    else:
                        weather_history.controls.clear()
                        weather_history.controls.append(
                            ft.Text(f"エラー: {response.status_code}", color=ft.colors.RED)
                        )
                
                except requests.RequestException as e:
                    weather_history.controls.clear()
                    weather_history.controls.append(
                        ft.Text(f"接続エラー: {str(e)}", color=ft.colors.RED)
                    )
                except json.JSONDecodeError as e:
                    weather_history.controls.clear()
                    weather_history.controls.append(
                        ft.Text(f"JSONデコードエラー: {str(e)}", color=ft.colors.RED)
                    )
                except Exception as e:
                    weather_history.controls.clear()
                    weather_history.controls.append(
                        ft.Text(f"予期せぬエラー: {str(e)}", color=ft.colors.RED)
                    )
            else:
                weather_history.controls.clear()
                weather_history.controls.append(
                    ft.Text(f"{selected_prefecture}の県コードが見つかりません", color=ft.colors.RED)
                )
            
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
                        weather_history,
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

ft.app(target=main)