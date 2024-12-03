
import flet as ft



def main(page: ft.Page):
    page.title = "天気予報"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 地方と県の辞書を作成
    areas = {
        "北海道地方": ["北海道"],
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
    selected_prefectures = []

    def on_destination_change(e):
        nonlocal selected_area, selected_prefectures
        selected_index = e.control.selected_index
        selected_area = list(areas.keys())[selected_index]
        selected_prefectures = areas[selected_area]
        update_prefectures()

    def update_prefectures():
        prefectures_column.controls.clear()
        for prefecture in selected_prefectures:
            prefectures_column.controls.append(ft.Text(prefecture))
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
                prefectures_column,
            ],
            expand=True,
        )
    )

ft.app(main)
