import json
import flet as ft
import requests
import sqlite3
from datetime import datetime, timedelta

class WeatherApp:
    def __init__(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect('weather_areas.db')
        self.create_database()

    def create_database(self):
        """
        データベースを作成し、地域と県コードのテーブルを初期化する
        """
        cursor = self.conn.cursor()
        
        # テーブルが存在しない場合に作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY,
            area TEXT NOT NULL,
            prefecture TEXT NOT NULL,
            prefecture_code TEXT NOT NULL
        )
        ''')
        
        # データがない場合に初期データを挿入
        cursor.execute('SELECT COUNT(*) FROM areas')
        if cursor.fetchone()[0] == 0:
            areas_data = [
                ('北海道', '北海道', '017000'),
                ('東北', '青森県', '020000'),
                ('東北', '岩手県', '030000'),
                ('東北', '宮城県', '040000'),
                ('東北', '秋田県', '050000'),
                ('東北', '山形県', '060000'),
                ('東北', '福島県', '070000'),
                ('関東', '茨城県', '080000'),
                ('関東', '栃木県', '090000'),
                ('関東', '群馬県', '100000'),
                ('関東', '埼玉県', '110000'),
                ('関東', '千葉県', '120000'),
                ('関東', '東京都', '130000'),
                ('関東', '神奈川県', '140000'),
                ('中部', '新潟県', '150000'),
                ('中部', '富山県', '160000'),
                ('中部', '石川県', '170000'),
                ('中部', '福井県', '180000'),
                ('中部', '山梨県', '190000'),
                ('中部', '長野県', '200000'),
                ('中部', '岐阜県', '210000'),
                ('中部', '静岡県', '220000'),
                ('中部', '愛知県', '230000'),
                ('近畿', '三重県', '240000'),
                ('近畿', '滋賀県', '250000'),
                ('近畿', '京都府', '260000'),
                ('近畿', '大阪府', '270000'),
                ('近畿', '兵庫県', '280000'),
                ('近畿', '奈良県', '290000'),
                ('近畿', '和歌山県', '300000'),
                ('中国', '鳥取県', '310000'),
                ('中国', '島根県', '320000'),
                ('中国', '岡山県', '330000'),
                ('中国', '広島県', '340000'),
                ('中国', '山口県', '350000'),
                ('四国', '徳島県', '360000'),
                ('四国', '香川県', '370000'),
                ('四国', '愛媛県', '380000'),
                ('四国', '高知県', '390000'),
                ('九州', '福岡県', '400000'),
                ('九州', '佐賀県', '410000'),
                ('九州', '長崎県', '420000'),
                ('九州', '熊本県', '430000'),
                ('九州', '大分県', '440000'),
                ('九州', '宮崎県', '450000'),
                ('九州', '鹿児島県', '460000'),
                ('九州', '沖縄県', '471000')
            ]
            cursor.executemany('''
                INSERT INTO areas (area, prefecture, prefecture_code) 
                VALUES (?, ?, ?)
            ''', areas_data)
        
        self.conn.commit()

    def get_areas(self):
        """
        地域の一覧を取得する
        :return: 地域のリスト
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT area FROM areas')
        return [row[0] for row in cursor.fetchall()]

    def get_prefectures(self, area):
        """
        指定された地域の県のリストを取得する
        :param area: 地域名
        :return: 県のリスト
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT prefecture FROM areas WHERE area = ?', (area,))
        return [row[0] for row in cursor.fetchall()]

    def get_prefecture_code(self, prefecture_name):
        """
        県名から県コードを取得する
        :param prefecture_name: 県名
        :return: 県コード
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT prefecture_code FROM areas WHERE prefecture = ?', (prefecture_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def fetch_weather_report(self, prefecture_name, selected_date=None):
        """
        選択された日付の天気予報を取得
        :param prefecture_name: 都道府県名
        :param selected_date: 選択された日付 (デフォルトは今日)
        :return: 天気予報情報
        """
        prefecture_code = self.get_prefecture_code(prefecture_name)
        
        if not prefecture_code:
            return f"{prefecture_name}の県コードが見つかりません"

        try:
            # 天気予報APIを使用
            weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefecture_code}.json"
            response = requests.get(weather_url)
            
            if response.status_code == 200:
                weather_data = response.json()
                
                # デフォルトは今日の予報
                if not selected_date:
                    selected_date = datetime.now()
                
                # JSONデータから適切な予報を検索
                for forecast in weather_data[0]['timeSeries']:
                    for area in forecast['areas']:
                        if 'timeDefines' in forecast:
                            for i, time_def in enumerate(forecast['timeDefines']):
                                forecast_date = datetime.fromisoformat(time_def.replace('Z', '+00:00'))
                                
                                # 日付が一致する予報を探す
                                if (forecast_date.date() == selected_date.date() and 
                                    'weathers' in area and i < len(area['weathers'])):
                                    return (f"{prefecture_name}の{forecast_date.strftime('%Y-%m-%d')}の天気予報: "
                                            f"{area['weathers'][i]}")
                
                return f"{prefecture_name}の選択された日付の予報が見つかりませんでした"
            else:
                return f"エラー: {response.status_code}"
        except Exception as e:
            return f"エラー: {str(e)}"

    def main(self, page: ft.Page):
        page.title = "天気予報 (日付選択版)"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # これらの変数は後でnonlocalで参照されるため、ここで定義
        selected_area = None
        selected_prefecture = None
        selected_date = datetime.now()
        
        weather_report = ft.Text(value="県を選択してください")
        date_picker = ft.DatePicker(
            first_date=datetime.now() - timedelta(days=7),  # 過去7日間から選択可能
            last_date=datetime.now() + timedelta(days=7),   # 今後7日間まで選択可能
        )

        def on_destination_change(e):
            nonlocal selected_area, selected_prefecture
            selected_index = e.control.selected_index
            selected_area = self.get_areas()[selected_index]
            selected_prefecture = None
            update_prefectures()

        def on_prefecture_click(e):
            nonlocal selected_prefecture
            selected_prefecture = e.control.content.data
            update_weather_report()

        def update_prefectures():
            # 選択された地域の県リストを更新
            prefectures = self.get_prefectures(selected_area)
            prefectures_column.controls.clear()
            for prefecture in prefectures:
                prefectures_column.controls.append(
                    ft.ElevatedButton(
                        prefecture, 
                        on_click=on_prefecture_click,
                        data=prefecture
                    )
                )
            page.update()

        def update_weather_report():
            if selected_prefecture:
                weather_report.value = self.fetch_weather_report(
                    selected_prefecture, 
                    selected_date
                )
                page.update()

        def on_date_change(e):
            nonlocal selected_date
            selected_date = e.control.value
            update_weather_report()

        def show_date_picker(e):
            date_picker.pick_date()

        # DatePickerのon_changeイベントを設定
        date_picker.on_change = on_date_change

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.LOCATION_ON, label=area)
                for area in self.get_areas()
            ],
            on_change=on_destination_change,
        )

        date_button = ft.ElevatedButton(
            "日付を選択", 
            on_click=show_date_picker
        )

        prefectures_column = ft.Column()

        page.overlay.append(date_picker)
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            date_button,
                            prefectures_column,
                            weather_report,
                        ],
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

    def __del__(self):
        """Close database connection when done"""
        self.conn.close()

def main(page: ft.Page):
    app = WeatherApp()
    app.main(page)

ft.app(target=main)