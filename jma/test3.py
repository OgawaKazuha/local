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
        group_alignment=-0.9
    )

    def handle_expansion_tile_change(e):
        if e.control.trailing:
            e.control.trailing.name = (
                ft.icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE
                else ft.icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    regions = [
        "北海道地方",
        "東北地方",
        "関東甲信越地方",
        "東海地方",
        "北陸地方",
        "近畿地方",
        "中国地方（山口県を除く）",
        "四国地方",
        "九州地方（山口県を含む）",
        "沖縄地方",
    ]

    expansion_tiles = [
        ft.ExpansionTile(
            title=ft.Text(region),
            subtitle=ft.Text("地方の天気情報"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=False,
            collapsed_text_color=ft.colors.BLUE,
            text_color=ft.colors.BLUE,
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("この地方の天気情報を表示する"))],
        )
        for region in regions
    ]

    page.add(*expansion_tiles)
    

ft.app(main)