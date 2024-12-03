import json
import flet as ft
import requests

URL= 'https://www.jma.go.jp/bosai/common/const/area.json'
data_json = requests.get(URL).json() 

def get_prefectures(region_code):
    prefectures = []
    for office in data_json["offices"].values():
        if office["parent"] == region_code:
            prefectures.append(office["name"])
    return prefectures

def create_rail_destinations():
    destinations = []
    for region_code, region in data_json["centers"].items():
        prefectures = get_prefectures(region_code)
        destinations.append(
            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label=region["name"],
                trailing=ft.DropdownButton(
                    options=[ft.dropdown.Option(pref) for pref in prefectures],
                    on_change=on_prefecture_change,
                ),
            )
        )
    return destinations

def on_prefecture_change(e):
    selected_prefecture = e.control.value
    print(f"Selected prefecture: {selected_prefecture}")
    # ここで、選択された都道府県に対応する天気情報を取得し、UIを更新する処理を追加できます


def main(page: ft.Page):

    page.title = "天気予報"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def on_area_selected(e):
        selected_area_code = e.control.data
        # 選択された地域の天気情報を取得し、UIを更新する処理を追加する
        print(f"Selected area: {selected_area_code}")

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
                icon=ft.icons.ARROW_DROP_DOWN, label="北海道地方",
                trailing=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=area["area_name"],
                            data=area["area_code"],
                            on_click=on_area_selected,
                        )
                        for area in get_child_areas("010100")
                    ],
                ),
            ),
       
     

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN, label="東北地方",trailing=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=area["area_name"],
                            data=area["area_code"],
                            on_click=on_area_selected,
                        )
                        for area in get_child_areas("010200")
                    ],
                ),
            ),
            
            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="関東甲信越地方 010300"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="東海地方 010400"
            ),

            ft.NavigationRailDestination(   
                icon=ft.icons.ARROW_DROP_DOWN,
                label="北陸地方 010500"
            ),

            ft.NavigationRailDestination(  
                icon=ft.icons.ARROW_DROP_DOWN,
                label="近畿地方 010600"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="中国地方（山口県を除く） 010700"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="四国地方 010800"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="九州地方（山口県を含む） 010900"
            ),

            ft.NavigationRailDestination(
                icon=ft.icons.ARROW_DROP_DOWN,
                label="沖縄地方 011000"
            ),
        ],

        #ボタンをクリックする


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
        # ft.ElevatedButton(text="北海道地方", on_click=button_clicked) 
)

ft.app(main)