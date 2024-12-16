import json
import flet as ft
import requests
import sqlite3

# データベースの初期化とデータの挿入
class WeatherApp:
    def __init__(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect('weather_areas.db')
        self.create_database()

    def create_database(self):
        """Create necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create areas table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        ''')
        
        # Create prefectures table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prefectures (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            code TEXT UNIQUE,
            area_id INTEGER,
            FOREIGN KEY (area_id) REFERENCES areas(id)
        )
        ''')
        
        # Populate areas if empty
        cursor.execute('SELECT COUNT(*) FROM areas')
        if cursor.fetchone()[0] == 0:
            areas = [
                "北海道地方",
                "東北地方",
                "関東甲信越地方",
                "東海地方",
                "北陸地方",
                "近畿地方",
                "中国地方",
                "四国地方",
                "九州地方",
                "沖縄地方"
            ]
            cursor.executemany('INSERT INTO areas (name) VALUES (?)', 
                               [(area,) for area in areas])
        
        # Populate prefectures if empty
        cursor.execute('SELECT COUNT(*) FROM prefectures')
        if cursor.fetchone()[0] == 0:
            prefectures_data = [
                ("北海道", "016000", "北海道地方"),
                ("青森県", "020000", "東北地方"),
                ("岩手県", "030000", "東北地方"),
                ("宮城県", "040000", "東北地方"),
                ("秋田県", "050000", "東北地方"),
                ("山形県", "060000", "東北地方"),
                ("福島県", "070000", "東北地方"),
                ("茨城県", "080000", "関東甲信越地方"),
                ("栃木県", "090000", "関東甲信越地方"),
                ("群馬県", "100000", "関東甲信越地方"),
                ("埼玉県", "110000", "関東甲信越地方"),
                ("千葉県", "120000", "関東甲信越地方"),
                ("東京都", "130000", "関東甲信越地方"),
                ("神奈川県", "140000", "関東甲信越地方"),
                ("新潟県", "150000", "関東甲信越地方"),
                ("富山県", "160000", "北陸地方"),
                ("石川県", "170000", "北陸地方"),
                ("福井県", "180000", "北陸地方"),
                ("山梨県", "190000", "関東甲信越地方"),
                ("長野県", "200000", "関東甲信越地方"),
                ("岐阜県", "210000", "東海地方"),
                ("静岡県", "220000", "東海地方"),
                ("愛知県", "230000", "東海地方"),
                ("三重県", "240000", "東海地方"),
                ("滋賀県", "250000", "近畿地方"),
                ("京都府", "260000", "近畿地方"),
                ("大阪府", "270000", "近畿地方"),
                ("兵庫県", "280000", "近畿地方"),
                ("奈良県", "290000", "近畿地方"),
                ("和歌山県", "300000", "近畿地方"),
                ("鳥取県", "310000", "中国地方"),
                ("島根県", "320000", "中国地方"),
                ("岡山県", "330000", "中国地方"),
                ("広島県", "340000", "中国地方"),
                ("山口県", "350000", "中国地方"),
                ("徳島県", "360000", "四国地方"),
                ("香川県", "370000", "四国地方"),
                ("愛媛県", "380000", "四国地方"),
                ("高知県", "390000", "四国地方"),
                ("福岡県", "400000", "九州地方"),
                ("佐賀県", "410000", "九州地方"),
                ("長崎県", "420000", "九州地方"),
                ("熊本県", "430000", "九州地方"),
                ("大分県", "440000", "九州地方"),
                ("宮崎県", "450000", "九州地方"),
                ("鹿児島県", "460000", "九州地方"),
                ("沖縄県", "470000", "沖縄地方")
            ]
            
            # First, add area_ids
            for prefecture, code, area in prefectures_data:
                cursor.execute('''
                    INSERT INTO prefectures (name, code, area_id) 
                    VALUES (?, ?, (SELECT id FROM areas WHERE name = ?))
                ''', (prefecture, code, area))
        
        self.conn.commit()

    def get_areas(self):
        """Retrieve all areas"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM areas')
        return [row[0] for row in cursor.fetchall()]

    def get_prefectures_by_area(self, area_name):
        """Retrieve prefectures for a given area"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.name 
            FROM prefectures p
            JOIN areas a ON p.area_id = a.id
            WHERE a.name = ?
        ''', (area_name,))
        return [row[0] for row in cursor.fetchall()]

    def get_prefecture_code(self, prefecture_name):
        """Get prefecture code for a given prefecture name"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT code FROM prefectures WHERE name = ?', (prefecture_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def fetch_weather_report(self, prefecture_name):
        """Fetch weather report for a given prefecture"""
        prefecture_code = self.get_prefecture_code(prefecture_name)
        
        if not prefecture_code:
            return f"{prefecture_name}の県コードが見つかりません"

        try:
            # 天気予報APIを使用
            weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefecture_code}.json"
            response = requests.get(weather_url)
            
            if response.status_code == 200:
                weather_data = response.json()
                
                # 天気予報のテキストを抽出（この部分は気象庁のJSONの構造に依存）
                weather_text = weather_data[0]['timeSeries'][0]['areas'][0]['weathers'][0]
                return f"{prefecture_name}の天気予報: {weather_text}"
            else:
                return f"エラー: {response.status_code}"
        except Exception as e:
            return f"エラー: {str(e)}"

    def main(self, page: ft.Page):
        page.title = "天気予報 (SQLite版)"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        selected_area = None
        selected_prefecture = None
        weather_report = ft.Text(value="県を選択してください")

        def on_destination_change(e):
            nonlocal selected_area, selected_prefecture
            selected_index = e.control.selected_index
            selected_area = self.get_areas()[selected_index]
            selected_prefecture = None
            update_prefectures()

        def on_prefecture_click(e):
            nonlocal selected_prefecture
            selected_prefecture = e.control.content.data
            weather_report.value = self.fetch_weather_report(selected_prefecture)
            page.update()

        def update_prefectures():
            prefectures_column.controls.clear()
            for prefecture in self.get_prefectures_by_area(selected_area):
                prefecture_button = ft.ElevatedButton(
                    content=ft.Text(prefecture, data=prefecture),
                    on_click=on_prefecture_click,
                )
                prefectures_column.controls.append(prefecture_button)
            page.update()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.LOCATION_ON, label=area)
                for area in self.get_areas()
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

    def __del__(self):
        """Close database connection when done"""
        self.conn.close()

def main(page: ft.Page):
    app = WeatherApp()
    app.main(page)

ft.app(target=main)