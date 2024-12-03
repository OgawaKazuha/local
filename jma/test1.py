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

        # ボタンを作る
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN, label="北海道地方"
            ),
       
     

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN, label="東北地方"
            ),
            
            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="関東甲信越地方"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="東海地方"
            ),

            ft.NavigationRailDestination(   
                icon=ft.icons.ARROW_DROP_DOWN,
                label="北陸地方"
            ),

            ft.NavigationRailDestination(  
                icon=ft.icons.ARROW_DROP_DOWN,
                label="近畿地方"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="中国地方（山口県を除く）"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="四国地方"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="九州地方（山口県を含む）"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="沖縄地方"
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index)
    )
    def on_destination_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:  # 北海道地方
        # JSONデータから北海道の天気情報を取得し、UIを更新する
         pass
        elif selected_index == 1:  # 東北地方
        # JSONデータから東北の天気情報を取得し、UIを更新する
            pass
    # 他の地方についても同様に処理を追加する

        rail = ft.NavigationRail(
        selected_index=0,
     # ... 残りのrailの設定 ...
        on_change=on_destination_change
        )


      
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column( alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
)

ft.app(main)